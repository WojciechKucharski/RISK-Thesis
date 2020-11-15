from datetime import datetime, date

def connect_csv(path): #reading CSV file
    obj = []
    with open(path) as f:
        lis = [line.split(",") for line in f] #splits line with ,
        for i, x in enumerate(lis):
            x[-1] = x[-1][:-1]
            obj.append(x)
    return obj #returns list of lists, lines in first, values in second

########################################################################################################################

color = {
    "red":(255, 0, 0), "blue":(0, 0, 255), "lime":(0, 255, 0),
    "cyan":(0,255,255), "green":(0, 153, 0), "yellow":(255, 255, 0),
    "white":(255, 255, 255), "black":(0, 0, 0), "brown":(102, 51, 0),
    "orange":(255, 153, 0), "pink":(255, 0, 255), "purple":(102, 0, 204),
    "gray":(115, 115, 115), "beige":(255, 230, 179)
}

color2 = [(255, 0, 0), (0, 0, 255), (0, 255, 0),
    (0,255,255), (0, 153, 0),(255, 255, 0),
    (255, 255, 255), (0, 0, 0), (102, 51, 0),
    (255, 153, 0), (255, 0, 255), (102, 0, 204),
    (115, 115, 115), (255, 230, 179)]

########################################################################################################################

def printError(e): #saving error message to file

    try:
        dateC ="Data\\Crash\\" + date.today().strftime("%d_%m_%Y") + ".txt" #current date
        now = datetime.now().strftime("%H_%M_%S") + str(e) +"\n"       #current time + error message
        with open(dateC, "a") as myfile:
            myfile.write(now)
        myfile.close() #close file
    except Exception as e:
        print(e)