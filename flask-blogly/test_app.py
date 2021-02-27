from unittest import TestCase
from app import app
from models import db, User, Post

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

        # User.query.delete() ## try removing because db.drop_all() should already handle this. 
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


    def test_user_profile(self):
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
            self.assertIn('<input type="text" name="first-name" placeholder="first name">', html)

    def test_make_post(self):
        
        with app.test_client() as client:
            resp = client.get(f"/new-post{self.user_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn(f"<h3>Content</h3>", html)



class PostRouteTestCase(TestCase):
    """Tests for views for Users."""

    def setUp(self):
        """Add sample user."""

        Post.query.delete()
        post = Post(title="First title", content="First content", created_at="2021-02-24 12:01:00", user_code=None)
        db.session.add(post)
        db.session.commit()

        self.post = post


    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()


    def test_show_post(self):
        
        with app.test_client() as client:
            resp = client.get(f"/user-post{self.post.id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn(f"<h2>First title</h2>", html)