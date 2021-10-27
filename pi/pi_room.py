import board
import neopixel
import socket
import time
import mysql.connector
import os
from pi.zone import Zone

s = socket.socket()
s.bind(('',4444))
s.listen(5)
s.settimeout(0)

num_leds = 60
room_id = 0

mydb = mysql.connector.connect(
  host="129.21.124.24",
  user="jabbate",
  password="####",
  database="LightTable"
)
mycursor = mydb.cursor()

pixels = neopixel.NeoPixel(board.D18, num_leds)

room = Zone( pixels, "SOLID", (0,0,0), (0,0,0), (0,0,0), 1 )

def getSQLData():
  mycursor.execute( "SELECT * FROM room" )
  return mycursor.fetchall()

def main():
  # Init
  room_data = getSQLData()[room_id]
  room.reset( room_data[1], room_data[2], room_data[3], room_data[4], room_data[5], room_data[6] )
  # Listen for updates and run lights
  while True:
    # Try and find new message, otherwise continue
    try:
      c, addr = s.accept()
      msg = c.recv(1024).decode()
      c.close()
    except TimeoutError:
      msg = "N/A"
    # Update detection
    if msg == "UPDATE":
          room_data = getSQLData()[room_id]
          room.reset( room_data[1], room_data[2], room_data[3], room_data[4], room_data[5], room_data[6] )
    room.process_colors( time.time() )

if __name__ == "__main__":
  main()