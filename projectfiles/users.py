
class Users:
    def __init__(self, N):
        self.users = []
        for _ in range(N):
            self.users.append(None)

    @property
    def size(self):
        return len(self.users)

    def join(self, ip):
        for i in range(self.size):
            if self.users[i] == None:
                self.users[i] = ip
                return i
            return False

    def leave(self, id):
        self.users[id] = None