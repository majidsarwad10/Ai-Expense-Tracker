PennyPilot – AI-Assisted Personal Expense Tracker

A personal finance web application built with Python and Flask to record expenses, organize spending, visualize financial activity, and export transaction data.

> **AI transparency:** The initial categorizer uses editable keyword rules. It is not a trained machine-learning model or an external generative-AI service. The project is structured so a model-based classifier can be added later.

## Features

Add, edit, and delete expenses

Automatic expense category suggestions

Manual category selection

Monthly spending visualization

Category-wise spending dashboard

CSV transaction export

SQLite database persistence

Input validation

Automated testing with pytest

## Tech stack

Python 3.11+, Flask, SQLite, HTML, CSS, JavaScript, Chart.js, pytest.

## Run locally on Windows

1. Install Python 3.11 or newer and Git.
2. Open PowerShell in the project folder.
3. Create and activate a virtual environment:

   ```powershell
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

   If PowerShell blocks activation, use Command Prompt and run:

   ```cmd
   .venv\Scripts\activate.bat
   ```

4. Install dependencies:

   ```powershell
   python -m pip install -r requirements.txt
   ```

5. Start the application:

   ```powershell
   python app.py
   ```

6. Open http://127.0.0.1:5000 in your browser.

The SQLite database is created automatically in the Flask instance folder.

## Run tests

```powershell
python -m pytest -v
```

## Project structure

```text
ai-expense-tracker/
├── app.py
├── database.py
├── ai_categorizer.py
├── requirements.txt
├── templates/
├── static/
└── tests/
```

## Example category rules

Descriptions containing terms such as `lunch`, `coffee`, or `grocery` are suggested as Food. Terms such as `uber`, `metro`, or `petrol` are suggested as Transport. Unknown descriptions are assigned Other. Users can override suggestions.

## Privacy and security notes

- Use fictional sample transactions in screenshots and demos.
- Do not commit personal financial records or the SQLite database.
- Set a strong secret key using an environment variable before deployment.
- This portfolio version is intended for local demonstration, not as a production financial service.
- Add authentication, CSRF protection, rate limiting, and deployment security review before making it publicly available for real users.

## Future improvements

- Add user authentication and per-user data isolation
- Add date-range and category filters
- Add recurring expenses and budgets
- Add a model-based category classifier with an evaluation dataset
- Add API endpoints and integration tests
- Add CI with GitHub Actions

## Portfolio note

This project is independently developed as a learning and demonstration project. Update this README with your actual implementation decisions, test results, screenshots, and known limitations before presenting it to employers or assessment reviewers.
