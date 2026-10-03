from flask import Flask, render_template, request, jsonify
import math
import re
import secrets
import string
from datetime import datetime

app = Flask(__name__)

COMMON_PASSWORDS = {
    "password", "password123", "123456", "12345678", "qwerty",
    "letmein", "welcome", "admin", "admin123", "hello123"
}

KEYBOARD_PATTERNS = [
    "qwerty", "asdf", "zxcv", "1234", "5678", "9876",
    "1qaz", "2wsx", "qwerty123", "asdf123"
]

DEMO_WORDS = {
    "password", "welcome", "admin", "letmein", "hello", "qwerty",
    "summer", "winter", "football", "dragon", "monkey", "login"
}

def analyze_length(password):
    n = len(password)
    if n < 8:
        label = "Very short"
    elif n <= 11:
        label = "Short"
    elif n <= 15:
        label = "Better length"
    else:
        label = "Strong length contribution"
    return {"length": n, "label": label}

def analyze_characters(password):
    checks = {
        "lowercase": any(c.islower() for c in password),
        "uppercase": any(c.isupper() for c in password),
        "digits": any(c.isdigit() for c in password),
        "symbols": any(c in string.punctuation for c in password),
        "spaces": any(c.isspace() for c in password),
    }
    unique = len(set(password)) if password else 0
    ratio = round(unique / len(password), 2) if password else 0
    return {
        "types": checks,
        "character_type_count": sum(checks.values()),
        "unique_character_count": unique,
        "unique_character_ratio": ratio
    }

def detect_sequences(password):
    s = password.lower()
    found = []
    for i in range(len(s) - 3):
        chunk = s[i:i+4]
        if all(ord(chunk[j+1]) - ord(chunk[j]) == 1 for j in range(3)):
            found.append(chunk)
        elif all(ord(chunk[j+1]) - ord(chunk[j]) == -1 for j in range(3)):
            found.append(chunk)
    return list(dict.fromkeys(found))

def detect_keyboard_patterns(password):
    s = password.lower()
    found = []
    for pattern in KEYBOARD_PATTERNS:
        if pattern in s or pattern[::-1] in s:
            found.append(pattern)
    return found

