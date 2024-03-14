from flask import Flask,render_template
from flask import request
import random, time, requests

current_year = time.localtime().tm_year
print(current_year)


app = Flask(__name__)

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


@app.route("/login",methods=[ "GET","POST"])
def login():
    return render_template("login.html",current_year=current_year)






# to run whithout using cmd >flask --app <filename> run 
# Allows to just use python hello.py
if __name__ == "__main__":
    app.run(debug=True, host="localhost", port="5000")