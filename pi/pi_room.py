import threading
import board
import neopixel
import time
import os
from zone import Zone
import config
import socketio
import argparse
import re

sio = socketio.Client()

parser = argparse.ArgumentParser(description='Takes Name of Pi Room')
parser.add_argument('-n','--name', type=str, help='Name to Present in Light', nargs = 1, default='Dev', required=False, dest='name') 
parser.add_argument('--host', type=str, help='Hostname to Connect To', nargs=1, default='http://127.0.0.1', required=False, dest='host')

args = parser.parse_args()

name = args.name[0]
host = args.host[0]
num_leds = 60
room_id = 0

pixels = neopixel.NeoPixel(board.D18, num_leds, auto_write = False)

room = Zone( pixels, "OFF", "#000000", "#000000", "#000000" )

kill = False

def get_serial():
  with open('/proc/cpuinfo') as file:
    for line in file:
      out = re.findall('Serial\s*:\s*[\d\w]*',line)
      if out:
        return out[0][10:]

@sio.on('connect')
def conn():
  print("Connected")
  pswd = get_serial()
  sio.emit('login',{'name':name,'pass':pswd})

@sio.on('login error')
def err(data):
  print('Login Error:',data['data'])
  sio.disconnect()

@sio.on('disconnect')
def disconn():
  print("Disconnected")
  kill = True
  room.reset('SOLID','#000000','#000000','#000000')

@sio.on('light')
def light_change(data):
  room.reset( data['style'], data['color1'], data['color2'], data['color3'] )

def attempt_connection():
  connection = False
  while not connection:
    try:
      sio.connect(host)
    except socketio.exceptions.ConnectionError as err:
      print(err)
      time.sleep(3)
    else:
      connection = True

def light_monitor():
  while True:
    room.process_colors()

def connection_monitor():
  attempt_connection()
  sio.wait()

def main():
  conn = threading.Thread(target=connection_monitor)
  light = threading.Thread(target=light_monitor)
  conn.start()
  light.start()
      
if __name__ == "__main__":
  main()

