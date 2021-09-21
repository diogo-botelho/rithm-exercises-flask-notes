from flask import Flask, request, redirect, render_template, jsonify 
from flask_debugtoolbar import 

from models import db, connect_db, User
from forms import #stuff

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///notes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)

@app.get('/')
def show_homepage():
    """Show homepage."""

    return redirect('/register')

@app.route('/register', method=['POST','GET'])
def create_user():
    """Show form. Create new user on valid form submission.""" 

    form = RegisterUserForm()

    if validade_on_submit():
        username = form.username.data
        password =form.password.data
        email = form.email.data
        first_name =form.first_name.data
        last_name = form.last_name.data

        error_messages = check_unique_inputs(username,email)

        if error_messages not False: 
            for message in error_messages:
                flash(message)

            return render_template('register-user.html',form=form)

        else:
            User.register(
                username=username,
                password=password,
                email=email,
                first_name=first_name,
                last_name=last_name
                )

            db.session.commit()

            return redirect('/secret')

    else:
        return render_template('register-user.html',form=form)

def check_unique_inputs(username, email):
    """Check if username and email already exist in data.
    Return a list of messages with each input that is not unique."""

    existing_user = User.query.get(username,None)

    error_messages = []
    
    if existing_user:
        error_messages.append(f'Username {username} already used.
        Please provide a different username')
    
    existing_email = User.query.filter(User.email == email)

    if existing_email:
        error_messages.append(flash(f'Email {email} already used.
        Please provide a different email'))

    return error_messages



    

