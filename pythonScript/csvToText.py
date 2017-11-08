import os
import csv

STEP = 2

def getAscii(val):
    intVal = int(val)
    if (intVal < 33):
        intVal += 161
    return str(chr(intVal))


def getInt(ascii):
    val = ord(ascii)
    if (val > 160):
        val -= 161
    return val

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

def getNextNote(songString, index, accountedNotes, startTime):
    consecutiveSpaces = 0
    time = startTime

    for i in range(index, len(songString)):
        if songString[i] == ' ':
            time += STEP
            consecutiveSpaces+=1
            if consecutiveSpaces == 2:
                del accountedNotes[:]
                consecutiveSpaces -= 2

        else:
            consecutiveSpaces = 0
            if songString[i] not in accountedNotes:
                return [songString[i], i, time]

    return [' ', -1, time]

def getNoteEndTime(songString, index, startTime):
    consecutiveSpaces = 0
    endTime = startTime
    notesInWord = []
    note = songString[index]

    for i in range(index, len(songString)):
        if songString[i] == ' ':

            consecutiveSpaces+=1

            if note not in notesInWord:
                return endTime

            del notesInWord[:]
            if consecutiveSpaces == 2:
                return endTime

            endTime += STEP
        else:
            notesInWord.append(songString[i])
            consecutiveSpaces = 0

    return endTime + STEP

base_path = os.path.dirname(__file__)                                           # Base path where code is executed
folder_path = os.path.abspath(os.path.join(base_path, "..", "CSVfiles/")) + "/" # Path where all csv files are


for fileName in os.listdir(folder_path):
    if fileName.endswith("BWV983.MID.csv"):

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

textFile = open("BWV983.txt", 'r')
csvFile = open("testOutput.csv", 'w')

csvFile.write("0, 0, Header, 1, 1, 480\n" +
               "1, 0, Start_track\n"       +
               "1, 0, Title_t, \"Test\"\n" +
               "1, 0, Tempo, 500000\n"     +
               "1, 0, Instrument_name_t, \"Church Organ\"\n")

songString = textFile.read()
accountedNotes = []
startTime = 0
endTime = 0
songEnding = 0
i = 0
toWrite = [("",0,"")]
del toWrite[:]

while i < len(songString):
    next = getNextNote(songString, i, accountedNotes, startTime)
    i = next[1]
    startTime = next[2]
    if i < 0:
        break
    nextNote = next[0]
    accountedNotes.append(nextNote)
    endTime = getNoteEndTime(songString, i, startTime)
    if endTime > songEnding:
        songEnding = endTime

    toWrite.append(("1, ", startTime, ", Note_on_c, 1, " + str(getInt(nextNote)) + ", 127\n"))
    toWrite.append(("1, ", endTime, ", Note_off_c, 1, " + str(getInt(nextNote)) + ", 0\n"))

sortedList = sorted(toWrite, key=lambda eventTime: eventTime[1])

for item in sortedList:
    csvFile.write(item[0] + str(item[1]) + item[2])

csvFile.write("1, " + str(endTime) + ", End_track\n")
csvFile.write("0, 0, End_of_file")
csvFile.close()
textFile.close()