def detect_repetition(password):
    repeated_chars = bool(re.search(r"(.)\1{2,}", password))
    repeated_substrings = []
    for size in range(2, min(6, len(password)//2 + 1)):
        for i in range(len(password) - 2*size + 1):
            part = password[i:i+size]
            if part and password[i+size:i+2*size] == part:
                repeated_substrings.append(part)
    return {
        "repeated_characters": repeated_chars,
        "repeated_substrings": list(dict.fromkeys(repeated_substrings))
    }

def detect_predictable_structure(password):
    s = password.lower()
    findings = []
    # Common word followed by digits/symbols
    if re.search(r"^[a-z]+[0-9!@#$%^&*._-]+$", s):
        word = re.match(r"^[a-z]+", s)
        if word and word.group() in DEMO_WORDS:
            findings.append("Common word followed by predictable numbers/symbols")
    # Year-like suffix/pattern
    if re.search(r"(19|20)\d{2}", s):
        findings.append("Year-like pattern detected")
    # Simple date-like pattern
    if re.search(r"(0?[1-9]|[12]\d|3[01])[-/]?(0?[1-9]|1[0-2])[-/]?(19|20)?\d{2}", s):
        findings.append("Date-like pattern detected")
    return findings

def detect_dictionary(password):
    s = password.lower()
    if s in COMMON_PASSWORDS:
        return True
    parts = re.split(r"[\W_]+", s)
    return any(part in DEMO_WORDS and len(part) >= 4 for part in parts)

def estimate_entropy(password, chars):
    if not password:
        return 0.0
    pool = 0
    if chars["types"]["lowercase"]: pool += 26
    if chars["types"]["uppercase"]: pool += 26
    if chars["types"]["digits"]: pool += 10
    if chars["types"]["symbols"]: pool += 32
    if chars["types"]["spaces"]: pool += 1
    pool = max(pool, 1)
    # Educational theoretical estimate only.
    return round(len(password) * math.log2(pool), 1)

def analyze_password(password, context=None):
    password = password or ""
    length = analyze_length(password)
    chars = analyze_characters(password)
    sequences = detect_sequences(password)
    keyboard = detect_keyboard_patterns(password)
    repetition = detect_repetition(password)
    predictable = detect_predictable_structure(password)
    common = detect_dictionary(password)
    entropy = estimate_entropy(password, chars)

    findings = []
    suggestions = []
    score = 0

    if not password:
        return {
            "score": 0, "classification": "VERY WEAK",
            "findings": ["Empty password."],
            "suggestions": ["Enter a password or generate a secure demo password."],
            "metrics": {
                "length": 0, "character_type_count": 0,
                "unique_character_count": 0, "unique_character_ratio": 0,
                "entropy_bits": 0
            }
        }

    # Length: up to 35
    if len(password) >= 16:
        score += 35
    elif len(password) >= 12:
        score += 27
    elif len(password) >= 8:
        score += 18
    elif len(password) >= 6:
        score += 8
    else:
        findings.append("Password is too short.")
        suggestions.append("Use at least 12–16 characters.")
    if len(password) >= 8 and len(password) < 12:
        suggestions.append("Increase the length for better resistance to guessing.")

    # Character diversity: up to 15
    score += min(chars["character_type_count"] * 4, 15)
    if chars["character_type_count"] < 3:
        findings.append("Limited character variety.")
        suggestions.append("Consider a mix of character types, while prioritizing unpredictability.")

    # Unique ratio: up to 10
    score += round(chars["unique_character_ratio"] * 10)

    # Pattern resistance: up to 20
    pattern_count = len(sequences) + len(keyboard) + len(predictable)
    if not sequences and not keyboard and not predictable:
        score += 20
    elif pattern_count == 1:
        score += 10
    else:
        score += 3

    if sequences:
        findings.append("Sequential characters detected: " + ", ".join(sequences))
        suggestions.append("Avoid predictable sequences such as 1234 or abcd.")
    if keyboard:
        findings.append("Keyboard pattern detected.")
        suggestions.append("Avoid keyboard walks such as qwerty or asdf.")
    if repetition["repeated_characters"]:
        findings.append("Repeated characters detected.")
        suggestions.append("Avoid repeated-character patterns such as aaa or 111.")
    if repetition["repeated_substrings"]:
        findings.append("Repeated substring detected.")
        suggestions.append("Avoid repeating the same short substring.")
    if predictable:
        findings.extend(predictable)
        suggestions.append("Avoid predictable word + number/year combinations.")

    # Common password: up to 10
    if common:
        findings.append("Common password or common word detected.")
        suggestions.append("Do not use common passwords or common words as the main password.")
    else:
        score += 10

    # Additional unpredictability: up to 10
    if not common and not sequences and not keyboard and not repetition["repeated_characters"]:
        score += 10

    # Optional context check
    if context:
        for value in context:
            value = (value or "").strip().lower()
            if len(value) >= 3 and value in password.lower():
                findings.append("Password appears to contain supplied personal context.")
                suggestions.append("Avoid names, college/company names, birthdays, or other personal information.")
                score -= 10
                break

    score = max(0, min(100, score))

    if score <= 20:
        classification = "VERY WEAK"
    elif score <= 40:
        classification = "WEAK"
    elif score <= 60:
        classification = "MODERATE"
    elif score <= 80:
        classification = "STRONG"
    else:
        classification = "VERY STRONG"

    if not findings:
        findings.append("No obvious weakness pattern detected by this project.")
    suggestions.append("Use a unique password for every account.")
    suggestions.append("Consider a password manager and enable MFA where available.")

    return {
        "score": score,
        "classification": classification,
        "findings": list(dict.fromkeys(findings)),
        "suggestions": list(dict.fromkeys(suggestions)),
        "metrics": {
            "length": length["length"],
            "length_label": length["label"],
            "character_type_count": chars["character_type_count"],
            "unique_character_count": chars["unique_character_count"],
            "unique_character_ratio": chars["unique_character_ratio"],
            "entropy_bits": entropy,
            "sequence_count": len(sequences),
            "keyboard_pattern_count": len(keyboard),
            "repetition_detected": repetition["repeated_characters"] or bool(repetition["repeated_substrings"]),
            "pattern_count": pattern_count
        }
    }

def generate_password(length=20):
    length = max(16, min(int(length), 64))
    alphabet = string.ascii_letters + string.digits + "!@#$%^&*()-_=+[]{};:,.?"
    # secrets is used instead of random for security-sensitive randomness.
    return "".join(secrets.choice(alphabet) for _ in range(length))

@app.route("/")
def home():
    return render_template("index.html")

@app.post("/api/analyze")
def api_analyze():
    data = request.get_json(silent=True) or {}
    password = data.get("password", "")
    context = data.get("context", [])
    if not isinstance(context, list):
        context = []
    # Password is analyzed in memory only and is never logged or stored.
    return jsonify(analyze_password(password, context))

@app.get("/api/generate-password")
def api_generate():
    length = request.args.get("length", 20, type=int)
    return jsonify({"password": generate_password(length)})

@app.get("/api/dashboard/stats")
def dashboard_stats():
    # Demo aggregate data only. No submitted password is stored.
    return jsonify({
        "message": "This demo dashboard intentionally does not store submitted passwords.",
        "generated_at": datetime.now().isoformat(timespec="seconds")
    })

if __name__ == "__main__":
    app.run(debug=True)
