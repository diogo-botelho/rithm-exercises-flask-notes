from flask import Flask, request, redirect, render_template, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from forms import RegisterUserForm, LoginForm

from models import db, connect_db, User

app = Flask(__name__)

app.config['SECRET_KEY'] = "secret"

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///notes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()

@app.get('/')
def show_homepage():
    """Show homepage."""

    return redirect('/register')

@app.route('/register', methods=['POST','GET'])
def create_user():
    """Show form. Create new user on valid form submission.""" 

    form = RegisterUserForm()

    if form.validate_on_submit():
        username = form.username.data
        password =form.password.data
        email = form.email.data
        first_name =form.first_name.data
        last_name = form.last_name.data

        error_messages = check_unique_inputs(username,email)
        if error_messages:
            breakpoint()
            for message in error_messages:
                flash(message)

            return render_template('register-user.html',form=form)

        else:
            breakpoint()
            new_user = User.register(
                username=username,
                password=password,
                email=email,
                first_name=first_name,
                last_name=last_name
                )
            breakpoint()
            db.session.add(new_user)
            db.session.commit()
            session["username"] = username
            breakpoint()
            return redirect('/secret')

        breakpoint()
    else:
        return render_template('register-user.html',form=form)

@app.route('/login', methods=['GET','POST'])
def login():
    """Show login form. If form values are valid and the credentials are correct,
    redirect to /secret"""

    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.check_login_credentials(username, password)

        if not user:
            flash('Invalid login credentials')
            return render_template('login.html',form=form)
        else:
            session["username"] = username
            return redirect('/secret')

@app.get('/secret')
def show_secret():
    """If user is logged in, render secret.html. If not, redirect to homepage"""

    if "username" not in session:
        flash("You must be logged in to view!")
        return redirect("/")

    else:
        return render_template("secret.html")


def check_unique_inputs(username, email):
    """Check if username and email already exist in data.
    Return a list of messages with each input that is not unique."""
    existing_user = User.query.filter_by(username=username).one_or_none()

    error_messages = []
    
    if existing_user:
        error_messages.append(f'Username {username} already used. Please provide a different username')
    
    breakpoint()
    existing_email = User.query.filter(User.email == email).one_or_none()

    if existing_email:
        error_messages.append(flash(f'Email {email} already used. Please provide a different email'))

    breakpoint()
    return error_messages
