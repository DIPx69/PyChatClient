import time
import os
import command as cmd
def logo(delay):
  os.system("clear")
  text = """
 ____         ____ _           _   
|  _ \ _   _ / ___| |__   __ _| |_ 
| |_) | | | | |   | '_ \ / _` | __|
|  __/| |_| | |___| | | | (_| | |_ 
|_|    \__, |\____|_| |_|\__,_|\__|
       |___/                       
"""
  cmd.typing(text,delay)
  print("\n")