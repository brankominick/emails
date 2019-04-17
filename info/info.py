import os
import sys

import imaplib
import email
import json

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath("config.py"))))
from config import *



####################FUNCTION DEFINITIONS##############################

def formatDate(date):
    print(date)
    if ',' in date:
        date = date.split(',')[1].split(' ')[1:5]
        time = date[3]
        date = date[0] + '-' + date[1] + '-' + date[2]
        print(date)
    else:
        date = date.split(' ')[:4]
        time = date[3]
        date = date[0] + '-' + date[1] + '-' + date[2]
        print(date)
        
    return date, time
    
def getListOfEmails(Imap_Inbox):  
    list_of_emails = []  
    result, data = mail.uid('search', None, 'ALL')
    if result == "OK":
        for i in data[0].split():            
            result, email_data = mail.uid('fetch', i, '(RFC822)')
            if result == 'OK':
                message = email.message_from_bytes(email_data[0][1])
                date, time = formatDate(message['Date'])
                
                if message['Subject'] != None:
                    try:
                        if isinstance(message['Subject'],str):
                            subject = message['Subject']
                        else:
                            subject = 'Error getting subject'
                        if message.is_multipart():
                            for part in message.walk():
                                if part.get_content_type() == 'text/plain':
                                    #print(part.get_payload(decode=True))
                                    if part.get_payload() != None:
                                        body = part.get_payload(decode=True).decode('utf-8','ignore')
                                        this_email = {'From' : message['From'], 'Subject' : subject, 'Date' : date, 'Time' : time, 'Body' : body}
                                        list_of_emails.append(this_email)
                                    else:
                                        this_email = {'From' : message['From'], 'Subject' : subject, 'Date' : date, 'Time' : time, 'Body' : 'None'}
                                        list_of_emails.append(this_email)                    
                                    
                        else:
                            body = message.get_payload(decode=True).decode('utf-8','ignore')
                            this_email = {'From' : message['From'], 'Subject' : subject, 'Date' : date, 'Time' : time, 'Body' : body}
                            list_of_emails.append(this_email)

                    except:
                        pass 
                    
                else:
                    try:
                        #print('\nFrom:' + message['From'] + '\nSubject: None' + '\nDate: ' + message['Date'])
                        if message.is_multipart():
                            for part in message.walk():
                                if part.get_content_type() == 'text/plain':
                                    #print(part.get_payload(decode=True))
                                    if part.get_payload() != None:
                                        body = part.get_payload(decode=True).decode('utf-8','ignore')
                                        this_email = {'From' : message['From'], 'Subject' : 'None', 'Date' : date, 'Time' : time, 'Body' : body}
                                        list_of_emails.append(this_email)
                                    else:
                                        this_email = {'From' : message['From'], 'Subject' : 'None', 'Date' : date, 'Time' : time, 'Body' : 'None'}
                                        print("This email: ", this_email)
                                        list_of_emails.append(this_email)                    
                        else:
                            if message.get_payload() != None:
                                body = message.get_payload(decode=True).decode('utf-8','ignore')
                                this_email = {'From' : message['From'], 'Subject' : 'None', 'Date' : date, 'Time' : time, 'Body' : body}
                                list_of_emails.append(this_email)
                            else:
                                this_email = {'From' : message['From'], 'Subject' : 'None', 'Date' : date, 'Time' : time, 'Body' : 'None'}
                                list_of_emails.append(this_email)
                    except:
                        pass
                    
    return list_of_emails
    

    #############################################MAIN###################

mail = imaplib.IMAP4_SSL('imap.gmail.com')
mail.login(MY_EMAIL, MY_PASSWORD)
mail.select("INBOX")



if os.stat("emails.json").st_size != 0:
    with open('emails.json', 'r+') as file:
        data = json.load(file)
    
    print("number of emails: ",len(data))
    last_email = data[-1]
    last_date = last_email['Date']
    
    print(last_date)


else:
    list_of_emails = getListOfEmails(mail)

    with open('emails.json', 'w') as outfile:
        json.dump(list_of_emails, outfile)
    


mail.close()
mail.logout()





