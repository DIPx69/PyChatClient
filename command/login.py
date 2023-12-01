import command as cmd
import time
import requests
import aiofiles
import json
import sys
import os
import pwinput as pin
def login():
  cmd.typing("[ 1 ] Login\n",0.3)
  cmd.typing("\n[ 2 ] Register\n",0.3)
  cmd.typing("\n\n[ ~ ] Enter : ",0.3)
  ask_login_menu()
def ask_login_menux():
  try:
   menu = int(input(""))
   if menu == 1:
     login_now()
   elif menu == 2:
     cmd.register(1,logo=True)
   else:
     ask_login_menu(1)
  except Exception as e:
   print(e)
   cmd.typing("\n> Invalid Menu Enter Again <",0.3)
   cmd.typing("\n\n[ ~ ] Enter : ",0.3)
   ask_login_menu()
def ask_login_menu():
   menu = int(input(""))
   if menu == 1:
     login_now()
   elif menu == 2:
     cmd.register(1,logo=True)
   else:
     ask_login_menu(1)
def login_now():
  cmd.logo(0.1)
  login_user(1)
def login_user(step,email=None,password=None,logo=None):
  if step == 1:
    cmd.logo(0.1) if logo is True else " "
    cmd.typing("\n[ ~ ] Enter Email: ",0.3)
    email = str(input(""))
    email_ck = cmd.login_email_validation(email)
    if email_ck == "True":
      login_user(2,email=email,logo=True)
    else:
      cmd.typing(f"\n[ ~ ] {email_ck}\n",0.3)
      login_user(1,logo=False)
  if step == 2:
    cmd.typing("\n[ ~ ] Enter Password: ",0.3)
    password = pin.pwinput(prompt='',mask='X')
    login_user(3,email=email,password=password)
  if step == 3:
   account_info = {"email":email,"password":password}
   req = requests.post("https://pychat-api.dipdey.repl.co/login", data=account_info)
   req_json = req.json()
   cmd.typing(f"\n[ ~ ] {req_json['message']}\n",0.3)
   if req.status_code == 200:
     data = {
       "email": email,
       "password": password,
       "username": req_json["username"],
       "verify":True
     }
     with open(".key.json", 'w') as f:
        f.write(json.dumps(data))
     filename = sys.argv[0]
     os.system(f"python {filename}")
   if req.status_code == 401:
     login_user(2,email=email)