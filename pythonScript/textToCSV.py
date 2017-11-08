import os

STEP = 1

def getInt(ascii):
    val = ord(ascii)
    if (val > 160):
        val -= 161
    return val

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


base_path = os.path.dirname(__file__)                                               # Base path where code is executed
folder_path = os.path.abspath(os.path.join(base_path, "..", "textInput/")) + "/"    # Path where all text files are

for fileName in os.listdir(folder_path):
    if fileName.endswith(".txt"):
        textFile = open(folder_path + fileName, 'r', encoding='latin-1')
        csvFile = open("../CSVoutput/" + fileName.split('.')[0] + '.csv', 'w', encoding='latin-1')

        csvFile.write("0, 0, Header, 1, 1, 480\n" +
                      "1, 0, Start_track\n" +
                      "1, 0, Title_t, \"Test\"\n" +
                      "1, 0, Tempo, 500000\n" +
                      "1, 0, Instrument_name_t, \"Church Organ\"\n")

        songString = textFile.read()
        accountedNotes = []
        startTime = 0
        endTime = 0
        i = 0
        toWrite = [("", 0, "")]
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

            toWrite.append(("1, ", startTime, ", Note_on_c, 1, " + str(getInt(nextNote)) + ", 127\n"))
            toWrite.append(("1, ", endTime, ", Note_off_c, 1, " + str(getInt(nextNote)) + ", 0\n"))

        sortedList = sorted(toWrite, key=lambda eventTime: eventTime[1])

        for item in sortedList:
            csvFile.write(item[0] + str(item[1]) + item[2])

        size = len(sortedList)
        csvFile.write("1, " + str(sortedList[size - 1][1]) + ", End_track\n")
        csvFile.write("0, 0, End_of_file")
        csvFile.close()
        textFile.close()


