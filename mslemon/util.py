#!/usr/bin/env python
import smtplib
from email.MIMEText import MIMEText

def make_email_message(subject, message, sender, receiver):
    msg = MIMEText(message)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = receiver
    return msg

def send_email_through_smtp_server(settings, message, sender, receiver):
    prefix = 'mslemon.smtp.'
    server = settings[prefix + 'server']
    port = int(settings[prefix + 'port'])
    login = settings[prefix + 'login']
    password = settings[prefix + 'password']
    server = smtplib.SMTP(server, port)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(login, password)
    msg = message.as_string()
    server.sendmail(sender, receiver, msg)
    server.close()

            
if __name__ == "__main__":
    subject = "test oneway.mailer.py"
    message = "This is another test.\nOneway.\n"
    sender = "oneway@littledebian.org"
    receiver = "joseph.rawson.works@littledebian.org"
    email = make_email_message(subject, message, sender, receiver)
    send_email_through_littledebian(email, sender, receiver)
    
    

        
    

