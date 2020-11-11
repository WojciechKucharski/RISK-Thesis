def command_int(self, command):
    if command == "roomlist":
        feedback = []
        for x in self.rooms:
            feedback.append(x.room_name)
        return feedback
    elif command =="create":
        print(len(self.rooms))
        if len(self.rooms) < 4:
            self.create_room("Nejpad")
    else:
        return False
