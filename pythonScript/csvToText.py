import os
import csv

def getAscii(val):
    intVal = int(val)
    if (intVal < 33):
        intVal += 161
    return str(chr(intVal))


def getInt(ascii):
    val = ord(ascii)
    if (ascii > 160):
        val -= 161
    return val

def getBPM(tempo): # 4 midi clocks
    return (tempo * 3)/12500

def insertToList(key, startTime, endTime):
    insertIndex = startTime/4                           # insert index in list
    lastTime = notes_list[len(notes_list) - 1][0]       # last midi clock time in list

    while(len(notes_list) <= insertIndex):              # append necessary "silent" times to list
        notes_list.append([lastTime, ""])
        lastTime += 4

    while(lastTime <= endTime):                          # add the note at the times it should be played
        notes_list[len(notes_list) - 1][1] += key
        notes_list.append([lastTime, ""])
        lastTime += 4

path = "/Users/Angel/Documents/Iteso/7moSemestre/AI/CSVfiles/" # Angel path

notes_list = [[0, ""]]
notes_helper_dict = {'a': 0}                            # helps us get start and end index for a note

for fileName in os.listdir(path):
    if fileName.endswith("test.csv"):

        reader = csv.reader(open(path + fileName, encoding='latin-1'),
                            delimiter=',', quotechar='"', skipinitialspace=True)
        for row in reader:
            if(row[2] == "Note_on_c"):
                velocity = row[5]
                key = getAscii(row[4])
                print(key)
                time = row[1]

                if(velocity != "0"):                     # this means it's the start time
                    notes_helper_dict[key] = time

                else:                                    # this means it's the end time so we insert it
                    startTime = notes_helper_dict[key]
                    insertToList(key, int(startTime), int(time))

        break

for timeNote in notes_list:
    print(timeNote)

print(notes_helper_dict)