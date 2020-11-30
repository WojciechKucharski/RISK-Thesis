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
        if command[2] == "myState": #returns -1 state, because user is in lobby
            return -1
        elif command[2] == "roomlist": #returns list of rooms from lobby object
            feedback = []
            for x in self.rooms:
                feedback.append(x.room_name)
            return feedback
        elif command[2] == "gameInfo": #if user asks for game info, and is in lobby, returns -1
            return [None, -1]
        elif command[2] == "create" and command[1] == "lobby": #command to create ROOM
            if len(self.rooms) < 4:
                print("Room created") #info about creating ROOM
                self.create_room(command[0])
                return command[0]
            return False
        elif command[2] == "join": #command to join certain ROOM
            self.rooms[self.index(command[3])].addplayer(command[0])
        else:
            return False
# COMMANDS WHILE IN GAME ###############################################################################################
    else:
        if command[2] == "gameInfo": #returns game info
            return self.rooms[self.index(command[1])].gameInfo(command[0])
        elif command[2] == "provinces": #returns LIST about provinces
            return self.rooms[self.index(command[1])].provinces
        elif command[2] == "myState": #returns user state [0 - 9]
            return self.rooms[self.index(command[1])].myState(command[0])
        elif command[2] == "gameSet": #returns game parameters [only if myState == 0]
            return self.rooms[self.index(command[1])].gameSet(command[0])
        elif command[2] == "gameSet2": #changes some game parameters, only if user is host
            self.rooms[self.index(command[1])].gameSet2(command[0], command[3])
        elif command[2] == "start": #starts game, only if user is host
            self.rooms[self.index(command[1])].startGame(command[0])
        elif command[2] == "provClick": #sends info about clicked province
            self.rooms[self.index(command[1])].provClick(command[0], command[3])
        elif command[2] == "skipAttack": #sends command to skip attacking
            self.rooms[self.index(command[1])].skipAttack(command[0])
        elif command[2] == "skipFortify": #sends command to skip fortifying
            self.rooms[self.index(command[1])].skipFortify(command[0])
        elif command[2] == "Tactic": #sends info about tactic user have chosen
            return self.rooms[self.index(command[1])].Tactic(command[0], command[3])
        elif command[2] == "number": #sends info about number chosen by user
            self.rooms[self.index(command[1])].number(command[0], command[3])
        elif command[2] == "leave": #sends info about leaving ROOM
            self.rooms[self.index(command[1])].rmplayer(command[0])
            self.clear_rooms()
        elif command[2] == "kick": #kicks player from ROOM, only for host
            self.rooms[self.index(command[1])].kick(command[0], command[3])
    return False
########################################################################################################################