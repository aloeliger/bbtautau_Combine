#Andrew Loeliger
#quick script for running the significance analysis of made bbtautau cards

import argparse
import os
import re
import logging

def main(args):
    #okay. First things first. Let's go and find the cards that we need to use
    homePath = os.getcwd()

    #construct the spot the datacards are supposed to be:
    outputPath = os.environ['CMSSW_BASE']+'/src/bbtautau_Combine/output/Output_'+args.dateTag
    if not os.path.isdir(outputPath):
        print("Couldn't find the output path. Check the date tag.")
        exit(-1)
        
    os.chdir(outputPath)
    
    #get the cards
    cardNames = filter(lambda x: re.match("FinalCard.+[0-9]\.root", x), os.listdir("./"))

    #print("Card names:")
    #print(cardNames)

    #setup a log to let us know what it is we did here.

    logging.basicConfig(filename="significanceAnalysisHistory_"+args.dateTag+".log",
                        filemode="w",
                        level=logging.INFO,
                        format='%(asctime)s %(message)s')
    significanceOutputFileName = 'significanceAnalysisOutput.txt'
    
    #Okay. Now, we run the combine tool over these and get blinded significances
    for cardName in cardNames:
        #get the mass point of the card we're working with'
        massPoint = re.search('[0-9]+(?=\.root)',cardName).group(0)
        print('Mass Point: ')
        print(massPoint)
        with open(significanceOutputFileName, 'a+') as theFile:
            theFile.write('Mass Point: \n')
            theFile.write(massPoint+'\n')
            theFile.close()
        significanceCommand = 'combineTool.py '+cardName+' -M Significance '
        if not args.unblind:
            significanceCommand += '-t -1 '
        significanceCommand+='--expectSignal=1 '
        logging.info('Mass Point {} signficance command:'.format(massPoint))
        logging.info('\n\n'+significanceCommand+'\n')
        os.system(significanceCommand+' | tee -a '+significanceOutputFileName)

    print("Finished!")
    os.chdir(homePath)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = "script for running the (blinded) signficances of the bbtautau cards")
    parser.add_argument('--dateTag',nargs='?', required=True, help='date tag to find the relvant datacards for doing the analysis from')
    parser.add_argument('--unblind', help='Unblind the analysis and do it for real. BE SURE ABOUT THIS.', action='store_true')
    
    args = parser.parse_args()

    main(args)
