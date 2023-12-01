import command as cmd
import time
import requests
import aiofiles
import json
import sys
import os
import threading
from datetime import datetime,timedelta
last_response = None
run = True
room_info = None
def refresh_chat(room_id):
   global last_response
   global run
   global room_info
   with open(".key.json","r") as e:
    data = json.load(e)
    email = data["email"]
   info = {"email":email}
   get_username = requests.post("https://pychat-api.dipdey.repl.co/get_username",data=info)
   room_info = {"id": room_id,"email":email}
   if get_username.status_code == 200:
     get_username_json = get_username.json()
     username = get_username_json["username"]
   elif get_username.status_code == 401:
      cmd.typing(f"\n[ # ] {data['messages']}\n",0.3)
      time.sleep(1)
      cmd.logout()
   while run:
     time.sleep(3)
     req = requests.post("https://pychat-api.dipdey.repl.co/join",data=room_info)
     response = req.json()
     if req.status_code == 200:
       last_message_username = response["messages"]["1"]["name"]
       last_message_timestamp = response["messages"]["1"]["timestamp"]
       if response != last_response and last_message_username != username:
         load_message(room_id,msg=True,data=response)
         cmd.typing(f"[ PY ] Message: ",0)
         last_response = response
     else:
      last_response = None
      break
def rooms():
   os.system("clear")
   cmd.logo(0.1)
   req = requests.get("https://pychat-api.dipdey.repl.co/rooms")
   req_json = req.json()
   rooms = req_json["rooms"]
   for index,room in enumerate(rooms,start=1):
     cmd.typing(f"\n[ {index} ] {room}\n",0.1)
   enter_room(len(rooms))
def enter_room(length):
  global last_response
  global run
  global room_info
  cmd.typing(f"\n[ ~ ] Enter Room ID: ",0.3)
  try:
   room_id = int(input(" "))
  except:
   room_id = ""
   if room_id == "":
     os.system('clear')
     cmd.logo(0.1)
     cmd.menus()
   pass
  cmd.typing(f"\n[ ~ ] Joining...",0.3)
  if room_id <= length:
     with open(".key.json","r") as e:
       data = json.load(e)
     email = data["email"]
     info = {"id": room_id,"email":email}
     req = requests.post("https://pychat-api.dipdey.repl.co/join",data=info)
     if req.status_code == 200:
       last_response = None
       run = True
       room_info = {"id":room_id}
       load_message(room_id,data=req.json())
     else:
       data = req.json()
       message = data["message"]
       error_message = '\b' * 10 + message + '\n'
       cmd.typing(error_message,0.3)
       enter_room(length)
  else:
    error_message = '\b' * 10 + "Invalid Room ID\n"
    cmd.typing(error_message,0.3)
    enter_room(length)
def timestamp2time(timestamp):
  dt = datetime.fromtimestamp(timestamp)
  #timezone = datetime.now(pytz.timezone('UTC')).astimezone().tzinfo
  #timezone = timezone.utcoffset(None).total_seconds() // 3600
  #dhaka_offset = timedelta(hours=timezone)
  #dt_dhaka = dt + dhaka_offset
  formatted_time = dt.strftime('%I:%M%p')
  return formatted_time
def load_message(room_id,data=None,msg=None):
  global last_response
  global run
  if last_response is None:
    run = True
    api_thread = threading.Thread(target=refresh_chat,args=(room_id,))
    api_thread.start()
  if data is None:
    with open(".key.json","r") as e:
     data = json.load(e)
    email = data["email"]
    info = {"id": room_id,"email":email}
    req = requests.post("https://pychat-api.dipdey.repl.co/join",data=info)
    if req.status_code == 200:
       data = req.json()
       print_message(data)
    else:
       data = req.json()
       message = data["message"]
       cmd.typing(f"\n[ ~ ] {message}\n\n",0.3)
  else:
   print_message(data)
  if msg is None:
     enter_message(room_id)
