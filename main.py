import WordProvider
import WordGetter
import ConfigProvider
import time

myConfigProvider = ConfigProvider.ConfigProvider()
myWordProvider = WordProvider.WordProvider(myConfigProvider)
myWordGetter = WordGetter.WordGetter(myWordProvider,myConfigProvider)

# while myWordProvider.getState() != "sleeping":
#     word = myWordProvider.getNextWord()
#     myWordGetter.getWordByWebService(word)
#     time.sleep(1)

print("finish!")



