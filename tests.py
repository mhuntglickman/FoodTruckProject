
import unittest

from party import app
from model import db, example_data, connect_to_db


class PartyTests(unittest.TestCase):
    """Tests for my party site."""

    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_homepage(self):
        result = self.client.get("/")
        self.assertIn("board games, rainbows, and ice cream sundaes", result.data)

    def test_no_rsvp_yet(self):
        # FIXME: Add a test to show we see the RSVP form, but NOT the party details
        result = self.client.get("/")
        self.assertNotIn("Party Details", result.data)
        self.assertIn("Please RSVP", result.data)

    def test_rsvp(self):
        result = self.client.post("/rsvp",
                                  data={'name': "Jane", 'email': "jane@jane.com"},
                                  follow_redirects=True)
        # FIXME: Once we RSVP, we should see the party details, but not the RSVP form
        self.assertIn("Party Details", result.data)


class PartyTestsDatabase(unittest.TestCase):
    """Flask tests that use the database."""

    def setUp(self):
        """Stuff to do before every test."""
        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'key123'
        self.client = app.test_client()

        with self.client as c:
            with c.session_transaction() as sess:
                sess['RSVP'] = True
        

        # Connect to test database (uncomment when testing database)
        connect_to_db(app, "postgresql:///testdb")

        # Create tables and add sample data (uncomment when testing database)
        db.create_all()
        example_data()

    def tearDown(self):
        """Do at end of every test."""

        # (uncomment when testing database)
        db.session.close()
        db.drop_all()

    def test_games(self):
        # FIXME: test that the games page displays the game from example_data()
        result = self.client.get("/games", follow_redirects=True)
        self.assertIn("Monopoly", result.data)


if __name__ == "__main__":
    unittest.main()
Status API Training Shop Blog About
© 2016 GitHub, Inc. Terms Privacy Security Contact Help