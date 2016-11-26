import urllib.request


class WordGetter:

    def __init__(self, inputWordProvider, inputConfigProvider):

        self.url_sep = "/"
        self.fileType = ".xml"

        # init myWordProvider
        self.myWordProvider = inputWordProvider

        # init myConfigProvider
        self.myConfigProvider = inputConfigProvider

        # these variables below need to get from ConfigProvider, later.
        self.prePath = self.myConfigProvider.getPrePath()
        self.url = self.myConfigProvider.getUrl()
        self.dicName = self.myConfigProvider.getDicName()
        self.urlFileType = self.myConfigProvider.getUrlFileType()
        self.serviceKey = self.myConfigProvider.getServiceKey()
        self.exceptionFilePath = self.myConfigProvider.getExceptionFilePath()
        self.exceptions = open(self.exceptionFilePath, "a")

        # use for text
        # print(self.prePath + "\n" +
        #       self.url + "\n" +
        #       self.dicName + "\n" +
        #       self.urlFileType + "\n" +
        #       self.serviceKey + "\n" +
        #       self.exceptionFilePath + "\n")



    def makeFileName(self, word):
        return self.prePath + word + self.fileType

    def makeUrl(self,word):
        return self.url + self.dicName + self.url_sep + self.urlFileType + self.url_sep + word + "?key=" + self.serviceKey

    def getWordByWebService(self, word):
        if word is not None:
            fullUrl = self.makeUrl(word)
            fullPathName = self.makeFileName(word)
            xml = None
            try:
                xml = urllib.request.urlopen(fullUrl)
            except Exception as e:
                print(e)
                self.exceptions.write(str(e))
                self.myWordProvider.markException(word)

            content = xml.read().decode("utf-8")

            file = open(fullPathName, "w", encoding="utf-8")
            file.write(content)
            file.close()
        elif word is None and self.myWordProvider.getState()=="working":
            print("Some thing is wrong with WordProvider!! Please check." +
                  "\n" +
                  "or The current work list is finished!!")
            self.myWordProvider.setStateSleeping()


    def __del__(self):
        if self.exceptions != None :
            self.exceptions.close()


