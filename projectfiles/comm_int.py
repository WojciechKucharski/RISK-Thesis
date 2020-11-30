def command_int(self, command):
    if len(command) <= 1: #check if command structure is wrong
        print("Error")
        return False
    command[1] = self.whereIam(command[0]) #check where client is

# COMMANDS WHILE IN ALWAYS #############################################################################################
    if command[2] == "whereIam": #returns name of room player is in
        return command[1]
# COMMANDS WHILE IN LOBBY ##############################################################################################
    if command[1] == "lobby":
        if command[2] == "myState":
            return -1
        elif command[2] == "roomlist":
            feedback = []
            for x in self.rooms:
                feedback.append(x.room_name)
            return feedback
        elif command[2] == "gameInfo":
            return [None, -1]
        elif command[2] == "create" and command[1] == "lobby":
            if len(self.rooms) < 4:
                print("Room created")
                self.create_room(command[0])
                return command[0]
            return False
        elif command[2] == "join":
            self.rooms[self.index(command[3])].addplayer(command[0])
        else:
            return False
# COMMANDS WHILE IN GAME ###############################################################################################
    else:
        if command[2] == "gameInfo":
            return self.rooms[self.index(command[1])].gameInfo(command[0])
        elif command[2] == "provinces":
            return self.rooms[self.index(command[1])].provinces
        elif command[2] == "myState":
            return self.rooms[self.index(command[1])].myState(command[0])
        elif command[2] == "gameSet":
            return self.rooms[self.index(command[1])].gameSet(command[0])
        elif command[2] == "gameSet2":
            self.rooms[self.index(command[1])].gameSet2(command[0], command[3])
        elif command[2] == "start":
            self.rooms[self.index(command[1])].startGame(command[0])
        elif command[2] == "provClick":
            self.rooms[self.index(command[1])].provClick(command[0], command[3])
        elif command[2] == "skipAttack":
            self.rooms[self.index(command[1])].skipAttack(command[0])
        elif command[2] == "skipFortify":
            self.rooms[self.index(command[1])].skipFortify(command[0])
        elif command[2] == "Tactic":
            return self.rooms[self.index(command[1])].Tactic(command[0], command[3])
        elif command[2] == "number":
            self.rooms[self.index(command[1])].number(command[0], command[3])
        elif command[2] == "leave":
            self.rooms[self.index(command[1])].rmplayer(command[0])
            self.clear_rooms()
        elif command[2] == "kick":
            self.rooms[self.index(command[1])].kick(command[0], command[3])
    return False
########################################################################################################################