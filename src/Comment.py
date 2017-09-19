import numpy

class GenericComment:
    def __init__(self, comment):
        self.id = comment.id
        self.author = comment.author
        self.score = comment.score
        self.body = comment.body

    def printout(self):
        return "TOP: " + self.body + " Id: " + str(self.id) + " Author: " + str(self.author) + " Score: " + str(self.score)

class TopLevelComment(GenericComment):
    commentChildren = []

    def printTree(self):
        for childComment in self.commentChildren:
            print("CHILD: " + childComment.body)
