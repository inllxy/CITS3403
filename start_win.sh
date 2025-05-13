#!/bin/bash

if [ ! -d "venv" ]; then
  echo "Creating virtual environment..."
  python -m venv venv
fi

source venv/Scripts/activate


venv/Scripts/python -m pip install --upgrade pip
venv/Scripts/python -m pip install flask flask-sqlalchemy flask-login flask-migrate email-validator flask-wtf


export FLASK_APP=run.py


if [ ! -d "migrations" ]; then
    echo "Initializing database migration setup..."
    venv/Scripts/python -m flask db init
    venv/Scripts/python -m flask db migrate -m "Initial migration"
    venv/Scripts/python -m flask db upgrade
else
    echo "Migrations already set up. Upgrading database..."
    venv/Scripts/python -m flask db upgrade
fi

echo "Starting Flask server at http://127.0.0.1:5000"
venv/Scripts/python -m flask run
