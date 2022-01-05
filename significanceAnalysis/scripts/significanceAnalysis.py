#Andrew Loeliger
#quick script for running the significance analysis of made bbtautau cards

import argparse
import os
import re
import logging

from bbtautau_Combine.common.datacardAccessManager import datacardAccessManager

def main(args):
    #hand off the datacard accessing to the module and get the cards
    theDatacardAccessManager = datacardAccessManager(args.dateTag)
    cardNames = theDatacardAccessManager.getCardNames()

    #setup a log to let us know what it is we did here.

    logging.basicConfig(filename="significanceAnalysisHistory_"+args.dateTag+".log",
                        filemode="w",
                        level=logging.INFO,
                        format='%(asctime)s %(message)s')
    significanceOutputFileName = 'significanceAnalysisOutput.txt'
    open(significanceOutputFileName, 'w').close()
    
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
    theDatacardAccessManager.returnToHomePath()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = "script for running the (blinded) signficances of the bbtautau cards")
    parser.add_argument('--dateTag',nargs='?', required=True, help='date tag to find the relvant datacards for doing the analysis from')
    parser.add_argument('--unblind', help='Unblind the analysis and do it for real. BE SURE ABOUT THIS.', action='store_true')
    
    args = parser.parse_args()

    main(args)
