# get all parameters when the ConfigProvider init, and other work object can get parameters from ConfigProvier.
# and most important, you can modify all parameters in only one file -- config.ini. it's easier and more robust
import configparser
import time
import os

class ConfigProvider:
    failedWordFile = None

    def __init__(self):
        if os.name == "nt":
            self.os_path_sep = "\\"
        else:
            self.os_path_sep = "/"

        self.configFilePath = os.path.dirname(__file__) + self.os_path_sep + "configFile" + self.os_path_sep + "config.ini"

        # use for test
        # print(self.configFilePath + "\n")

        self.count = 0
        self.state = "working"
        self.ISOTIMEFORMAT = "%Y-%m-%d"

        # init the configparser
        self.config = configparser.ConfigParser()
        self.config.read(self.configFilePath,encoding="utf-8")

        self.default = self.config["DEFAULT"]
        self.count = int(self.default["count"])
        self.date = self.default["date"]
        self.limitation = int(self.default["limitation"])
        self.failedWordFilePath = self.default["failedWordFilePath"]

        # some config parameters for WordGetter
        self.wgPara = self.config["WGPARA"]
        self.url = self.wgPara["url"]
        self.dicName = self.wgPara["dicName"]
        self.urlFileType = self.wgPara["urlFileType"]
        self.serviceKey = self.wgPara["serviceKey"]
        self.prePath = self.wgPara["prePath"]
        self.exceptionFilePath = self.wgPara["exceptionFilePath"]

        # some config parameters for WordProvider
        self.wpPara = self.config["WPPARA"]
        self.re = self.wpPara["re"]
        self.wordListFilePath = self.wpPara["wordListFilePath"]

        # get current date
        newDate = time.localtime()
        dateStr = time.strftime(self.ISOTIMEFORMAT, newDate)

        if dateStr == self.date and self.count < self.limitation :
            self.state = "working"
        elif dateStr == self.date and self.count >= self.limitation:
            self.state = "sleeping"
        elif dateStr != self.date :
            self.state = "working"
            self.count = 0
            self.default["count"] = str(self.count)
            self.default["date"] = dateStr

        #open failedWordFile
        self.failedWordFile = open(self.failedWordFilePath,"a")

    def getState(self):
        return self.state


    def getLastFinishedWordNum(self):
        if self.state == "working":
            if self.count == self.limitation:
                self.state = "sleeping"
                return -1
            else :
                # set count in program and config file
                self.count = self.count + 1
                self.default['count'] = str(self.count)

                # set lastfinishedWordNum in
                newLastfinishedWordNum = int(self.default["lastfinishedWordNum"]) + 1
                self.default["lastfinishedWordNum"] = str(newLastfinishedWordNum)
                return newLastfinishedWordNum

        elif self.state == "sleeping" :
            return -1

    def keepExceptionWords(self, word):
        self.failedWordFile.write(word)

    def __del__(self):
        with open(self.configFilePath, "w", encoding="utf-8") as configfile:
            self.config.write(configfile)
        if self.failedWordFile != None:
            self.failedWordFile.close()
        self.config = None

    # some get function for WordGetter
    def getUrl(self):
        return self.url

    def getDicName(self):
        return self.dicName

    def getUrlFileType(self):
        return self.urlFileType

    def getServiceKey(self):
        return self.serviceKey

    def getPrePath(self):
        return self.prePath

    def getExceptionFilePath(self):
        return self.exceptionFilePath

    def getOsPathSep(self):
        return self.os_path_sep

    # some get function for WordProvider
    def getRe(self):
        return self.re

    def getWordListFilePath(self):
        return self.wordListFilePath

