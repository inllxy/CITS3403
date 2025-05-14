import unittest
import threading
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from app import create_app, db
from app.models import User
from werkzeug.security import generate_password_hash
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Flask server thread
def run_app():
    app = create_app()
    app.config.from_object("config.TestConfig")
    app.run(port=5001)  # Use a separate port to avoid conflicts

class SeleniumTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Start Flask app in a thread
        cls.server_thread = threading.Thread(target=run_app)
        cls.server_thread.daemon = True
        cls.server_thread.start()
        time.sleep(2)  # Wait a bit for the server to start

        # Setup headless browser
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        cls.driver = webdriver.Chrome(options=chrome_options)
        cls.driver.implicitly_wait(3)

        # Create a test user in the DB
        app = create_app()
        app.config.from_object("config.TestConfig")
        with app.app_context():
            db.drop_all()
            db.create_all()
            if not User.query.filter_by(email='test@example.com').first():
                test_user = User(username='testuser', email='test@example.com')
                test_user.set_password('password123')
                db.session.add(test_user)
                db.session.commit()


    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def test_login_and_submit_player(self):
        self.driver.get("http://127.0.0.1:5001/logout")
        time.sleep(1)

        self.driver.get("http://127.0.0.1:5001/")  # Home page has the login form

        # Fill in login form on home page
        self.driver.find_element(By.NAME, "username").send_keys("testuser")
        self.driver.find_element(By.NAME, "password").send_keys("password123")
        self.driver.find_element(By.CSS_SELECTOR, "form button").click()

        # Wait for redirect to dashboard
        time.sleep(1)
        self.assertIn("/dashboard", self.driver.current_url)

        # Click modal open button (if it exists)
        try:
            open_btn = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable((By.ID, "openPlayerModal"))
            )
            open_btn.click()
            time.sleep(1)  # Give modal time to fully display
        except:
            print("Modal already open or not needed.")

        # Fill out player form
        self.driver.find_element(By.NAME, "player_name").send_keys("Selenium Bot")
        self.driver.find_element(By.NAME, "league").send_keys("Test League")
        self.driver.find_element(By.NAME, "twitter_link").send_keys("https://twitter.com/test")
        self.driver.find_element(By.NAME, "twitch_link").send_keys("https://twitch.tv/test")
        self.driver.find_element(By.NAME, "photo_link").send_keys("https://example.com/photo.jpg")
        self.driver.find_element(By.CSS_SELECTOR, "form button[type=submit]").click()

        time.sleep(1)
        self.assertIn("Player added successfully", self.driver.page_source)
