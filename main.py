## Client Of Animation X 
import os 
import colour
import random
import time
import json
import sys
import requests
import threading
import command as cmd
from pick import pick
from colour import Color
# Code Info
# Developer: Dip Dey
# Project Name: PyChat

def main_menu():
   cmd.logo(0.1)
   if os.path.exists(".key.json"):
     cmd.user_menu()
   else:
    cmd.login()
main_menu()