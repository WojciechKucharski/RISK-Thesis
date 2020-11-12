def command_int(self, command):

    print(command)
    if len(command) <= 1:
        print("Error")
        return False
    if command[2] == "roomlist":
        feedback = []
        for x in self.rooms:
            feedback.append(x.room_name)
        return feedback
    elif command[2] =="create" and command[1] == "lobby":

        if len(self.rooms) < 4:
            print("Room created")
            self.create_room(command[0])
            return command[0]

        return False
    elif command[2] == "mapname":
        return self.rooms[self.index(command[1])].mapname
    elif command[2] == "prov":
        a = self.rooms[self.index(command[1])].provs[command[3]].owner
        b = self.rooms[self.index(command[1])].provs[command[3]].units
        return [a, b]

    else:
        return False

