#!/bin/bash

# Activate the virtual environment
python3 -m venv venv     
source venv/bin/activate
./venv/bin/python3 -m pip install flask flask-sqlalchemy flask-login flask-migrate email-validator flask-wtf
# Set Flask app
export FLASK_APP=run.py

# Check if migrations folder exists
if [ ! -d "migrations" ]; then
    echo "Initializing database migration setup..."
    ./venv/bin/python3 -m flask db init
    ./venv/bin/python3 -m flask db migrate -m "Initial migration"
    ./venv/bin/python3 -m flask db upgrade
else
    echo "Migrations already set up. Upgrading database..."
    ./venv/bin/python3 -m flask db upgrade
fi

# Run the development server
echo "Starting Flask server at http://127.0.0.1:5000"
./venv/bin/python3 -m flask run
