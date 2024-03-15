from flask import Flask,render_template
from flask import request
import random, time, requests

from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from wtforms import StringField, PasswordField,SubmitField
# from flask_wtf.csrf import CSRFProtect



class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')

current_year = time.localtime().tm_year
print(current_year)


app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  # Change to your secret key
# csrf = CSRFProtect(app)  # might not be needed, look into documentation


@app.route("/")
def home():
    return render_template("home.html",current_year=current_year)

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
        
    # if request.method == 'POST':
    #      email = StringField('inputEmail')
    #      password = PasswordField('inputPassword')
        return render_template("home.html",current_year=current_year)
    else:
        return render_template("login.html",current_year=current_year,form=form)






# to run whithout using cmd >flask --app <filename> run 
# Allows to just use python hello.py
if __name__ == "__main__":
    app.run(debug=True, host="localhost", port="5000")