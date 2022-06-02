from Result import CommentsOperation, CommentOperation, EraseOperation

newLine = '\n'
space = ' '
none = ''
t = '\t'
r = '\r'
doubleString = '\"'
oneString = '\''
slash = '\\'
sharp = '#'
doubleSlash = '//'
end = ';'
figure = '{'
OLComments = []
MLComments = []
MLCStart = "/*"
MLCEnd = '*/'
textWord = 'text'
commentWord = 'comment'
commentsWord ='comments'
countWord = 'count'
positionWord = 'position'

def findComments(text, startChar, splitter):
    position = 0
    length = len(splitter) - 1
    comments = []
    while position < len(text) - length:
        position = findWordComment(text, position, startChar).position
        result = addComment(text, position, comments, splitter)
        text = result.text
    return CommentsOperation(text, removeStrings(comments))

def addComment(text, position, comments, splitter):
    result = findWordComment(text, position, splitter)
    comments.append(result.comment)
    return result

def removeStrings(array, item=''):
    while item in array:
        array.remove(item)
    return array

def findWordComment(text, position, splitter):
    length = len(splitter)
    endPosition = position + length
    return findComment(text, position, endPosition, splitter)

def findComment(text, position, endPosition, splitter):
    size = len(text)
    end = endPosition + len(splitter)
    while getTextFragment(text, endPosition, end) != splitter and endPosition < size:
        endPosition += 1
        end += 1
    comment = text[position: end]
    text = text[:position] + text[end:]
    return CommentOperation(text, comment, endPosition)

def getTextFragment(text, startPosition, endPosition):
    return text[startPosition:endPosition]

def findFirstChar(s, position, char):
    while position < len(s) and s[position] != char:
        position += 1
    return position


def findMLC(s):
    return findComments(s, MLCStart, MLCEnd)

def findOLC(s):
    return findComments(s, doubleSlash, newLine)

def getText( path  ):
    return open(path).read()

def eraseEmptyLines(s):
    position = 0
    while position < len(s):
        if s[position] == newLine:
           result = eraseEmptyLine(s, position)
           position = result.position
           s = result.text
        position += 1
    return s

def eraseEmptyLine(s, startPosition):
    position = startPosition + 1
    result = EraseOperation(s, startPosition)
    while position < len(s) and s[position] == space :
        position += 1
    if position < len(s) and s[position] == newLine:
        result.text = s[:startPosition] + s[position:]
        result.position -= 1
    return result

def getMLCLinesCount(array):
    sum = 0
    for item in array:
        sum += item.count(newLine) + 1
    return sum

def deleteNotInfluenced(text):
    notInfluenced = [t, r, newLine, space ]
    for item in notInfluenced:
        text = text.replace(item, '')
    return text

def countLLOC(text):
    text = deleteNotInfluenced(text)
    result = countJumps(text)
    result += countFiguresAndEnds(text, result)
    result += countConditions(text)
    result += countLoop(text)
    result += countTry(text)
    return result

def countConditions(text):
    conditions = ['if', 'else', 'elseif', '?', ':', 'switch', 'case']
    return countWords(text, conditions)

def countTry(text):
    tryCatch = ['try', 'catch', 'finnaly']
    return countWords(text, tryCatch)

def countWords(text, conditions):
    result = 0
    for item in conditions:
        result += countChar(text, item)
    return result

def countJumps(text):
    jump = ['break', 'continue']
    return countWords(text, jump)



def countLoop(text):
    words = ['for', 'foreach', 'while']
    return countWords(text, words)

def countFiguresAndEnds(text, other ):
    semi = '};'
    return text.count(figure ) + text.count(end) - 2 * text.count(semi) - other

def countChar(text, char):
    lengthText = len(text)
    lengthChar = len(char)
    count = 0
    for i in range(0, lengthText):
        chars = text[i:i+ lengthChar]
        if chars == char:
            count += checkKeyWord(text, i, lengthChar)
    return count

def checkKeyWord(text, i, length):
    previousChar = text[i - 1]
    nextChar = text[i + length]
    if checkChar(previousChar) and checkChar(nextChar):
        return 0
    return 1

def checkChar(char):
    position = ord(char)
    return checkUpper(position) or checkLower(position) or checkUnderLine(position) or checkNumber(position)# CheckUnderLine(position)

def inRange(position, start, end):
    return position >= start and position <= end

def checkUpper(position):
    startUpper = 65
    endUpper = 90
    return inRange(position, startUpper, endUpper)

def checkLower(position):
    startLower = 97
    endLower = 122
    return inRange(position, startLower, endLower)

def checkUnderLine(position):
    underline = 95
    return position == underline

def checkNumber(position):
    start = 48
    end = 57
    return inRange(position, start, end)

def Program(fileName):
    s = getText(fileName)
    count = s.count(newLine) + 1


    result = findMLC(s)
    s = result.text
    MLComments = result.comments


    result = findOLC(s)
    s = result.text
    OLComments = result.comments


    s = eraseEmptyLines(s)


    OLCCount = len(OLComments)
    MLCCount = getMLCLinesCount(MLComments)
    commentsCount = OLCCount + MLCCount


    print(s)


    PLOC = s.count(newLine) + 1
    LLOC = countLLOC(s)


    print('LOC: ' + str(count) + ', comments: ' + str(commentsCount) +', LLOC: ' + str(LLOC) + ', PLOC: ' + str(PLOC))


    return s

