#!/usr/bin/env python
# coding: utf-8

# In[24]:


import imaplib
import email
from email.header import decode_header
import pandas as pd
import numpy as np


# In[25]:


username="User Mail"
app_password="User Password"
gmail_host= 'imap.gmail.com'


# In[26]:


mail=imaplib.IMAP4_SSL(gmail_host)


# In[27]:


mail.login(username, app_password)


# In[28]:


#mail.select(mailbox='INBOX') #Access to inbox
res, messages = mail.select('"[Gmail]/Sent Mail"')  #Acess to sent emails
messages = int(messages[0])
n = 9


# In[29]:


res


# In[38]:


lis_subj=[]
lis_from=[]
for i in range(messages, messages - n, -1):
    res, msg = mail.fetch(str(i), "(RFC822)")     
    for response in msg:
        if isinstance(response, tuple):
            msg = email.message_from_bytes(response[1])
              
            # getting the sender's mail id
            From = msg["From"]
            lis_from.append(msg["From"])
            # getting the subject of the sent mail
            subject = msg["Subject"]
            lis_subj.append(msg["Subject"])
            # printing the details
            print("From : ", From)
            print("Subject : ", subject)


# In[37]:


lis_subj=pd.DataFrame(lis_subj)
lis_subj.rename(columns = {0:'Subject'}, inplace = True)
lis_subj


# In[32]:


lis_from=pd.DataFrame(lis_from)
lis_from.rename(columns={0:'From'}, inplace = True)
lis_from


# In[33]:


result = pd.concat([lis_from, lis_subj],axis = 1, join = 'outer', ignore_index=False, sort=False)
result


# In[34]:


body_mes=[]
for i in range(messages, messages-n, -1):
    # fetch the email message by ID
    res, msg = mail.fetch(str(i), "(RFC822)")
    for response in msg:
        if isinstance(response, tuple):
            # parse a bytes email into a message object
            msg = email.message_from_bytes(response[1])
            # decode the email subject
            subject, encoding = decode_header(msg["Subject"])[0]
            if isinstance(subject, bytes):
                # if it's a bytes, decode to str
                subject = subject.decode(encoding)
            # decode email sender
            From, encoding = decode_header(msg.get("From"))[0]
            if isinstance(From, bytes):
                From = From.decode(encoding)
            print("Subject:", subject)
            print("From:", From)
             # if the email message is multipart
            if msg.is_multipart():
                # iterate over email parts
                for part in msg.walk():
                    # extract content type of email
                    content_type = part.get_content_type()
                    content_disposition = str(part.get("Content-Disposition"))
                    try:
                        # get the email body
                        body = part.get_payload(decode=True).decode()
                    except:
                        pass
                    if content_type == "text/plain" and "attachment" not in content_disposition:
                        # print text/plain emails and skip attachments
                        print(body)
                    elif "attachment" in content_disposition:
                        # download attachment
                        filename = part.get_filename()
                        if filename:
                            folder_name = clean(subject)
                            if not os.path.isdir(folder_name):
                                # make a folder for this email (named after the subject)
                                os.mkdir(folder_name)
                            filepath = os.path.join(folder_name, filename)
                            # download attachment and save it
                            open(filepath, "wb").write(part.get_payload(decode=True))
            else:
                # extract content type of email
                content_type = msg.get_content_type()
                # get the email body
                body = msg.get_payload(decode=True).decode()
                if content_type == "text/plain":
                    # print only text email parts
                    body_mes.append(int(body))
                    print(body)


# In[35]:


body_mes=pd.DataFrame(body_mes)
body_mes.rename(columns = {0:'Body'}, inplace = True)


# In[36]:


result1 = pd.concat([result, body_mes],axis = 1, join = 'outer', ignore_index=False, sort=False)
result1

