# SF6 Spotlight – Tournament Web Application

## 📝 Purpose & Design

This application is designed to support the management and visualization of competitive brackets for Street Fighter 6 (SF6) tournaments. It allows authenticated users to:

1.Register and log in to access their personal dashboard.

2.Submit match results and player data to contribute to the tournament record.

3.View detailed player statistics, including each player's win rate, total matches played, and matches won.

4.Share specific match results with other users. Shared results are visible to the recipient in a dedicated section of their dashboard.

5.View and manage all matches and players they have submitted, including options to delete or share them with others.

The system is built using Flask (Python) with SQLite for lightweight database storage. The frontend uses Bootstrap to provide a responsive and clean user interface, and Jinja2 for dynamic HTML templating. Flask-WTF is used for secure and user-friendly form handling. The overall design focuses on simplicity, accessibility, and modularity to support future feature expansion.
## 👥 Group Members

| UWA ID       | Name        | GitHub Username |
|--------------|-------------|------------------|
|23915299      |Harper Chen  |inllxy            |
|23751927      |Jenna Milford|jmil47            |
|24322728      |Weichen Wang |GlazeStar         |
|23867057      |Namgay Choden|Nchoden           |

## 🚀 How to Launch the Application

1.  **Create and activate a virtual environment**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

2.  **Install dependencies**
    ```bash
    python3 -m pip install -r requirements.txt
    ```

3.  **Run the application**
    ```bash
    python3 run.py
    ```
    The app will be available at http://127.0.0.1:5000 by default.

## 🚀 How to Run the Tests for the Application

1.  **Create and activate a virtual environment**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

2.  **Install dependencies**
    ```bash
    python3 -m pip install -r requirements.txt
    pip install selenium
    ```

3.  **Run Selenium tests**
    ```bash
    python3 -m tests.test_selenium
    ```

4.  **Run basic unit tests**
    ```bash
    python3 -m tests.test_basic
    ```
