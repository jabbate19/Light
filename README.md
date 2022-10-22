# Light

Website-Controlled RGB LED Light Controls. Uses a Bootstrap Frontend and Flask Backend. User data, Room status, and Logs are stored in a MySQL Database. Light nodes use a Linux service and Python script to control and communicate.

## Project Structure

The `./website` directory holds all code pertaining to the Flask website. `./pi` directory holds all code for pi nodes

## Website

### Installing Python

This guide should cover installing python then you need to make sure you have pip installed.

### Requirements

This project requires Python 3.7 or higher

### Recommended setup

From inside your repository directory run

`python -m virtualenv venv`
`source venv/bin/activate`
`pip install -r requirements.txt`

### Accessing the DB locally

If you are on CSHNet, you can access the SQL database via mysql.csh.rit.edu. To obtain credentials, please contact an RTP. If you are unable to do so, you should run your own MySQL database locally and test using that.

### Running the app

All that's left is running it with `flask run -p 8080`. Flask should automatically find app.py, though you may want to set debug mode with export FLASK_ENV=development before you run it. This detects file changes and automatically restarts the program.

## Pi Nodes

### Deploying New Production Node

To add a new pi to the system, find the .deb package within the ./pi directory and run `sudo dpkg -i <NAME>.deb`

You may need to start/enable the service, which can be done via
`sudo systemctl enable light`
`sudo systemctl start light`

Ask an RTP or EBoard member to add the desired display name and Serial ID Number (and whitelist if desired)
To find your Serial ID Number, run `cat /proc/cpuinfo | grep Serial`

### Contributing to Repo

Due to a python module requring sudo, these commands must be done as sudo.

Download Modules via:
`sudo pip3 install -r requirements.txt`

To run:
`sudo python3 pi_room.py`
