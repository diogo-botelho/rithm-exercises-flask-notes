from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import bcrypt

db = SQLAlchemy()

def connect_db(app):
    """Connect this database to provided Flask app.
    You should call this in your Flask app.
    """
    db.app = app
    db.init_app(app)

class User(db.Models):

    username = db.Column(
        db.String(20), 
        primary_key=True)

    password = db.Column(
        db.String(100), 
        nullable=False)

    email = db.Column(
        db.String(50), 
        nullable=False,
        unique=True)

    first_name = db.Column(
        db.String(30), 
        nullable=False)

    last_name = db.Column(
        db.String(30), 
        nullable=False)

    @classmethod
    def register(cls, username, password):
        """Register a user w/ hashed password and return user
        IF both username and email are unique. Otherwise return false"""
        #FINISH UP AFTER MAKING FORM
        hashed = bcrypt.generate_password_hash(password).decode('utf8')

        return cls(username=username, password=hashed)

    @classmethod
    def login(cls, username, password):
        """Check for login w/ hashed password and return T/F"""

        user = cls.query.filter_by(username=username).one_or_none()

        if user and bcrypt.check_password_hash(user.password, password):
            return user
        else:
            return False