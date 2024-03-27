from flask import Flask,render_template,redirect,url_for
from flask import request
import random, time, requests
from datetime import date
import sqlite3

from flask_wtf import FlaskForm
from flask_bootstrap import Bootstrap5
from wtforms.validators import DataRequired,Email
from wtforms import StringField, PasswordField,SubmitField,ValidationError,form
# from flask_wtf.csrf import CSRFProtect

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float, create_engine


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
    username = StringField('Email', validators=[DataRequired()])  
    email = StringField('Email', validators=[Email()])
    password = PasswordField('Password', validators=[DataRequired(), length(min=8,max=50)])
    submit = SubmitField('Sign Up')


class PostForm(FlaskForm):
    poster = StringField('Poster', validators=[DataRequired()])
    topic = StringField('Topic', validators=[DataRequired()])
    user_post = StringField("What's on your mind!",validators=[DataRequired(), length(min=1,max=500)])
    submit = SubmitField('Post')

current_year = time.localtime().tm_year
print(current_year)




#################################### Flask APP #########################################
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  # Change to your secret key
# This is the SQLite URI format. `./example.db` specifies the path to your database file.
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./example.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
bootstrap = Bootstrap5(app)
    # csrf = CSRFProtect(app)  # might not be needed, look into documentation


################################### Database ###############################
posts = []

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    password_salt = db.Column(db.String(128), nullable=False)

    # Relationship to UserPost
    posts = db.relationship('UserPost', backref='author', lazy='dynamic')

    def __repr__(self):
        return '<User %r>' % self.username

class UserPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return '<Post %r>' % self.content
    

################################### ROUTES  ################################
    
@app.before_first_request
def create_tables():
    db.create_all()

@app.route("/")
def home():
    return render_template("home.html",current_year=current_year,posts=posts)

@app.route("/about")
def about():
    return render_template("about.html",current_year=current_year)


@app.route("/contact",methods=[ "GET","POST"])
def contact():
    if request.method == 'POST':
        sender_name = request.form['name']
        sender_email = request.form['email']
        message = request.form['message']
        with open('messages.txt', 'a') as file:  # Open the text file in append mode
            file.write(f"from:{sender_name}\nemail:{sender_email}\n{message}\n\n")  # Write the message to the file with a newline
        return render_template("home.html",current_year=current_year)
    else:
        return render_template("contact.html",current_year=current_year)


@app.route("/login",methods=[ "GET","POST"] )
def login():
    form = LoginForm()
    if form.validate_on_submit():
        pass
    return render_template("login.html",current_year=current_year,form=form)

@app.route("/signup",methods=[ "GET","POST"] )
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        password_hash = password #add hash process here 
        password_salt = "P@ssW0RdS@1t" # generate password salt here 
        new_user = User(username=username, password_hash=password_hash, password_salt=password_salt)
        db.session.add(new_user)
        db.session.commit()
    return render_template("signup.html",current_year=current_year,form=form)


@app.route("/post",methods=[ "GET","POST"] )
def post():
    form = PostForm()
    if form.validate_on_submit():
        post_data = {
            "poster": form.poster.data,
            "topic": form.topic.data,
            "post_date": date.today(),
            "user_post": form.user_post.data 
        }
        posts.append(post_data)
        print(post_data)
        return redirect(url_for('home'))
    else:
        return render_template("post.html",current_year=current_year,form=form)


if __name__ == "__main__":
    app.run(debug=True, host="localhost", port="5000")