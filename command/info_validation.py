import command as cmd
import time
import requests
import aiofiles
import json
import sys
import os
import pwinput as pin
def is_valid_email(email):
   data = {"email":email}
   req = requests.post("https://pychat-api.dipdey.repl.co/email_validation", data=data)
   if req.status_code != 500:
     req = req.json()
     return req["message"]
   else:
     req = requests.post("https://pychat-api.dipdey.repl.co/email_validation", data=data).json()
     data = req["message"]
     return data
def is_valid_username(username):
   data = {"username":username}
   req = requests.post("https://pychat-api.dipdey.repl.co/username_validation", data=data)
   if req.status_code != 500:
     req = req.json()
     return req["message"]
   else:
     req = requests.post("https://pychat-api.dipdey.repl.co/email_validation", data=data).json()
     data = req["message"]
     return data
def login_email_validation(email):
   data = {"email":email}
   req = requests.post("https://pychat-api.dipdey.repl.co/login_email_validation", data=data).json()
   return req["message"]