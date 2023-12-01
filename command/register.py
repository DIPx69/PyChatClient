import command as cmd
import time
import requests
import aiofiles
import json
import sys
import os
import pwinput as pin
def register(step,email=None,username=None,password=None,logo=None):
  if step == 1:
   cmd.logo(0.1) if logo is True else " "
   cmd.typing("\n[ ~ ] Enter Email: ",0.3)
   email = str(input(""))
   email_ck = cmd.is_valid_email(email)
   if email_ck == "True":
     register(2,email=email,logo=True)
   else:
     cmd.typing(f"\n[ ~ ] {email_ck}\n",0.3)
     register(1,logo=False)
  if step == 2:
   cmd.typing("\n[ ~ ] Enter Username: ",0.3)
   username = str(input(""))
   if cmd.is_valid_username(username) == "True":
     register(3,email=email,username=username,logo=True)
   else:
     cmd.typing(f"\n[ ~ ] {cmd.is_valid_username(username)}\n",0.3)
     register(2,email=email,logo=False)
  if step == 3:
   cmd.typing("\n[ ~ ] Enter Password: ",0.3)
   password = pin.pwinput(prompt='',mask='X')
   register(4,email=email,username=username,password=password)
  if step == 4:
   account_info = {"email":email,"username":username,"password":password}
   cmd.typing("\n[ ~ ] Registering Account\n",0.3)
   req = requests.post("https://pychat-api.dipdey.repl.co/register", data=account_info)
   code = req.status_code
   req_json = req.json()
  try:
    if code == 200:
     data = {
       "email": email,
       "password": password,
       "username": username,
       "verify": True
     }
     with open(".key.json", 'w') as f:
       f.write(json.dumps(data))
     cmd.typing(f"\n[ ~ ] {req_json['message']}\n",0.3)
     time.sleep(0.5)
     filename = sys.argv[0]
     os.system(f"python {filename}")
  except:
    pass