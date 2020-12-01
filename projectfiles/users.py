
class Users:
    def __init__(self):
        self.users = []

    def addUser(self, ip):
        nick = None
        self.users.append([ip, nick])
