#Andrew Loeliger
#Quick class for creating output spaces and handling the datacards

import datetime
import os
import random
import string

class outputArea():
    def __init__(self):
        #let's start by deciding the random "name" that we give to the area
        self.dateTag = datetime.datetime.now().strftime("%d%b%y_%H%M") + '_' + self.createRandomStringTag()
        
        #now, let's set up the actual directories we need
        self.outputPath = os.environ['CMSSW_BASE']+'/src/bbtautau_Combine/output/Output_'+self.dateTag
        os.makedirs(self.outputPath)

        #report the location
        self.printOutputInfo()

    def createRandomStringTag(self, size=6, chars=string.ascii_uppercase+string.ascii_lowercase+string.digits):
        return ''.join(random.choice(chars) for x in range(size))

    def printOutputInfo(self):
        print('')
        print('**************************************************')
        print('{:^50}'.format("This sesion is run under tag: "+self.dateTag))
        print('**************************************************')
        print('')
