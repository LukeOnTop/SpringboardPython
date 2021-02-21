from unittest import TestCase
from app import app
from models import db, User

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()

class UserRouteTestCase(TestCase):
    """Tests for views for Users."""

    def setUp(self):
        """Add sample user."""

        User.query.delete()

        user = User(first_name="FirstNameJohn", last_name= "LastNameDoe", image_url="https://picsum.photos/200")
        db.session.add(user)
        db.session.commit()

        self.user_id = user.id

    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()


    def test_home_page(self):
        with app.test_client() as client:
           resp = client.get("/")
           html = resp.get_data(as_text=True)
           self.assertEqual(resp.status_code, 200)
           self.assertIn('FirstNameJohn', html)


    def test_user_details(self):
        with app.test_client() as client:
            resp = client.get(f"/{self.user_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>FirstNameJohn LastNameDoe</h1>', html)


    def test_edit_user(self):
        with app.test_client() as client:
            resp = client.get(f"/edit{self.user_id}")
            html = resp.get_data(as_text=True)
    
            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>Edit Me! - FirstNameJohn</h1>', html)


    def test_add_user(self):
        with app.test_client() as client:
            resp = client.get(f"/add-user")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>Add User</h1>', html)