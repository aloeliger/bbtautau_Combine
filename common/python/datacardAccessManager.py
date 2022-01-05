#Andrew Loeliger
#quick class to avoid repeating datacard accessing code in multiple submodules

import os
import re

class datacardAccessManager():
    def __init__(self, dateTag):
        self.dateTag = dateTag
        self.homePath = os.getcwd()
        self.outputPath = os.environ['CMSSW_BASE']+'/src/bbtautau_Combine/output/Output_'+self.dateTag
        if not os.path.isdir(self.outputPath):
            print("Couldn't find the output path. Check the date tag.")
            exit(-1)

        os.chdir(self.outputPath)

        self.cardNames = filter(lambda x: re.match("FinalCard.+[0-9]\.root", x), os.listdir("./"))
    

    def getCardNames(self):
        return self.cardNames

    def returnToHomePath(self):
        os.chdir(self.homePath)
