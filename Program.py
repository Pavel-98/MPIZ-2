from Result import CommentsOperation, CommentOperation, EraseOperation

newLine = '\n'
space = ' '
none = ''
t = '\t'
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
    LLOC = s.count(figure ) + s.count(end)


    print('LOC: ' + str(count) + ', comments: ' + str(commentsCount) +', LLOC: ' + str(LLOC) + ', PLOC: ' + str(PLOC))


    return s

