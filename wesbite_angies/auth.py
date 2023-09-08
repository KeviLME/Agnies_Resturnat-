from flask import Blueprint,render_template, request, flash, redirect, url_for
from email.message import EmailMessage
import ssl
import smtplib
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash 
from . import db #means from __init__.py import db
# from .sender import sender
import stripe
import os


# app.config["STRIPE_PUBLIC_KEY"] = "pk_test_51NnXW1JT2HBC5ySEagq9GCHh3V6V8YJPAyw7RhpxYNsoC2jhevASWQ3MzMGDD21J9crxaZbQs1AtP21KdFtn5r1R00tnT2BuoQ"
# app.config["STRIPE_SECRET_KEY"] = "sk_test_51NnXW1JT2HBC5ySE0rMExL7wYFwRz0a7Ttt20h9s8XZogV8jtvZSCwhRaJzxxUoEhD5FgDpUwYHw9TThDqdtkagw00fQZY8cx5"

# stripe.api_key = app.config["STRIPE_SECRET_KEY"]




class send_email():

        def __init__(self, email_sender, Email_password, Email_reciver, Subject, Body):
            self.email_sender = email_sender
            self.Email_password = Email_password
            self.Email_reciver = Email_reciver
            self.Subject = Subject
            self.Body = Body
        
        def send(self):
            em = EmailMessage()
            em["From"] = self.email_sender
            em["To"] = self.Email_reciver
            em["subject"] = self.Subject
            em.set_content(self.Body)

            context = ssl.create_default_context()

            with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as smtp:
                smtp.login(self.email_sender, self.Email_password)
                smtp.sendmail(self.email_sender, self.Email_reciver, em.as_string())



auth = Blueprint("auth", __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("paswword")

        user = User.query.filter_by(email=email).first()

        if user:
            if check_password_hash(user.password, password):
                flash("Logged in successfully!", category="success")
                return redirect(url_for("views.home"))

            else:
                flash("Incorrect password, try again", category="error")
        else:
            flash("Email does not exist.", category="error")

    return render_template("Login.html")






@auth.route("/logout")
def logout():
    return render_template("tes_logou.html")

@auth.route("/sign-up",methods=["GET","POST"])
def sign_up():
    if request.method == "POST":
        email = request.form.get("email")
        firstName = request.form.get("FirstName")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")
        print(request.form)


        user = User.query.filter_by(email=email).first()

        if user:
            flash("Email already exists.",category="error")

        elif len(email) < 4:
            flash("Email must be greater than 4 characters.",category="error")
        elif len(firstName) < 2:
            flash("Name must be longer than 1 character.",category="error")
        elif password1 != password2:
            flash("Passwords do not match!",category="error")
        elif len(password1) < 7:
            flash("Password must be longer than 6 characters.",category="error")
        else:
            new_user = User(email=email, first_name=firstName, password=generate_password_hash(password1, method='sha256')) #this will store the new user data in teh User Class from the ==Models== folder putting there emai l name and passwoer but using the swcure has mehtod to ranfom encyerp the passowrd 

            db.session.add(new_user)#this will add the new user to the database
            db.session.commit()#this will save teh user in by updataing teh data base with the new user !!
            
            

            flash("Account created!",category="success")

            
            # Mail = send_email(email_sender= "Kevinlookup@gmail.com",Email_password= "kevdetshfttxpddk",Email_reciver= email, Subject= "Sign-up", Body= "Thank you bitch")
            # Mail.send() #this will send the user a email conformtion of there account gettign created 
            

            return redirect(url_for("views.home"))#this will redirect the user to the home page after they have created there account


    return render_template("signup.html")






        

    return render_template("Final_check_out.html")
        
        




    return render_template("Check_out.html")



