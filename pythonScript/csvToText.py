import os
import csv

STEP = 1

def getAscii(val):
    intVal = int(val)
    if (intVal < 33):
        intVal += 161
    return str(chr(intVal))

def getBPM(tempo): # 2 midi clocks
    return (tempo * 3)/12500

def insertToList(key, startTime, endTime):
    insertIndex = startTime/STEP                                                   # insert index in list
    lastTime = notes_list[len(notes_list) - 1][0]                               # last midi clock time in list

    while(len(notes_list) <= insertIndex):                                      # append necessary "silent" times to list
        notes_list.append([lastTime, ""])
        lastTime += STEP

    endIndex = endTime/STEP

    while((insertIndex * STEP)< endTime):                                          # add the note at the times it should be played
        notes_list[int(insertIndex)][1] += key

        insertIndex += 1

        if len(notes_list) <= endIndex:
            notes_list.append([int(insertIndex * STEP), ""])


base_path = os.path.dirname(__file__)                                           # Base path where code is executed
folder_path = os.path.abspath(os.path.join(base_path, "..", "CSVfiles/")) + "/" # Path where all csv files are

textFile = open("../aiOutput/turingInput.txt", 'a', encoding='latin-1')

for fileName in os.listdir(folder_path):
    if fileName.endswith(".csv"):

        notes_list = [[0, ""]]
        notes_helper_dict = {'a': 0}                                            # helps us get start and end index for a note

        reader = csv.reader(open(folder_path + fileName, encoding='latin-1'),
                            delimiter=',', quotechar='"', skipinitialspace=True)
        for row in reader:
            if(row[2] == "Note_on_c" or row[2] == "Note_off_c"):
                velocity = row[5]
                key = getAscii(row[4])
                time = row[1]

                if(velocity != "0" and row[2] == "Note_on_c"):                  # this means it's the start time
                    notes_helper_dict[key] = time

                else:                                                           # this means it's the end time so we insert it
                    startTime = notes_helper_dict[key]
                    insertToList(key, int(startTime), int(time))

        for timeNote in notes_list:
            textFile.write(timeNote[1] + ' ')

        textFile.write(' ')

textFile.close()
