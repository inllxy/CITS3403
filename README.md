# SF6 Spotlight — Flask Backend Quick-Start Guide

> **Goal**  
> Spin the project up locally and open `http://127.0.0.1:5000/` with just a few commands.

---

## Steps

```bash
# 1. Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate        # macOS / Linux
# .\venv\Scripts\activate       # Windows PowerShell

# 2. Install dependencies
python -m pip install --upgrade pip
python -m pip install Flask Flask-SQLAlchemy Flask-Login email-validator

# 3. Initialize the database (run once)
python -m flask --app app.py init-db

# 4. Start the development server
python -m flask --app app.py run
