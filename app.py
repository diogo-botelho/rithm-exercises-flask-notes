from flask import Flask, request, redirect, render_template, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from forms import RegisterUserForm, LoginForm

from models import db, connect_db, User

app = Flask(__name__)

app.config['SECRET_KEY'] = "secret" #Code Review = get into habit to using the .env file - fine here but good to build the habit

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///notes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()

@app.get('/')
def show_homepage():
    """Check if user already logged in. If yes, redirect to user details page.
    If not, redirect to register page."""

    if "username" not in session:
        return redirect('/register')
    else:
        username = session["username"]

        return redirect(f'/users/{username}')


@app.route('/register', methods=['POST','GET'])
def create_user(): #CODE REVIEW: Needs better name - eg: show_or_handle_registration()
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
            for message in error_messages:
                flash(message)

            return render_template('register-user.html',form=form)

        else:
            new_user = User.register(
                username=username,
                password=password,
                email=email,
                first_name=first_name,
                last_name=last_name
                )
            #db.session.add(new_user) #This line should be in the User class method register()
            db.session.commit()

            session["username"] = username
            return redirect(f'/users/{username}')

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

        if user:
            session["username"] = username
            return redirect(f'/users/{username}')
        # else:
            # return render_template('login.html',form=form)
        flash('Invalid login credentials')
    
    return render_template('login.html',form=form)

@app.get('/users/<username>')
def show_user_page(username):
    """If user is logged in, render secret.html. If not, redirect to homepage"""

    if session.get("username") != username:
        flash("You must be logged in to view!")
        return redirect("/")

    else: #Code Review: Probably don't need the else. Doesn't hurt to keep it in
        user = User.query.get(username) #Code Review: get_or_404

        return render_template("user-page.html",
            user=user)


@app.post('/logout') #Code Review: For logging out, we should have a very simple WTForm just to have the CSRF token.
def logout():
    """Log out user. Delete user session and redirect to homepage."""
    
    del session["username"]

    return redirect('/')


###########################################Auxiliary functions##########

#CODE REVIEW: This would be a great method to have as a static method in the User class
def check_unique_inputs(username, email):
    """Check if username and email already exist in data.
    Return a list of messages with each input that is not unique."""
    existing_user = User.query.filter_by(username=username).one_or_none()

    error_messages = []
    
    if existing_user:
        error_messages.append(f'Username {username} already used. Please provide a different username')
    
    existing_email = User.query.filter(User.email == email).one_or_none()

    if existing_email:
        error_messages.append(flash(f'Email {email} already used. Please provide a different email'))

    return error_messages