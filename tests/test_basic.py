import unittest
from app import create_app, db
from app.models import Player, Competition
from flask import url_for
from config import Config

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    WTF_CSRF_ENABLED = False  # disable CSRF for testing

class BasicTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.app.config.from_object(TestConfig)
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_home_page_loads(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_submit_player(self):
        data = {
            'player_name': 'Test Player',
            'league': 'Test League',
            'twitter_link': 'https://twitter.com/test',
            'twitch_link': 'https://twitch.tv/test',
            'visibility': 'private',
            'photo_link': 'https://example.com/photo.png'
        }
        response = self.client.post('/dashboard/submit-player', data=data, follow_redirects=True)
        self.assertIn(b'Player added successfully', response.data)

        with self.app.app_context():
            player = Player.query.first()
            self.assertEqual(player.name, 'Test Player')

    def test_like_api(self):
        # Pretend comp_id is 1
        response = self.client.post('/dashboard/api/like', json={'comp_id': 1})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'likes', response.data)

    def test_add_comment_invalid(self):
        response = self.client.post('/dashboard/api/comment', json={'text': ''})
        self.assertEqual(response.status_code, 400)

