from flask import Flask,render_template
from flask import request
import random, time, requests

from flask_wtf import FlaskForm
from flask_bootstrap import Bootstrap5
from wtforms.validators import DataRequired,Email
from wtforms import StringField, PasswordField,SubmitField,ValidationError,form
# from flask_wtf.csrf import CSRFProtect



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

current_year = time.localtime().tm_year
print(current_year)



app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  # Change to your secret key
bootstrap = Bootstrap5(app)
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
        pass
    # # if request.method == 'POST':
    # #      email = StringField('inputEmail')
    # #      password = PasswordField('inputPassword')
    #     return render_template("home.html",current_year=current_year)
    # else:
    return render_template("login.html",current_year=current_year,form=form)






# to run whithout using cmd >flask --app <filename> run 
# Allows to just use python hello.py
if __name__ == "__main__":
    app.run(debug=True, host="localhost", port="5000")