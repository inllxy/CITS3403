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
from selenium.webdriver.support.ui import Select

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
            # Add recipient user
            recipient_user = User(username='testuser2', email='test2@example.com')
            recipient_user.set_password('password456')
            db.session.add(recipient_user)

            db.session.commit()

    @classmethod
    def tearDownClass(cls):
        time.sleep(10)
        cls.driver.quit()

     # TEST 1: login and submit player
    def test_1_login_and_submit_player(self):
        driver = self.driver
        driver.get("http://127.0.0.1:5001/logout")
        time.sleep(1)

        driver.get("http://127.0.0.1:5001/")

        # Step 1: click Login / Register 
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

    # TEST 2: submit full competition
    def test_2_submit_full_competition(self):
        driver = self.driver
        driver.get("http://127.0.0.1:5001/logout")
        time.sleep(1)

        driver.get("http://127.0.0.1:5001/")

        login_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-bs-target='#authModal']"))
        )
        driver.execute_script("arguments[0].click();", login_btn)

        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.NAME, "username"))).send_keys("testuser")
        driver.find_element(By.NAME, "password").send_keys("password123")

        submit_btn = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#loginTab form input[type='submit']"))
        )
        driver.execute_script("arguments[0].click();", submit_btn)

        WebDriverWait(driver, 10).until(EC.url_contains("/dashboard"))
        self.assertIn("/dashboard", driver.current_url)

        # Handle flash alert from login
        try:
            alert_box = WebDriverWait(driver, 5).until(
                EC.visibility_of_element_located((By.CLASS_NAME, "alert"))
            )
            print("Flash alert appeared")
            try:
                close_btn = alert_box.find_element(By.CLASS_NAME, "btn-close")
                driver.execute_script("arguments[0].click();", close_btn)
                WebDriverWait(driver, 3).until(EC.invisibility_of_element(alert_box))
                print("Flash alert closed")
            except Exception:
                print("Flash alert has no close button — continuing")
        except Exception:
            print("No flash alert appeared — continuing")

        # Corrected button ID from 'openCompetitionModal' to 'openModal'
        add_comp_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "openModal"))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", add_comp_btn)
        driver.execute_script("arguments[0].click();", add_comp_btn)

        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "addCompetitionModal"))
        )

        driver.find_element(By.NAME, "name").send_keys("Selenium Bracket")
        driver.find_element(By.NAME, "year").send_keys("2025")
        Select(driver.find_element(By.NAME, "month")).select_by_value("5")
        driver.find_element(By.NAME, "day").send_keys("22")
        driver.find_element(By.NAME, "poster_link").send_keys("https://example.com/poster.jpg")
        driver.find_element(By.NAME, "logo_link").send_keys("https://example.com/logo.jpg")
        driver.find_element(By.NAME, "comp_link").send_keys("https://example.com")

        def fill_match(round_id, match_id):
            driver.find_element(By.NAME, f"{round_id}_match{match_id}_team1").send_keys(f"Team{match_id}A")
            driver.find_element(By.NAME, f"{round_id}_match{match_id}_player1").send_keys(f"Player{match_id}A")
            driver.find_element(By.NAME, f"{round_id}_match{match_id}_score1").send_keys("1")
            driver.find_element(By.NAME, f"{round_id}_match{match_id}_team2").send_keys(f"Team{match_id}B")
            driver.find_element(By.NAME, f"{round_id}_match{match_id}_player2").send_keys(f"Player{match_id}B")
            driver.find_element(By.NAME, f"{round_id}_match{match_id}_score2").send_keys("2")

        rounds = {
            "round1": [1, 2, 3, 4],
            "round2": [13, 14],
            "round3": [19],
            "round4": [23],
            "round5": [5, 6, 7, 8],
            "round6": [9, 10, 11, 12],
            "round7": [15, 16],
            "round8": [17, 18],
            "round9": [20],
            "round10": [21],
        }

        for r, matches in rounds.items():
            for m in matches:
                fill_match(r, m)

        submit_btn = driver.find_element(By.CSS_SELECTOR, "button[type='submit'][value='public']")
        driver.execute_script("arguments[0].click();", submit_btn)

        WebDriverWait(driver, 10).until(EC.url_contains("/dashboard"))
        time.sleep(1)
        driver.save_screenshot("competition_submitted.png")
        self.assertIn("Dashboard", driver.title)
        
        # TEST 3: delete a player card that was already submitted
    def test_3_delete_player_card(self):
        driver = self.driver

        # Log in as testuser
        driver.get("http://127.0.0.1:5001/logout")
        driver.get("http://127.0.0.1:5001/")
        login_btn = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "button[data-bs-target='#authModal']"))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", login_btn)
        time.sleep(0.5)
        driver.execute_script("arguments[0].click();", login_btn)

        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.NAME, "username"))).send_keys("testuser")
        driver.find_element(By.NAME, "password").send_keys("password123")
        driver.find_element(By.CSS_SELECTOR, "#loginTab form input[type='submit']").click()

        WebDriverWait(driver, 10).until(EC.url_contains("/dashboard"))

        # Locate the player card by name
        player_cards = driver.find_elements(By.CLASS_NAME, "player-card")
        target_card = None
        for card in player_cards:
            name = card.find_element(By.CLASS_NAME, "player-name").text.strip()
            if name == "Selenium Bot":
                target_card = card
                break

        self.assertIsNotNone(target_card, "Player card not found")

        # Find and click delete button in the form
        delete_form = target_card.find_element(By.TAG_NAME, "form")
        delete_button = delete_form.find_element(By.CSS_SELECTOR, "input[type='submit']")
        driver.execute_script("arguments[0].click();", delete_button)

        # Confirm deletion if browser alert appears
        try:
            WebDriverWait(driver, 3).until(EC.alert_is_present())
            driver.switch_to.alert.accept()
        except:
            pass  # continue even if no JS alert appears

        # Wait for redirect and verify deletion
        WebDriverWait(driver, 10).until(EC.url_contains("/dashboard"))
        time.sleep(1)
        # Make sure no player card contains "Selenium Bot"
        player_cards = driver.find_elements(By.CLASS_NAME, "player-card")
        for card in player_cards:
            name = card.find_element(By.CLASS_NAME, "player-name").text.strip()
            self.assertNotEqual(name, "Selenium Bot", "Player card was not deleted")


        # TEST 4: share competition and verify with recipient
    def test_4_share_competition(self):
        # Restart browser to simulate a fresh session
        self.driver.quit()
        chrome_options = Options()
        # chrome_options.add_argument("--headless")
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.implicitly_wait(3)
        driver = self.driver

        # Login as testuser
        driver.get("http://127.0.0.1:5001/logout")
        driver.get("http://127.0.0.1:5001/")

        login_btn = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "button[data-bs-target='#authModal']"))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", login_btn)
        time.sleep(0.5)
        driver.execute_script("arguments[0].click();", login_btn)

        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.NAME, "username"))).send_keys("testuser")
        driver.find_element(By.NAME, "password").send_keys("password123")
        driver.find_element(By.CSS_SELECTOR, "#loginTab form input[type='submit']").click()
        WebDriverWait(driver, 10).until(EC.url_contains("/dashboard"))

        # Find the competition card titled "Selenium Bracket"
        cards = driver.find_elements(By.CLASS_NAME, "competition-result-item")
        share_card = None
        for card in cards:
            try:
                title = card.find_element(By.CSS_SELECTOR, "h3.title").text.strip()
                if title == "Selenium Bracket":
                    share_card = card
                    break
            except:
                continue

        self.assertIsNotNone(share_card, "Competition card not found")

        # Click share button and submit username
        share_btn = share_card.find_element(By.CSS_SELECTOR, "button.btn-outline-primary")
        driver.execute_script("arguments[0].click();", share_btn)

        share_input = share_card.find_element(By.NAME, "share_with")
        share_input.send_keys("testuser2")

        comp_id = share_btn.get_attribute("id").replace("toggle-share-", "")
        form_id = f"share-form-{comp_id}"
        submit_share = driver.find_element(By.CSS_SELECTOR, f"form#{form_id} button[type='submit']")
        driver.execute_script("arguments[0].click();", submit_share)

        WebDriverWait(driver, 10).until(EC.url_contains("/dashboard"))
        driver.get("http://127.0.0.1:5001/logout")

        # Login as recipient (testuser2)
        driver.get("http://127.0.0.1:5001/")
        login_btn = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "button[data-bs-target='#authModal']"))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", login_btn)
        time.sleep(0.5)
        driver.execute_script("arguments[0].click();", login_btn)

        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.NAME, "username"))).send_keys("testuser2")
        driver.find_element(By.NAME, "password").send_keys("password456")
        driver.find_element(By.CSS_SELECTOR, "#loginTab form input[type='submit']").click()

        WebDriverWait(driver, 10).until(EC.url_contains("/dashboard"))
        time.sleep(1)

        # Final check: shared comp visible to testuser2
        self.assertIn("Selenium Bracket", driver.page_source)
        driver.save_screenshot("shared_competition.png")

