from flask import Flask,render_template,redirect,url_for, flash, jsonify, request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask import request, session
import random, time, requests,datetime
from datetime import datetime
import sqlite3
from functools import wraps


from flask_wtf import FlaskForm
from flask_bootstrap import Bootstrap5
from wtforms import StringField, PasswordField, SubmitField, ValidationError, Form
from wtforms.validators import DataRequired, Email, InputRequired, Regexp

# from flask_wtf.csrf import CSRFProtect

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float, create_engine

from dotenv import load_dotenv
import os

load_dotenv()

###########################Cognito Config############################
from flask_cognito import CognitoAuth
from flask_cognito import cognito_auth_required, current_user, current_cognito_jwt
import boto3
from botocore.exceptions import ClientError, NoCredentialsError, PartialCredentialsError, EndpointConnectionError

######################## Flask Form ################################
def length(min=-1, max=-1):
    message = 'Must be between %d and %d characters long.' % (min, max)

    def _length(form, field):
        l = field.data and len(field.data) or 0
        if l < min or max != -1 and l > max:
            raise ValidationError(message)

    return _length


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[Email()])
    password = PasswordField('Password', validators=[DataRequired(), length(min=8,max=50)])
    submit = SubmitField('Log In')

class SignupForm(FlaskForm):
    #Need to add validator to check if there use user with similar username or email.
    username = StringField(
        validators=[
            InputRequired(),
            length(3, 20),
            Regexp(
                "^[A-Za-z][A-Za-z0-9_.]*$",
                0,
                "Usernames must have only letters, " "numbers, dots or underscores",
            ),
        ]
    )  
    email = StringField('Email', validators=[Email()])
    password = PasswordField('Password', validators=[DataRequired(), length(min=8,max=50)])
    submit = SubmitField('Sign Up')

class PostForm(FlaskForm):
    poster = StringField('Poster', validators=[DataRequired()])
    topic = StringField('Topic', validators=[DataRequired()])
    user_post = StringField("What's on your mind!",validators=[DataRequired(), length(min=1,max=500)])
    submit = SubmitField('Post')

class NewPassword(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired(), length(min=8,max=50)])
    submit = SubmitField('Sign Up')

current_year = time.localtime().tm_year
print(current_year)

class ConfirmationForm(FlaskForm):
    verification_code = StringField('Verification Code', validators=[DataRequired()])
    submit = SubmitField('Verify Account')

# As of flask-sqlalchemy version 3.1, you need to pass a subclass of DeclarativeBase to the constructor of the database.
class Base(DeclarativeBase):
    pass

#################################### Flask APP #########################################
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  # Change to your secret key

# This is the SQLite URI format. `./example.db` specifies the path to your database file.
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///blog_db.db"
db = SQLAlchemy(model_class=Base)
db.init_app(app)


app.config['JWT_SECRET_KEY'] = 'your_secret_key'
jwt = JWTManager(app)

bootstrap = Bootstrap5(app)
    # csrf = CSRFProtect(app)  # might not be needed, look into documentation
app.config['COGNITO_REGION'] = os.getenv('COGNITO_REGION')  # e.g., us-east-1
app.config['COGNITO_USERPOOL_ID'] = os.getenv('USER_POOL_ID')
app.config['COGNITO_APP_CLIENT_ID'] = os.getenv('APP_CLIENT_ID')
app.config['COGNITO_CHECK_TOKEN_EXPIRATION'] = False  # Set as per your preference


cognito = CognitoAuth(app)


# AWS Cognito credentials
USER_POOL_ID = os.getenv('USER_POOL_ID')
CLIENT_ID = os.getenv('APP_CLIENT_ID')
REGION = os.getenv('COGNITO_REGION')

client = boto3.client('cognito-idp', region_name=REGION)

def sign_in(email, password):
    try:
        resp = client.initiate_auth(
            ClientId=CLIENT_ID,
            AuthFlow='USER_PASSWORD_AUTH',
            AuthParameters={
                'USERNAME': email,
                'PASSWORD': password
            }
        )
        return resp
    except ClientError as e:
        # Specific error handling based on error code
        error_code = e.response['Error']['Code']
        if error_code in ['NotAuthorizedException', 'UserNotFoundException']:
            print(f"Authentication failed: {e.response['Error']['Message']}")
        else:
            print(f"Unexpected error: {e.response['Error']['Message']}")
        return None
    except (NoCredentialsError, PartialCredentialsError):
        print("Credentials are not available or incomplete.")
        return None
    except EndpointConnectionError:
        print("Network issues, unable to connect to Cognito endpoint.")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")
        return None
    
def respond_to_new_password_challenge(username, session, new_password):
    try:
        response = client.respond_to_auth_challenge(
            ClientId=CLIENT_ID,
            ChallengeName='NEW_PASSWORD_REQUIRED',
            Session=session,
            ChallengeResponses={
                'USERNAME': username,
                'NEW_PASSWORD': new_password,
            }
        )
        return response
    except ClientError as e:
        error_code = e.response['Error']['Code']
        if error_code == 'ExpiredCodeException':
            print("Session token expired. Please re-authenticate.")
        else:
            print(f"Error during password reset: {e.response['Error']['Message']}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred during password challenge: {str(e)}")
        return None


