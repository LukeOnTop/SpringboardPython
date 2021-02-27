"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

    #models go below
class User(db.Model):
    """"User"""

    __tablename__ = "user"

    id = db.Column(db.Integer,
                    primary_key=True,  
                    autoincrement=True)

    first_name = db.Column(db.String(20),
                            nullable=False,
                            unique=False)

    last_name = db.Column(db.String(20),
                            nullable=False,
                            unique=False)

    image_url = db.Column(db.VARCHAR(500), 
                            nullable=False,
                            unique=False)

    posts = db.relationship("Post", backref="user", cascade="all, delete-orphan")

    

class Post(db.Model):
    """"Post"""

    __tablename__ = "post"

    id = db.Column(db.Integer,
                    primary_key=True,  
                    autoincrement=True)


    title = db.Column(db.String(50), 
                        nullable=False,
                        unique=False)

    content = db.Column(db.String(250),
                        nullable=False,
                        unique=False)

    created_at = db.Column(db.DateTime, 
                        nullable=False, 
                        unique=False)

    user_code = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)

    #tags = db.relationship("Tag", secondary="posts_tags", backref="post")

class PostTag(db.Model):
    """Tag on a post."""

    __tablename__ = "posts_tags"

    post_id = db.Column(db.Integer, db.ForeignKey('post.id', ondelete="CASCADE"), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id', ondelete="CASCADE"), primary_key=True)


class Tag(db.Model):
    """Tag that can be added to posts."""

    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key=True)
    
    name = db.Column(db.Text, nullable=False, unique=True)

    post = db.relationship("Post", secondary="posts_tags", backref="tags")

    
    # cascade="all,delete",




