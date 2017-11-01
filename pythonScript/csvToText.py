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
    insertIndex = startTime/4                                                   # insert index in list
    lastTime = notes_list[len(notes_list) - 1][0]                               # last midi clock time in list

    while(len(notes_list) <= insertIndex):                                      # append necessary "silent" times to list
        notes_list.append([lastTime, ""])
        lastTime += 4

    endIndex = endTime/4

    while((insertIndex * 4)< endTime):                                          # add the note at the times it should be played
        notes_list[int(insertIndex)][1] += key

        insertIndex += 1

        if len(notes_list) <= endIndex:
            notes_list.append([int(insertIndex * 4), ""])


base_path = os.path.dirname(__file__)                                           # Base path where code is executed
folder_path = os.path.abspath(os.path.join(base_path, "..", "CSVfiles/")) + "/" # Path where all csv files are


for fileName in os.listdir(folder_path):
    if fileName.endswith("test.csv"):

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


        textFile = open(fileName.split('.')[0] + '.txt', 'w')

        for timeNote in notes_list:
            textFile.write(timeNote[1] + ' ')

        textFile.close()

        break

csvFile = open("testOutput.csv", 'w')

csvFile.write("0, 0, Header, 1, 1, 480\n" +
               "1, 0, Start_track\n"       +
               "1, 0, Title_t, \"Test\"\n" +
               "1, 0, Tempo, 500000\n"     +
               "1, 0, Instrument_name_t, \"Church Organ\"\n")

# Poner notas aquí
#
#
#

#csvFile.write("2, [TIEMPO CUANDO SE ACABA LA CANCION], End_track")
csvFile.write("0, 0, End_of_file")
csvFile.close()