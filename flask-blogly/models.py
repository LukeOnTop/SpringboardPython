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

    def __repr__(self):
        return (f"{self.id}, {self.first_name} - {self.last_name} -- {self.image_url}")

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