import board
import neopixel
import socket
import time
import mysql.connector
import os
from zone import Zone
import config

s = socket.socket()
s.bind(('',4444))
s.listen(5)
s.settimeout(0)

num_leds = 60
room_id = 0

mydb = mysql.connector.connect(
  host = config.DB_IP,
  user = config.DB_USERNAME,
  password = config.DB_PASSWORD,
  database = config.DB_DATABASE
)

mycursor = mydb.cursor()

pixels = neopixel.NeoPixel(board.D18, num_leds, auto_write = False)

room = Zone( pixels, "SOLID", "#000000", "#000000", "#000000", 1 )

def getSQLData():
  mydb.commit()
  mycursor.execute( "SELECT * FROM room" )
  return mycursor.fetchall()

def main():
  # Init
  room_data = getSQLData()[room_id]
  room.reset( room_data[1], room_data[2], room_data[3], room_data[4], room_data[5] )
  # Listen for updates and run lights
  while True:
    # Try and find new message, otherwise continue
    try:
      c, addr = s.accept()
      msg = c.recv(1024).decode()
      c.close()
    except TimeoutError:
      msg = "N/A"
    except socket.error:
      msg = "N/A"
    # Update detection
    if msg == "UPDATE":
      room_data = getSQLData()[room_id]
      print(room_data)
      room.reset( room_data[1], room_data[2], room_data[3], room_data[4], room_data[5] )
    room.process_colors( time.time() )
    pixels.show()
    time.sleep(0.05)

if __name__ == "__main__":
  main()
