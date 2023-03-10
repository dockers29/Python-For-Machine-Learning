#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
import smtplib
#with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
    #smtp.ehlo()
    #smtp.starttls()
    #smtp.ehlo()
server=smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
import pandas as pd
import random as rd


# In[2]:


EMAIL_ADDRESS = os.environ.get('User Email')
EMAIL_PASSWORD = os.environ.get('User Password') 


# In[3]:


server.login(EMAIL_ADDRES, EMAIL_PASSWORD)


# In[4]:


numbers=rd.randint(1,5)
subject="#" + str(numbers)
body=rd.randint(100,200)
msg=f'Subject: {subject}\n\n{body}'


# In[5]:


server.sendmail(EMAIL_ADDRES, 'Email Destination Address', msg)


# In[6]:


df=pd.read_csv('cs-test.txt') #This is the file that we will be looking at
df


# In[7]:


Debt = df.DebtRatio
if Debt[1] > 0.5:
           server.sendmail(EMAIL_ADDRES, 'Email Destination Address', msg) #Send email on condition