# for login - in progress
def cognito_login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Check if the session contains Cognito tokens
        access_token = session.get('access_token')
        print(access_token)
        if not access_token:
            # No token, redirect to login
            return redirect(url_for('login'))

        # Create a Cognito identity provider client
        client = boto3.client('cognito-idp', region_name=REGION)
        
        try:
            # Attempt to get user data to validate the current token
            response = client.get_user(
                AccessToken=access_token
            )
            # Optionally, refresh token logic here if the token is about to expire
        except client.exceptions.NotAuthorizedException:
            # Token is not valid or expired, redirect to login
            return redirect(url_for('login'))
        except client.exceptions.UserNotFoundException:
            # User does not exist, handle accordingly
            return redirect(url_for('login'))
        except Exception as e:
            # Handle other possible exceptions
            print(f"Error verifying Cognito access token: {str(e)}")
            return redirect(url_for('login'))
        
        # If everything is fine, proceed to the protected route
        return f(*args, **kwargs)

    return decorated_function

################################### Database ###############################
posts = []

class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    password_salt = db.Column(db.String(128), nullable=False)

    # Relationship to UserPost
    posts = db.relationship('UserPost', backref='author', lazy='dynamic')

    def __repr__(self):
        return '<User %r>' % self.username

class UserPost(db.Model):
    post_id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    

    def __repr__(self):
        return '<Post %r>' % self.content
    
class Contact_message(db.Model):
    contact_msg_id = db.Column(db.Integer, primary_key=True)
    sender_name = db.Column(db.Text, nullable=False)
    sender_email = db.Column(db.Text, nullable=False)
    message = db.Column(db.Text, nullable=False)
    message_recieve_time = db.Column(db.DateTime, default=datetime.utcnow())
    

    def __repr__(self):
        return '<contact %r>' % self.content

with app.app_context():
    db.create_all() 

################################### ROUTES  ################################
    


@app.route("/")
def home():
    return render_template("home.html",posts=posts)

@cognito_auth_required
@app.route('/secure_area')
def secure_area():
    return 'yes You are logged In'


@app.route("/about")
def about():
    return render_template("about.html")

@cognito_auth_required
@app.route("/contact",methods=[ "GET","POST"])
def contact():
    if request.method == 'POST':
        sender_name = request.form['name']
        sender_email = request.form['email']
        message = request.form['message']
        
        new_message = Contact_message(message=message, sender_email=sender_email, sender_name=sender_name)
        db.session.add(new_message)
        db.session.commit()
        with open('messages.txt', 'a') as file:  # Open the text file in append mode
            file.write(f"from:{sender_name}\nemail:{sender_email}\n{message}\n\n")  # Write the message to the file with a newline
        return render_template("home.html")
    else:
        return render_template("contact.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        print("Email:", email)
        print("Password:", password)
        auth_response = sign_in(email, password)
        print("auth response: ", auth_response)
        if auth_response and 'ChallengeName' in auth_response and auth_response['ChallengeName'] == 'NEW_PASSWORD_REQUIRED':
            session['username'] = email  # Store username temporarily
            session['session'] = auth_response['Session']  # Store the session token temporarily
            return redirect(url_for('new_password'))  # Redirect to the new password page
        if auth_response and 'AuthenticationResult' in auth_response:
            session['email'] = email
            session['access_token'] = auth_response['AuthenticationResult']['AccessToken']
            return redirect(url_for('home'))
        else:
            print("AWS Cognito Error:", ClientError)
            return 'Login failed', 401
    return render_template('login.html',form=form)

@app.route('/new_password', methods=['GET', 'POST'])
def new_password():
    if request.method == 'POST':
        new_password = request.form['new_password']
        username = session.get('username')
        session_token = session.get('session')
        response = respond_to_new_password_challenge(username, session_token, new_password)
        if response and 'AuthenticationResult' in response:
            return redirect(url_for('home'))
        else:
            return 'Failed to update password', 400
    return render_template('new_password.html')  # Render a template for new password input

@cognito_auth_required
@app.route('/logout')
def logout():
    session.pop('email', None)
    session.pop('access_token', None)
    return redirect(url_for('home'))


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        session['email'] = email
        try:
            response = client.sign_up(
                ClientId=CLIENT_ID,
                Username=email,  # Typically, the email is used as the username
                Password=password,
                UserAttributes=[
                    {
                        'Name': 'email',
                        'Value': email
                    },
                    {
                        'Name': 'preferred_username',
                        'Value': username
                    }
                ]
            )
            flash('Signup successful! Please check your email to confirm your account.', 'success')
            return redirect(url_for('verify_account'))
        except client.exceptions.UsernameExistsException:
            flash('This email already exists.', 'error')
        except Exception as e:
            flash('Failed to sign up due to an error: {}'.format(e), 'error')

    return render_template('signup.html', form=form)

@app.route('/verify', methods=['GET', 'POST'])
def verify_account():
    form = ConfirmationForm()
    if form.validate_on_submit():
        verification_code = form.verification_code.data
        email = session.get('email')  # Assuming you've stored the user's email in the session after signup

        try:
            response = client.confirm_sign_up(
                ClientId=CLIENT_ID,
                Username=email,
                ConfirmationCode=verification_code,
            )
            flash('Account verified successfully! You can now log in.', 'success')
            return redirect(url_for('login'))
        except client.exceptions.UserNotFoundException:
            flash('User not found.', 'error')
        except client.exceptions.CodeMismatchException:
            flash('Invalid verification code provided.', 'error')
        except client.exceptions.NotAuthorizedException:
            flash('User is already confirmed.', 'info')
        except Exception as e:
            flash('Failed to verify account due to an error: {}'.format(e), 'error')

    return render_template('verify.html', form=form)


@cognito_auth_required
@app.route("/post",methods=[ "GET","POST"] )
def post():
    form = PostForm()
    if form.validate_on_submit():
        post_data = {
            "poster": form.poster.data,
            "topic": form.topic.data,
            "post_date": datetime.today(),
            "user_post": form.user_post.data 
        }
        posts.append(post_data)
        print(post_data)
        return redirect(url_for('home'))
    else:
        return render_template("post.html",form=form)
    

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port="5000")