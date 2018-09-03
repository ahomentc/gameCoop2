from discuss.models import Post,Reply

class ReplyHelper:
    def __init__(self, post, user):
        self.post = post
        self.user = user

    # recursively get an infinitely nested dictionary of all the replies
    def getRepliesNestedDict(self,highestList):
        tempDict = {}
        for element in highestList:
            subReplies = Reply.objects.filter(post=self.post,parent=element)
            if len(subReplies) == 0:
                tempDict[element] = None
            else:
                tempDict[element] = self.getRepliesNestedDict(subReplies)
        return tempDict

    # returns a dictionary where the subdictionaries have been flattened to a list
    def correctlyFormatDict(self,dict):
        newDict = {}
        for key,value in dict.items():
            if value is None:
                newDict[key] = None
            else:
                newDict[key] = sorted(self.flattenDict(value),key=lambda x:x.pub_date,reverse=False)
        return newDict

    # recursively flattens a dictionary that looks like this: {a:{b:None,c:{d:None}},e:None} to a list [a,b,c,d,e]
    def flattenDict(self,dict):
        tempList = []
        for key,value in dict.items():
            tempList = tempList + [key]
            if value != None:
                tempList = tempList + self.flattenDict(value)
        return tempList

    def getRepliesUserLiked(self):
        allReplies = Reply.objects.filter(post=self.post)
        replies = []
        for reply in allReplies:
            if self.user in reply.userUpVotes.all():
                replies.append(reply)
        return replies

    def getRepliesUserDisliked(self):
        allReplies = Reply.objects.filter(post=self.post)
        replies = []
        for reply in allReplies:
            if self.user in reply.userDownVotes.all():
                replies.append(reply)
        return replies

    def getSortedDict(self):
        sortedDict = {}

        # list of replies that are not replies to a reply to the post
        noParentsList = Reply.objects.filter(post=self.post, parent__isnull=True).order_by('-pub_date')

        infiniteNested = self.getRepliesNestedDict(noParentsList)
        repliesDict = self.correctlyFormatDict(infiniteNested)

        for key in sorted(repliesDict.keys(), key=lambda x: x.pub_date):
            sortedDict[key] = repliesDict[key]

        return sortedDict
