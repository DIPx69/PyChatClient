import command as cmd
import time
import requests
import aiofiles
import json
import sys
import os
def profile():
  with open(".key.json","r") as e:
    data = json.load(e)
    email = data["email"]
    password = data["password"]
    username = data["username"]
  account_info = {"email":email,"password":password}
  cmd.logo(0.1)
  cmd.typing(f"\n[ ~ ] Verifying Password\n",0.3)
  req = requests.post("https://pychat-api.dipdey.repl.co/login_verify", data=account_info)
  req_json = req.json()
  cmd.typing(f"\n[ ~ ] {req_json['message']} \n",0.3)
  time.sleep(0.5)
  if req.status_code == 200:
    os.system('clear')
    cmd.logo(0.1)
    cmd.typing(f"\n[ ~ ] Username: {username}\n",0.3)
    cmd.typing(f"\n[ ~ ] Email: {email}\n",0.3)
    cmd.typing(f"\n[ ~ ] Password: {password} [Locally Stored]\n",0.3)
    cmd.typing(f"\n\n[ X ] Press Enter To Back: ",0.3)
    input("")
    os.system("clear")
    cmd.logo(0.1)
    cmd.menus()
  if req.status_code == 401:
     time.sleep(0.5)
     cmd.typing(f"\n[ ~ ] Automatic Log Out Activated\n",0.3)
     os.remove(".key.json")
     time.sleep(0.5)
     cmd.typing(f"\n[ ~ ] Successfully Logut\n",0.3)
     time.sleep(0.5)
     cmd.typing(f"\n[ ~ ] Restarting Client\n",0.3)
     time.sleep(0.5)
     filename = sys.argv[0]
     os.system(f"python {filename}")