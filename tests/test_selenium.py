import unittest
import threading
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from app import create_app, db
from app.models import User
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Flask server thread
def run_app():
    app = create_app()
    app.config.from_object("config.TestConfig")
    app.run(port=5001)

class SeleniumTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.server_thread = threading.Thread(target=run_app)
        cls.server_thread.daemon = True
        cls.server_thread.start()
        time.sleep(2)

        chrome_options = Options()
        # chrome_options.add_argument("--headless") 
        cls.driver = webdriver.Chrome(options=chrome_options)
        cls.driver.implicitly_wait(3)

        app = create_app()
        app.config.from_object("config.TestConfig")
        with app.app_context():
            db.drop_all()
            db.create_all()
            test_user = User(username='testuser', email='test@example.com')
            test_user.set_password('password123')
            db.session.add(test_user)
            db.session.commit()

    @classmethod
    def tearDownClass(cls):
        time.sleep(10)
        cls.driver.quit()

    def test_login_and_submit_player(self):
        driver = self.driver
        driver.get("http://127.0.0.1:5001/logout")
        time.sleep(1)

        driver.get("http://127.0.0.1:5001/")

        # Step 1: click Login / Register 按钮
        login_btn = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "button[data-bs-target='#authModal']"))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", login_btn)
        time.sleep(0.5)
        driver.execute_script("arguments[0].click();", login_btn)

        # Step 2: wait for modal to appear
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "authModal"))
        )

        # Step 3: write in username and password
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.NAME, "username"))
        ).send_keys("testuser")
        driver.find_element(By.NAME, "password").send_keys("password123")

        # Step 4: submit the form
        submit_btn = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#loginTab form input[type='submit']"))
        )
        driver.execute_script("arguments[0].click();", submit_btn)

        # Step 5: get into dashboard
        WebDriverWait(driver, 10).until(EC.url_contains("/dashboard"))
        self.assertIn("/dashboard", driver.current_url)

        # Step 6: open Add Player modal
        add_player_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "openPlayerModal"))
        )
        driver.execute_script("arguments[0].click();", add_player_btn)

        # Step 7: wait for modal to appear
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "addPlayerModal"))
        )

        # Step 8: fill in the form
        driver.find_element(By.NAME, "player_name").send_keys("Selenium Bot")
        driver.find_element(By.NAME, "league").send_keys("Test League")
        driver.find_element(By.NAME, "twitter_link").send_keys("https://twitter.com/test")
        driver.find_element(By.NAME, "twitch_link").send_keys("https://twitch.tv/test")
        driver.find_element(By.NAME, "photo_link").send_keys("https://example.com/photo.jpg")

        
        publish_btn = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#addPlayerModal button.btn.btn-success[name='action'][value='public']"))
        )
        driver.execute_script("arguments[0].click();", publish_btn)


        # Step 10: jump to dashboard
        WebDriverWait(driver, 10).until(
            EC.url_to_be("http://127.0.0.1:5001/dashboard/")
        )


        # screenshot before submit
        time.sleep(1)
        driver.save_screenshot("after_submit.png")
        self.assertIn("Dashboard", driver.title)  

        # step 11: manually check if the player is added
        time.sleep(1)
        driver.save_screenshot("after_submit.png")
        self.assertIn("Player added successfully", driver.page_source)