def print_message(data):
  os.system('clear')
  cmd.logo(0)
  cmd.typing(f"[ ~ ] Room Name: {data['room_name']}\n",0)
  cmd.typing(f"\n[ ~ ] Owner : {data['owner']}\n\n",0)
  for key in sorted(data["messages"].keys(), key=int, reverse=True):
   message_data = data["messages"][key]
   cmd.typing(f"{message_data['name']} [{timestamp2time(message_data['timestamp'])}]: {message_data['message']}\n\n",0.00)
def enter_message(room_id):
  global run
  cmd.typing(f"[ PY ] Message: ",0.3)
  your_message = input("")
  if your_message in ["/back","back","1"," "]:
     run = False
     os.system("clear")
     cmd.logo(0.1)
     cmd.menus()
  elif your_message in ["/refresh","/re","re","0",""]:
     load_message(room_id)
  else:
    with open(".key.json","r") as e:
      user = json.load(e)
      password = user["password"]
      email = user["email"]
    send_message(room_id,send_message={"email":email,"message":your_message,"key":password})
def send_message(room_id,send_message=None):
   email = send_message["email"]
   message = send_message["message"]
   password = send_message["key"]
   new_message ={"email":email,"message":message,"id":room_id,"key":password}
   req = requests.post("https://pychat-api.dipdey.repl.co/send_message",data=new_message)
   if req.status_code == 200:
     data = req.json()
     message_data = data["messages"]["1"]
     print("\x1b[1A\x1b[2K", end='', flush=True)
     cmd.typing(f"{message_data['name']} [{timestamp2time(message_data['timestamp'])}]: {message_data['message']}\n\n",0.00)
     enter_message(room_id)
   elif req.status_code == 402:
     data = req.json()
     cmd.typing(f"\n[ ~ ] {data['message']}",0.3)
     time.sleep(1)
     load_message(room_id)
   elif req.status_code == 404:
     load_message(room_id)
   elif req.status_code == 401:
     data = req.json()
     cmd.typing(f"\n[ ~ ] {data['message']}",0.3)
     time.sleep(1)
     cmd.logout()
   elif req.status_code == 400:
     data  = req.json()
     cmd.typing(f"\n[ ~ ] {data['message']}",0.3)
     time.sleep(1)
     cmd.logout()
def joined_room(room_id):
  global last_response
  if last_response is None:
    api_thread = threading.Thread(target=refresh_chat,args=(room_id,))
    api_thread.start()
  load_message(room_id)
def xjoined_room(room_id,data=None,send_message=None):
  global last_response
  if last_response is None:
    print("Hu")
    api_thread = threading.Thread(target=refresh_chat,args=(room_id,))
    api_thread.start()
  if data is None:
   info = {"id": room_id}
   req = requests.post("https://pychat-api.dipdey.repl.co/join",data=info)
   if req.status_code == 200:
    data = req.json()
  #os.system('clear')
  cmd.logo(0)
  cmd.typing(f"[ ~ ] Room Name: {data['room_name']}\n",0)
  cmd.typing(f"\n[ ~ ] Owner : {data['owner']}\n\n",0)
  for key in sorted(data["messages"].keys(), key=int, reverse=True):
    message_data = data["messages"][key]
    cmd.typing(f"{message_data['name']} [{timestamp2time(message_data['timestamp'])}]: {message_data['message']}\n\n",0.00)
  cmd.typing(f"\n[ PY ] Message: ",0.3)
  your_message = input("")
  if your_message in ["/back","back","1"," "]:
     #os.system("clear")
     cmd.logo(0.1)
     cmd.menus()
  elif your_message in ["/refresh","/re","re","0",""]:
     joined_room(room_id)
  else:
    with open(".key.json","r") as e:
      user = json.load(e)
      password = user["password"]
      email = user["email"]
    joined_room(room_id,send_message={"email":email,"message":your_message,"key":password})