import command as cmd
import time
import requests
import aiofiles
import json
import sys
import os
def create_room():
  cmd.typing(f"\n[ ~ ] Enter Room Name: ",0.1)
  room_name = input("")
  if room_name == "":
    os.system('clear')
    cmd.logo(0.1)
    cmd.menus()
  with open(".key.json","r") as e:
     user = json.load(e)
     password = user["password"]
     email = user["email"]
  info = {"room_name":room_name,"email":email,"key":password}
  req = requests.post("https://pychat-api.dipdey.repl.co/create",data=info)
  if req.status_code == 200:
   req_json = req.json()
   cmd.typing(f"\n[ ~ ] {req_json['message']} \n",0.3) 
   time.sleep(1)
   cmd.rooms()
  elif req.status_code == 401:
   req_json = req.json()
   cmd.typing(f"\n[ ~ ] {req_json['message']} \n",0.3) 
   time.sleep(1)
   cmd.logout()
  elif req.status_code == 402:
   req_json = req.json()
   cmd.typing(f"\n[ ~ ] {req_json['message']} \n",0.3) 
   create_room()