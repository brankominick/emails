import os
import sys
import smtplib
from email.message import EmailMessage

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath("config.py"))))
from config import *

with open("message.txt") as fp:
    msg = EmailMessage()
    msg.set_content(fp.read())

msg['Subject'] = "Test email"
msg['From'] = MY_EMAIL
msg['To'] = 'kominick@bc.edu'

smObj = smtplib.SMTP('smtp.gmail.com', 587)
smObj.connect('smtp.gmail.com', 587)
smObj.ehlo()
smObj.starttls()
smObj.ehlo()
smObj.login(MY_EMAIL, MY_PASSWORD)

smObj.send_message(msg)
smObj.quit()
