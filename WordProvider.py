import re

class WordProvider:
    def __init__(self, inputConfigProvider):
        # init ConfigProvider object
        self.configProvider = inputConfigProvider

        self.wordList = {}
        self.openType = "r"

        self.re = self.configProvider.getRe()
        self.pattern = re.compile(self.re)
        self.wordListFilePath = self.configProvider.getWordListFilePath()

        # read the word list which need to be deal with
        f = open(self.wordListFilePath,self.openType)
        for line in f:
            match = self.pattern.match(line)
            self.wordList[match.group(1)] = match.group(2)
            # print("the group 1 is " + match.group(1) + ". the group 2 is " + match.group(2))
        f.close()

        # get state from ConfgProvider object
        self.state = self.configProvider.getState()

        # use for test
        # print(self.re + "\n" +
        #       self.wordListFilePath + "\n")


    def getNextWord(self):
        if self.state == "working" :
            num = self.configProvider.getLastFinishedWordNum()
            if num == -1 :
                self.state = "sleeping"
                return None
            else :
                return self.wordList.get(str(num))
        else:
            return None

    def markException(self, word):
        self.configProvider.keepExceptionWords(word)

    def getState(self):
        return self.state

    def setStateSleeping(self):
        self.state = "sleeping"

