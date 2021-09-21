from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()

def connect_db(app):
    """Connect this database to provided Flask app.
    You should call this in your Flask app.
    """
    db.app = app
    db.init_app(app)

class User(db.Model):

    __tablename__ = "users"

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
    def register(cls, username, password, email, first_name, last_name):
        """Return an instance of the User class w/ hashed password."""
        
        return cls(
            username=username,
            password=hash_password(password),
            email=email,
            first_name=first_name,
            last_name=last_name)

    @classmethod
    def login(cls, username, password):
        """Check for login w/ hashed password and return T/F"""

        user = cls.query.filter_by(username=username).one_or_none()

        if user and bcrypt.check_password_hash(user.password, password):
            return user
        else:
            return False

    @classmethod
    def check_login_credentials(cls, username, password):
        """Returns the user if username and password are valid login credentials.
        If invalid, it returns false"""
        
        user = cls.query.filter_by(username=username).one_or_none()

        if user and bcrypt.check_password_hash(user.password, password):
            return user
        else:
            return False


def hash_password(password):
    """Returns a bcrypt hash of the password provided"""
    
    hashed = bcrypt.generate_password_hash(password).decode('utf8')
    return hashed
