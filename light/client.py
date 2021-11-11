from datetime import datetime

class Client:
    __slots__ = ['sid','name', 'last_modify_time', 'last_modify_user', 'style', 'color1', 'color2', 'color3']
    def __init__(self, sid):
        self.sid = sid
        self.name = ''
        self.last_modify_time = datetime.now().strftime("%m/%d/%Y %H:%M:%S")
        self.last_modify_user = 'root'
        self.style = 'SOLID'
        self.color1 = '#B0197E'
        self.color2 = '#E11C52'
        self.color3 = '#B0197E'