####################################
# File name: models.py             #
# Author: Ayush Goel & Fred Rybin  #
# Contributors: Joe Abbate         #
####################################
from lights import db

class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.String, primary_key=True)
    style = db.Column(db.String, nullable=True)
    color1 = db.Column(db.String, nullable=True)
    color2 = db.Column(db.String, nullable=True)
    color3 = db.Column(db.String, nullable=True)
    custom = db.Column(db.String, nullable=True)
    attribute = db.Column(db.Integer, nullable=True)

    def __init__(self, uid, style, color1, color2, color3, custom, attribute):
        self.id = uid
        self.type = style
        self.color1 = color1
        self.color2 = color2
        self.color3 = color3
        self.custom = custom
        self.attribute = attribute

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
    custom = db.Column(db.String, nullable=True)
    attribute = db.Column(db.Integer, nullable=True)

    def __init__(self, style, color1, color2, color3, custom, attribute):
        self.type = style
        self.color1 = color1
        self.color2 = color2
        self.color3 = color3
        self.custom = custom
        self.attribute = attribute

    def __repr__(self):
        return '<id {}>'.format(self.id)