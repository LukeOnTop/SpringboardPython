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

    user_code = db.Column(db.Integer, db.ForeignKey('user.id'))