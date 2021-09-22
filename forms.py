"""Forms for adopt app."""
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import InputRequired, length, Email

class RegisterUserForm(FlaskForm):
    """Form for registering new users"""

    username = StringField("Username", 
        validators=[InputRequired(), length(max=20)])

    password = StringField("Password", 
        validators=[InputRequired(), length(max=100)]) #can make password field a PasswordField, which prevents the password from being displayed when it's being typed
        
    email = StringField("Email",
        validators=[InputRequired(), length(max=50), Email()])

    first_name = StringField("First Name",
        validators=[InputRequired(), length(max=30)])

    last_name = StringField("Last Name",
        validators=[InputRequired(), length(max=30)])

class LoginForm(FlaskForm):
    """Form for logging in users"""

    username = StringField("Username", 
        validators=[InputRequired(), length(max=20)])

    password = StringField("Password", 
        validators=[InputRequired(), length(max=100)])
        
#Code REview: Create a very simple form for logging out, so we can have the CSRF token and validate_on_submit