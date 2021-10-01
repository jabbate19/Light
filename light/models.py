####################################
# File name: models.py             #
# Author: Ayush Goel & Fred Rybin  #
# Contributors: Joe Abbate         #
####################################
from light import db

class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.String, primary_key=True)
    firstname = db.Column(db.String, nullable=False)
    lastname = db.Column(db.String, nullable=False)
    picture = db.Column(db.String, nullable=False)
    style = db.Column(db.String, nullable=True)
    color1 = db.Column(db.String, nullable=True)
    color2 = db.Column(db.String, nullable=True)
    color3 = db.Column(db.String, nullable=True)
    numcolors = db.Column(db.Integer, nullable=True)

    def __init__(self, uid, firstname, lastname, picture, style, color1, color2, color3, numcolors):
        self.id = uid
        self.firstname = firstname
        self.lastname = lastname
        self.picture = picture
        self.type = style
        self.color1 = color1
        self.color2 = color2
        self.color3 = color3
        self.numcolors = numcolors

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


class Seat(db.Model):
    __tablename__ = 'events'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user = db.Column(db.String, db.ForeignKey('user.id'), nullable=True)
    style = db.Column(db.String, nullable=True)
    color1 = db.Column(db.String, nullable=True)
    color2 = db.Column(db.String, nullable=True)
    color3 = db.Column(db.String, nullable=True)
    numcolors = db.Column(db.Integer, nullable=True)

    def __init__(self, style, color1, color2, color3, numcolors):
        self.type = style
        self.color1 = color1
        self.color2 = color2
        self.color3 = color3
        self.numcolors = numcolors

    def __repr__(self):
        return '<id {}>'.format(self.id)