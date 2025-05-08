cd /d "%~dp0"
call venv\Scripts\activate.bat
set FLASK_APP=run.py
flask run
pause