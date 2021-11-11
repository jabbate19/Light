import threading
import board
import neopixel
import time
import os
from zone import Zone
import config
import socketio
import argparse

sio = socketio.Client()

parser = argparse.ArgumentParser(description='Takes Name of Pi Room')
parser.add_argument('-n','--name',type=str,help='Name to Present in Light', nargs = 1,default='Default Name',required=False,dest='name') 

args = parser.parse_args()

name = args.name[0]
num_leds = 60
room_id = 0

pixels = neopixel.NeoPixel(board.D18, num_leds, auto_write = False)

room = Zone( pixels, "PULSE", "#FF0000", "#000000", "#000000" )

@sio.on('connect')
def conn():
  sio.emit('syn',{'connected':True})
  room.reset("RAINBOW","#000000", "#000000", "#000000")

@sio.on('ack')
def ack(data):
  sio.emit('name',{'id':data['id'],'name':name})

@sio.on('disconnect')
def disconn():
  room.reset('PULSE','#FF0000','#000000','#000000')

@sio.on('light')
def light_change(data):
  room.reset( data['style'], data['color1'], data['color2'], data['color3'] )

def attempt_connection():
  connection = False
  while not connection:
    try:
      sio.connect('https://joe-light.cs.house')
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
