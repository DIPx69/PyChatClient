import time
def typing(input_text,delay):
   delay = delay/len(input_text)
   for char in input_text:
     print(f"{char}",flush=True,end='')
     time.sleep(delay)