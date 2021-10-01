#import board
#import neopixel
import socket
import time
import mysql.connector


s = socket.socket()
s.bind(('',4444))
s.listen(5)

mydb = mysql.connector.connect(
  host="localhost",
  user="jabbate",
  password="###########",
  database="LightTable"
)

mycursor = mydb.cursor()

#pixels = neopixel.NeoPixel(board.D18, 30)
data = None

while True:
    c, addr = s.accept()
    msg = c.recv(1024).decode()
    print( msg )
    if msg == "UPDATE":
        print( "UPDATING SYSTEM" )
        mycursor.execute("SELECT * FROM user WHERE id = 'skyz' limit 1")
        data = mycursor.fetchall()
        print(data[0])
    c.close()
    while True:
        print(time.time())