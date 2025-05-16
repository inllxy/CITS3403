import unittest
from app import create_app, db
from app.models import Player, Competition, User
from flask import url_for
from config import Config, TestConfig

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    WTF_CSRF_ENABLED = False  # disable CSRF for testing

# unit test for adding player
class PlayerSubmitTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app(TestConfig)
        self.client = self.app.test_client()

        with self.app.app_context():
            db.drop_all()
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    # ensure user is logged in to allow access to dashboard
    def login_test_user(self):
        with self.app.app_context():
            user = User(username='testuser', email='test@example.com')
            user.set_password('testpassword')
            db.session.add(user)
            db.session.commit()
    
            with self.client.session_transaction() as sess:
                sess['_user_id'] = str(user.id)  # Flask-Login uses _user_id to track login

    def test_submit_player(self):
        self.login_test_user()
        data = {
            'player_name': 'Test Player',
            'league': 'Test League',
            'twitter_link': 'https://twitter.com/test',
            'twitch_link': 'https://twitch.tv/test',
            'visibility': 'private',
            'photo_link': 'https://example.com/photo.png'
        }
        response = self.client.post('/dashboard/submit-player', data=data, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Player added successfully', response.data)

        with self.app.app_context():
            player = Player.query.first()
            self.assertEqual(player.name, 'Test Player')
    
    # user not logged in, fails to add player
    def test_submit_player_not_allowed(self):
        data = {
            'player_name': 'Test Player',
            'league': 'Test League',
            'twitter_link': 'https://twitter.com/test',
            'twitch_link': 'https://twitch.tv/test',
            'visibility': 'private',
            'photo_link': 'https://example.com/photo.png'
        }
        response = self.client.post('/dashboard/submit-player', data=data, follow_redirects=True)
        self.assertIn(b'Please log in to access this page.', response.data)


# unit test for adding competition
class CompetitionSubmitTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app(TestConfig)
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()

    # ensure user is logged in to allow access to dashboard
    def login_test_user(self):
        with self.app.app_context():
            user = User(username='testuser', email='test@example.com')
            user.set_password('testpassword')
            db.session.add(user)
            db.session.commit()
    
            with self.client.session_transaction() as sess:
                sess['_user_id'] = str(user.id)  # Flask-Login uses _user_id to track login

    def test_submit_competition(self):
        self.login_test_user()
        data = {
            'name': 'Test Competition',
            'year': '2025',
            'month' : '3',
            'day' : '12',
            'poster_link' : 'https://example.com/poster.png',
            'logo_link': 'https://example.com/logo.png',
            'comp_link': 'https://competition-site.com/',
            'visibility': 'private',
        }
        response = self.client.post('/dashboard/submit-competition', data=data, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Competition added successfully', response.data)

        with self.app.app_context():
            competition = Competition.query.first()
            self.assertEqual(competition.name, 'Test Competition')
    
    # user not logged in, fails to add player
    def test_submit_competition_not_allowed(self):
        data = {
            'name': 'Test Competition',
            'year': '2025',
            'month' : '3',
            'day' : '12',
            'poster_link' : 'https://example.com/poster.png',
            'logo_link': 'https://example.com/logo.png',
            'comp_link': 'https://competition-site.com/',
            'visibility': 'private',
        }
        response = self.client.post('/dashboard/submit-competition', data=data, follow_redirects=True)
        self.assertIn(b'Please log in to access this page.', response.data)
    
    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

# unit test for loading all pages correctly
class PagesLoadingTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app(TestConfig)
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()

    def test_home_page_loads(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
    
    def test_player_page_loads(self):
        response = self.client.get('/players')
        self.assertEqual(response.status_code, 200)

    def test_competitions_accessible(self):
        response = self.client.get('/api/competitions')
        self.assertEqual(response.status_code, 200)

    # dashboard not accessible unless logged in
    def test_dashboard_no_login_no_access(self):
        response = self.client.get('/dashboard/')
        self.assertEqual(response.status_code, 302)

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

# unit test for user registering
class RegisterTestCase(unittest.TestCase):
     
    def setUp(self):
        self.app = create_app(TestConfig)
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()

    def test_register_user(self):
        data = {
            'username' : 'test_new',
            'email' : 'test_new@email.com',
            'password' : 'password1',
            'confirm' : 'password1'
        }
        response = self.client.post('/register', data=data, follow_redirects = True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Registration successful', response.data)

    def test_register_user_duplicate(self):
        data = {
            'username' : 'test',
            'email' : 'test@email.com',
            'password' : 'password1',
            'confirm' : 'password1'
        }
        user = User(username='test', email='test@email.com')
        user.set_password('password1')
        db.session.add(user)
        db.session.commit()
        response = self.client.post('/register', data=data, follow_redirects = True)
    
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'The username or email already exists', response.data)
    
    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

# unit test for user login
class LoginTestCase(unittest.TestCase):
     
    def setUp(self):
        self.app = create_app(TestConfig)
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
 
        db.create_all()
        user = User(username="test", email="test@email.com")
        user.set_password("password1")
        db.session.add(user)
        db.session.commit()

    def test_login(self):
        data = {
            'username' : 'test',
            'password' : 'password1'
        }
        response = self.client.post('/login', data=data, follow_redirects = True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login successful', response.data)

    def test_login_fail(self):
        data = {
            'username' : 'test',
            'password' : 'incorrect'
        }
        response = self.client.post('/login', data=data, follow_redirects = True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Incorrect account or password', response.data)

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

# unit test for likes functionality
class LikesTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()

    def test_like_api(self):
        # Pretend comp_id is 1
        response = self.client.post('/dashboard/api/like', json={'comp_id': 1})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'likes', response.data)
    
    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
            
 
if __name__ == '__main__':
    unittest.main()
 