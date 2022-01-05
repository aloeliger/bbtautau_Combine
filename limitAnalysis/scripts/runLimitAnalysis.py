#Andrew Loeliger
#quick script for running (expected) CLs frequentist limits as was done by the previous analysis
#on bb tautau cards

import argparse
import os
import re
import logging

from bbtautau_Combine.common.datacardAccessManager import datacardAccessManager

def main(args):
    theDatacardAccessManager = datacardAccessManager(args.dateTag)
    cardNames = theDatacardAccessManager.getCardNames()

    #setup a log of our combine actions
    logging.basicConfig(filename="asymptoticLimitsAnalysisHistory_"+args.dateTag+".log",
                        filemode='w',
                        level=logging.INFO,
                        format='%(asctime)s %(message)s')
    limitOutputFileName = 'asymptoticLimitsAnalysisOutput.txt'
    open(limitOutputFileName, 'w').close()

    #run the combine tool on everything
    for cardName in cardNames:
        massPoint = re.search('[0-9]+(?=\.root)', cardName).group(0)
        print('Mass Point: ')
        print(massPoint)
        with open(limitOutputFileName, 'a+') as theFile:
            theFile.write('Mass Point: \n')
            theFile.write(massPoint+'\n')
            theFile.close()
        limitCommand = 'combineTool.py '+cardName+' -M AsymptoticLimits '
        if not args.unblind:
            limitCommand += '--run blind '
        limitCommand+= '--expectSignal=1 '
        logging.info('Mass Point limit command:'.format(massPoint))
        logging.info('\n\n'+limitCommand+'\n')
        os.system(limitCommand+' | tee -a '+limitOutputFileName)
            

    print("Finished!")
    theDatacardAccessManager.returnToHomePath()

if __name__=='__main__':
    parser = argparse.ArgumentParser(description = 'script for running the (blinded) asymptotic limits of the bbtautau cards')
    parser.add_argument('--dateTag', nargs='?', required=True, help='date tag to find the relevant datacrds for doing the analysis')
    parser.add_argument('--unblind', help='unblind the analysis and do it for real. BE SURE ABOUT THIS.', action='store_true')

    args = parser.parse_args()

    main(args)
