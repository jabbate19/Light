####################################
# File name: models.py             #
# Author: Joe Abbate               #
####################################
from light import db
from datetime import datetime

class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.String, primary_key=True)
    firstname = db.Column(db.String, nullable=False)
    lastname = db.Column(db.String, nullable=False)
    picture = db.Column(db.String, nullable=False)

    def __init__(self, uid, firstname, lastname, picture):
        self.id = uid
        self.firstname = firstname
        self.lastname = lastname
        self.picture = picture

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def get_id(self):
        return self.id

    @staticmethod
    def is_authenticated():
        return True

    @staticmethod
    def is_active():
        return True

    @staticmethod
    def is_anonymous():
        return False

class Room(db.Model):
    __tablename__ = 'room'

    id = db.Column(db.String, primary_key=True, nullable=False)
    pswd = db.Column(db.String, nullable=False)
    style = db.Column(db.String, nullable=False)
    color1 = db.Column(db.String, nullable=False)
    color2 = db.Column(db.String, nullable=False)
    color3 = db.Column(db.String, nullable=False)
    last_modify_user = db.Column(db.String, nullable=False)
    last_modify_time = db.Column(db.String, nullable=False)
    session_id = db.Column(db.String, nullable=True)

    def __init__( self, id, pswd, style='COMET2', color1='#B0197E',color2='#E11C52',color3='#FFFFFF' ):
        self.id = id
        self.pswd = pswd
        self.style = style
        self.color1 = color1
        self.color2 = color2
        self.color3 = color3
        self.last_modify_user = 'root'
        self.last_modify_time = datetime.now().strftime("%m/%d/%Y %H:%M:%S")
        self.session_id = None


    def __repr__(self):
        return '<id {}>'.format(self.id)

class Log(db.Model):
    __tablename__ = 'logs'

    id = db.Column(db.String, primary_key=True, nullable=False, auto_increment=True)
    user = db.Column(db.String, nullable=False)
    timestamp = db.Column(db.String, nullable=False)
    device = db.Column(db.String, nullable=False)
    style = db.Column(db.String, nullable=False)
    color1 = db.Column(db.String, nullable=False)
    color2 = db.Column(db.String, nullable=False)
    color3 = db.Column(db.String, nullable=False)

    def __init__(self, room):
        self.user = room.last_modify_user
        self.timestamp = room.last_modify_time
        self.device = room.id
        self.style = room.style
        self.color1 = room.color1
        self.color2 = room.color2
        self.color3 = room.color3

