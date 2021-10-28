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

mydb = mysql.connector.connect(
  host = config.DB_IP,
  user = config.DB_USERNAME,
  password = config.DB_PASSWORD,
  database = config.DB_DATABASE
)
mycursor = mydb.cursor()

pixels = neopixel.NeoPixel(board.D18, 60)

# Function that prints
# the required sequence
def split(x, n):
 
    # If we cannot split the
    # number into exactly 'N' parts
    if(x < n):
        return None
 
    # If x % n == 0 then the minimum
    # difference is 0 and all
    # numbers are x / n
    elif (x % n == 0):
      out = []
      for i in range(n):
          out.append(x//n)
      return out
    else:
      # upto n-(x % n) the values
      # will be x / n
      # after that the values
      # will be x / n + 1
      zp = n - (x % n)
      pp = x//n
      out = []
      for i in range(n):
        if(i>= zp):
          out.append(pp + 1)
        else:
          out.append(pp)
      return out

def getSQLData():
  mycursor.execute("SELECT * FROM seat")
  return mycursor.fetchall()

def main():
  # Init
  data = getSQLData()
  num_seats = len(data)
  seats = []
  # Split pixels among the seats, add seats to list
  start = 0
  end = 0
  nums = split( 60, num_seats )
  for i in range( num_seats ):
    nxt_pt = nums[i]
    end += nxt_pt
    s = data[i]
    seats.append( Seat( pixels[start:end], s[1], s[2], s[3], s[4], s[5], s[6] ) )
    start = nxt_pt
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
    if "UPDATE" in msg:
          print( "UPDATING SYSTEM" )
          seat_index = int(msg[6])-1
          s = getSQLData()[seat_index]
          seats[seat_index].reset( s[1], s[2], s[3], s[4], s[5], s[6] )
    # Light updates
    for seat in seats:
      seat.process_colors( time.time() )
    pixels.write()

if __name__ == "__main__":
  main()