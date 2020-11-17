def command_int(self, command):
    #command 0 1 2 3 4
    #        nick, room, command, args

    if len(command) <= 1:
        print("Error")
        return False

    command[1] = self.whereIam(command[0])

    ########################################################################################################################

    if command[2] == "whereIam":
        return command[1]

########################################################################################################################
    if command[1] == "lobby":
        if command[2] == "roomlist":
            feedback = []
            for x in self.rooms:
                feedback.append(x.room_name)
            return feedback
        elif command[2] == "create" and command[1] == "lobby":

            if len(self.rooms) < 4:
                print("Room created")
                self.create_room(command[0])
                return command[0]

            return False

        elif command[2] == "join":
            print(command)
            self.rooms[self.index(command[3])].addplayer(command[0])

########################################################################################################################
    # self.rooms[self.index(command[1])].
    else:
        if command[2] == "mapname":
            return self.rooms[self.index(command[1])].mapname

        elif command[2] == "prov":
            a = self.rooms[self.index(command[1])].provs[command[3]].owner
            b = self.rooms[self.index(command[1])].provs[command[3]].units
            return [a, b]
        elif command[2] == "player_list":
            return self.rooms[self.index(command[1])].players
        elif command[2] == "leave":
            self.rooms[self.index(command[1])].rmplayer(command[0])
            self.clear_rooms()
        elif command[2] == "myState":
            return self.rooms[self.index(command[1])].myState(command[0])

########################################################################################################################

    return False