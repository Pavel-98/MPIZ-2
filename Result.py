class CommentsOperation:
    def __init__(self, text, comments):
        self.text = text
        self.comments = comments

class CommentOperation:
    def __init__(self, text, comment, position):
        self.text = text
        self.comment = comment
        self.position = position

class EraseOperation:
    def __init__(self, text, position):
        self.text = text
        self.position = position

