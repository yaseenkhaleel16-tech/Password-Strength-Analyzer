# Password Strength Analyzer & Security Suggestion Tool

A beginner-friendly defensive cybersecurity project built with Python Flask.

## Features
- Real-time password strength meter
- 0–100 project-defined score
- VERY WEAK / WEAK / MODERATE / STRONG / VERY STRONG classification
- Length analysis
- Character diversity analysis
- Common-password detection
- Sequence detection
- Keyboard-pattern detection
- Repetition detection
- Predictable word/year detection
- Optional personal-context warning
- Educational entropy estimate
- Specific security suggestions
- Secure password generator using `secrets`
- Show/hide password
- Automated tests

## Privacy design
Submitted passwords are processed in memory only. This beginner version does not store passwords, log passwords, place them in URLs, or put them in a database.

Use only synthetic/demo passwords for screenshots and testing.

## Run on Windows

Open Command Prompt inside this folder:

```text
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Then open:

`http://127.0.0.1:5000`

## Run tests

```text
pytest
```

## Demo inputs
Use synthetic examples from the assignment such as:
- 123456
- Password123!
- aaaaaaaaaaaaaaaa
- qwerty2026!

Do not use your real password.

## Important limitation
The score is a project-defined educational heuristic, not a universal security standard. Entropy is theoretical and assumes random selection, which does not describe many human-created passwords.

## Suggested future improvements
- SQLite aggregate analytics without password fields
- Configurable password policies
- Privacy-preserving breach checking
- FastAPI/React version
- MFA and password-manager education
- Passkey/WebAuthn awareness
