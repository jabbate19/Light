import asyncio
from flask_socketio import emit
import board
import neopixel
import time
import os
from zone import Zone
import config
import socketio

sio = socketio.AsyncClient()

connected = False

name = 'Development'
num_leds = 60
room_id = 0

pixels = neopixel.NeoPixel(board.D18, num_leds, auto_write = False)

room = Zone( pixels, "PULSE", "#FF0000", "#000000", "#000000" )

@sio.on('connect')
def connect():
  global connected, name
  connected = True
  emit('name', {'name':name})
  room.reset("RAINBOW","#000000", "#000000", "#000000")

@sio.on('disconnect')
def disconnect():
  global connected
  connected = False
  room.reset("PULSE", "#FF0000", "#000000", "#000000")

@sio.on('light')
def light_change(data):
  room.reset( data['style'], data['color1'], data['color2'], data['color3'] )

async def light_monitor():
  while True:
    room.process_colors()

async def connection_monitor():
  while True:
    if not connected:
      await sio.connect('light.cs.house/pi')
    else:
      await sio.wait()

async def main():
  asyncio.gather( light_monitor(), connection_monitor() )
      
if __name__ == "__main__":
  asyncio.run(main())
