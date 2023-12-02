import command as cmd
import time
import requests
import aiofiles
import json
import sys
import os
def user_menu():
   verify_login()
   menus()
def menus():
   cmd.typing(f"\n[ X ] Version {cmd.version}\n",0.1)
   cmd.typing(f"\n[ 1 ] Profile\n",0.1)
   cmd.typing(f"\n[ 2 ] Chat Rooms\n",0.1)
   cmd.typing(f"\n[ 3 ] Create Room\n",0.1)
   cmd.typing(f"\n[ 4 ] Logout\n",0.1)
   cmd.typing("\n\n[ ~ ] Enter : ",0.1)
   ask_menu()
def logout():
  os.system('clear')
  cmd.logo(0.1)
  os.remove(".key.json")
  time.sleep(0.5)
  cmd.typing(f"[ ~ ] Successfully Log Out\n",0.3)
  time.sleep(0.5) 
  cmd.typing(f"\n[ ~ ] Restarting Client\n",0.3)
  time.sleep(0.5)
  filename = sys.argv[0]
  os.system(f"python {filename}")

def ask_menu():
  try:
   menu = int(input(""))
   if menu == 1:
     cmd.profile()
   elif menu == 2:
     cmd.rooms()
   elif menu == 3:
     os.system('clear')
     cmd.logo(0.1)
     cmd.create_room()
   elif menu == 4:
     logout()
   else:
     ask_menu(1)
  except Exception as e:
   cmd.typing("\n - Invalid Menu Enter Again",0.3)
   cmd.typing("\n\n[ ~ ] Enter : ",0.3)
   ask_menu()
def verify_login():
  with open(".key.json","r") as e:
    data = json.load(e)
    email = data["email"]
    password = data["password"]
    verify = data["verify"]
  if verify is False:
   cmd.typing(f"\n[ ~ ] Loging as {email}\n",0.3)
   time.sleep(0.5)
   cmd.typing(f"\n[ ~ ] Verifying Email & Password\n",0.3)
   account_info = {"email":email,"password":password}
   req = requests.post("https://pychat-api.dipdey.repl.co/login_verify", data=account_info)
   req_json = req.json()
   cmd.typing(f"\n[ ~ ] {req_json['message']} \n",0.3)
   if req.status_code == 200:
     data["verify"] = True
     with open("key.json","w") as e:
       json.dump(data,e)
     os.system("clear")
     cmd.logo(0.1)
     user_menu()
   if req.status_code == 401:
     cmd.typing(f"\n[ ~ ] Enter Password : ",0.3)
     password = input(" ")
     data["password"] = password
     with open("key.json","w") as e:
       json.dump(data,e)
     os.system("clear")
     cmd.logo(0.1)
     user_menu()
   if req.status_code == 400:
     time.sleep(0.5)
     cmd.typing(f"\n[ ~ ] Automatic Log Out Activated\n",0.3)
     os.remove("key.json")
     time.sleep(0.5)
     cmd.typing(f"\n[ ~ ] Successfully Logut\n",0.3)
     time.sleep(0.5)
     cmd.typing(f"\n[ ~ ] Restarting Client\n",0.3)
     time.sleep(0.5)
     filename = sys.argv[0]
     os.system(f"python {filename}")