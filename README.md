<img width="1857" height="882" alt="Screenshot 2026-10-03 110323" src="https://github.com/user-attachments/assets/02058dd2-a0d0-4414-964b-8999b1b1e3a4" />
<img width="1885" height="890" alt="Screenshot 2026-10-03 110304" src="https://github.com/user-attachments/assets/756f70b7-47ab-44fe-b9bf-558889e9385d" />
<img width="1878" height="893" alt="Screenshot 2026-10-03 110213" src="https://github.com/user-attachments/assets/5d5dc028-0d18-4a9b-b29e-4a0ab2cb5fb5" />
<img width="1881" height="897" alt="Screenshot 2026-10-03 110149" src="https://github.com/user-attachments/assets/4815d545-2d8f-4e58-938a-fbd7be33be22" />
<img width="1875" height="890" alt="Screenshot 2026-10-03 110050" src="https://github.com/user-attachments/assets/c1f4c344-48c2-43ab-99b2-350f42741809" />
<img width="1871" height="898" alt="Screenshot 2026-10-03 110029" src="https://github.com/user-attachments/assets/d412695b-ec0d-4845-90c8-59843b3f74ae" />
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
