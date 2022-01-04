#Andrew Loeliger
#Script for running the combine harvester models, and archiving the output

import argparse
from  bbtautau_Combine.combineHarvesterModel.outputArea import outputArea
import os
import logging
import re


def main(args):

    #Let's set-up an ouput area to store all the cards we make
    theOutputArea = outputArea()
    
    #change over to the output directory. All output should be created there now
    homePath = os.getcwd()
    os.chdir(theOutputArea.outputPath)

    #let's set up logging information to make sure we understand what happens across the whole process
    logging.basicConfig(filename="CombineHistory_"+theOutputArea.dateTag+".log",
                        filemode="w",
                        level=logging.INFO,
                        format='%(asctime)s %(message)s')

    outputLoggingFileName = "outputLog_"+theOutputArea.dateTag+".txt"

    #okay. Let's run the actual card creation command
    cardCreationCommand = 'bbtautauModel'
    #If any other complications to the card creation command get created, we put them here
    #Now, log the command itself, so the process is recreatable
    os.system(cardCreationCommand + ' | tee -a ' + outputLoggingFileName)
    logging.info('Card Creation Command')
    logging.info('\n\n'+cardCreationCommand+'\n')

    #Now, process into a final text based datacard, and workable workspace

    #let's find everything that looks like it is one of our cards
    #this isn't exactly perfect, but I don't have better ideas right now
    cardNames = filter(lambda x: re.match(".+_[0-9]+\.txt", x), os.listdir("./"))
    
    #Combine cards and make a workspace
    #... after adding in the autoMCStats
    for cardName in cardNames:
        cardFile = open(cardName, "a+")
        cardFile.write("* autoMCStats 0.0\n")
        cardFile.close()

    #okay, we need to group the cards up by mass point, because we have to do this mass point
    #by mass point
    #first thing to do, get a list of the available mass points
    massPoints = []
    for cardName in cardNames:
        massPoint = re.search("[0-9]+(?=\.txt)",cardName).group(0)
        if  massPoint not in massPoints:
            massPoints.append(massPoint)

    print("Mass Points in the analysis: ")
    print(massPoints)

    combinedCardNames = []
    for massPoint in massPoints:
        cardCombiningCommand = 'combineCards.py'
        combinedCardName = 'FinalCard_'+theOutputArea.dateTag+'_'+massPoint+'.txt'
        combinedCardNames.append(combinedCardName)
        for cardName in cardNames:
            if re.search('.+_'+massPoint+'\.txt',cardName):
                cardCombiningCommand+= ' '+cardName+' '
        cardCombiningCommand += ' > ' + combinedCardName
        #log it and do it
        logging.info("Mass Point {} Card Combining Command".format(massPoint))
        logging.info("\n\n"+cardCombiningCommand)
        os.system(cardCombiningCommand+' |tee -a ' + outputLoggingFileName)
    
        #Make a workspace? Or workspaces?
        textToWorkspaceCommand = 'text2workspace.py -m '+massPoint+' '+combinedCardName
        logging.info('Mass Point {} Text to workspace command: '.format(massPoint))
        logging.info('\n\n'+textToWorkspaceCommand+'\n')
        os.system(textToWorkspaceCommand+' | tee -a '+outputLoggingFileName)

    print("Finished!")
    theOutputArea.printOutputInfo()
    os.chdir(homePath)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = "script for creating the complete bbtautau datacard setup and logging it")

    args = parser.parse_args()

    main(args)

