from email.message import EmailMessage
import ssl
import smtplib
from flask import Blueprint,render_template, request

sender = Blueprint("sender", __name__)



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




