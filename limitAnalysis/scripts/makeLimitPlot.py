#Andrew Loeliger
#Using limit analysis output, create expected limits of the analysis

import argparse
import os
import re
import ROOT
from array import array

#function that will take each of the mass point "text blocks" from the output text file
#and process it down into the relevant numbers
# mass point, 2 sigma down, 1 sigma down, center, 1 sigma up, 2 sigma up
def takeOutputAndReturnDictionary(textBlock):
    splitTextBlock = textBlock.split('\n')
    massPoint = splitTextBlock[0]
    #now, let's go through and drop anything that doesn't have a mention of the paramter ' r '
    for line in splitTextBlock:
        if '2.5%:' in line:
            twoSigmaDownString = re.search("[0-9]+\.[0-9]+(?!%)", line).group(0)
            twoSigmaDownFloat = float(twoSigmaDownString)
        if '16.0%:' in line:
            oneSigmaDownString = re.search("[0-9]+\.[0-9]+(?!%)", line).group(0)
            oneSigmaDownFloat = float(oneSigmaDownString)
        if '50.0%:' in line:
            centralValueString = re.search("[0-9]+\.[0-9]+(?!%)", line).group(0)
            centralValueFloat = float(centralValueString)
        if '84.0%:' in line:
            oneSigmaUpString = re.search("[0-9]+\.[0-9]+(?!%)", line).group(0)
            oneSigmaUpFloat = float(oneSigmaUpString)
        if '97.5%:' in line:
            twoSigmaUpString = re.search("[0-9]+\.[0-9]+(?!%)", line).group(0)
            twoSigmaUpFloat = float(twoSigmaUpString)
    #arrange the values
    valuesDict = {
        'twoSigmaDown': twoSigmaDownFloat,
        'oneSigmaDown': oneSigmaDownFloat,
        'centralValue': centralValueFloat,
        'oneSigmaUp': oneSigmaUpFloat,
        'twoSigmaUp': twoSigmaUpFloat,
    }
    return massPoint, valuesDict

#assemble a dictionary of mass points, and value dictionaries
def assembleCompleteDictionary(massPointContentList):
    completeDict = {}
    for massPointText in massPointContentList:
        massPoint, values = takeOutputAndReturnDictionary(massPointText)
        completeDict[massPoint] = values
    return completeDict
            
def main(args):
    homePath = os.getcwd()
    outputPath = os.environ['CMSSW_BASE']+'/src/bbtautau_Combine/output/Output_'+args.dateTag
    os.chdir(outputPath)
    #Find the output file
    limitOutputFileName = 'asymptoticLimitsAnalysisOutput.txt'
    with open(limitOutputFileName, 'r') as theOutputFile:
        theFileContents = theOutputFile.read()
        massPointContents = theFileContents.split('Mass Point: \n')

    #cut the empty entry out
    massPointContents = massPointContents[1:len(massPointContents)+1]
    graphDictionary = assembleCompleteDictionary(massPointContents)
    #okay. Now we need to start assempling the graph that is doing to hold our shapes.
    #We're going to want two tgraph asymm errors

    oneSigmaGraph = ROOT.TGraphAsymmErrors()
    twoSigmaGraph = ROOT.TGraphAsymmErrors()
    centralValueGraph = ROOT.TGraphAsymmErrors()

    oneSigmaGraph.Set(len(graphDictionary))
    twoSigmaGraph.Set(len(graphDictionary))
    centralValueGraph.Set(len(graphDictionary))

    nPoint = 0
    for massPoint in graphDictionary:

        oneSigmaGraph.SetPoint(nPoint, float(massPoint), graphDictionary[massPoint]['centralValue'])
        twoSigmaGraph.SetPoint(nPoint, float(massPoint), graphDictionary[massPoint]['centralValue'])
        centralValueGraph.SetPoint(nPoint, float(massPoint), graphDictionary[massPoint]['centralValue'])

        oneSigmaGraph.SetPointEYhigh(nPoint, abs(graphDictionary[massPoint]['oneSigmaUp']-graphDictionary[massPoint]['centralValue']))
        oneSigmaGraph.SetPointEYlow(nPoint, abs(graphDictionary[massPoint]['oneSigmaDown']-graphDictionary[massPoint]['centralValue']))

        twoSigmaGraph.SetPointEYhigh(nPoint, abs(graphDictionary[massPoint]['twoSigmaUp']-graphDictionary[massPoint]['centralValue']))
        twoSigmaGraph.SetPointEYlow(nPoint, abs(graphDictionary[massPoint]['twoSigmaDown']-graphDictionary[massPoint]['centralValue']))
        
        nPoint += 1

    oneSigmaGraph.Sort()
    twoSigmaGraph.Sort()
    centralValueGraph.Sort()

    centralValueGraph.SetLineColor(1)
    centralValueGraph.SetLineStyle(7)
        
    oneSigmaGraph.SetLineColor(1)
    oneSigmaGraph.SetLineStyle(7)
    oneSigmaGraph.SetFillColor(3)
    oneSigmaGraph.SetFillStyle(1001)

    twoSigmaGraph.SetLineColor(1)
    twoSigmaGraph.SetLineStyle(7)
    twoSigmaGraph.SetFillColor(5)
    twoSigmaGraph.SetFillStyle(1001)

    graphCanvas = ROOT.TCanvas()
    graphCanvas.SetLogy()
    graphCanvas.SetGridx()
    graphCanvas.SetGridy()

    #twoSigmaGraph.Draw('ACF')
    #oneSigmaGraph.Draw('ALX4')
    twoSigmaGraph.SetMinimum(10E-4)
    twoSigmaGraph.SetMaximum(10E3)
    twoSigmaGraph.Draw('A3')
    oneSigmaGraph.Draw('3')
    centralValueGraph.Draw("L")

    twoSigmaGraph.GetXaxis().SetTitle("m_{x} (GeV)")
    twoSigmaGraph.GetXaxis().CenterTitle()
    twoSigmaGraph.GetYaxis().SetTitle("#sigma_{95%} #times BR(X #rightarrow HH)[pb]")
    twoSigmaGraph.GetYaxis().CenterTitle()

    #let's draw the other text pieces.
    cmsLatex = ROOT.TLatex()
    #cmsLatex.SetTextSize(0.09)
    cmsLatex.SetNDC(True)
    cmsLatex.SetTextFont(61)
    cmsLatex.SetTextAlign(11)
    cmsLatex.DrawLatex(0.1,0.92,"CMS")
    cmsLatex.SetTextFont(52)
    cmsLatex.DrawLatex(0.1+0.09,0.92,"Preliminary")
    
    lumiText = ""
    
    if args.lumi == '2016APV':
        lumiText = '19.52 fb^{-1}'
    elif args.lumi == '2016':
        lumiText = '16.81 fb^{-1}'
    elif args.lumi == '2017':
        lumiText = '41.48 fb^{-1}'
    elif args.lumi == '2018':
        lumiText = '59.83 fb^{-1}'
    elif args.lumi == 'Run2':
        lumiText = "137 fb^{-1}"
    lumiText += " (13TeV)"

    cmsLatex.SetTextAlign(31)
    cmsLatex.SetTextFont(42)
    cmsLatex.DrawLatex(0.9,0.92, lumiText)

    #draw in a legend
    theLegend = ROOT.TLegend(0.5, 0.6, 0.88, 0.88)
    theLegend.AddEntry(twoSigmaGraph, "Asympt. CL_{s} Expected #pm 1#sigma", "FL")
    theLegend.AddEntry(oneSigmaGraph, "Asympt. CL_{s} Expected #pm 2#sigma", "FL")
    theLegend.SetLineColor(0)
    theLegend.Draw()


    graphCanvas.SaveAs("testLimits.png")

if __name__=='__main__':
    parser = argparse.ArgumentParser(description = 'script for creating the asymptotic limit plot')
    parser.add_argument('--dateTag',nargs='?', required=True, help='date tag to go and find the relvant output for creating the plot')
    parser.add_argument('--lumi', nargs='?', choices = ['2016APV', '2016', '2017', '2018', 'Run2'], default = '2016', help='luminosity to draw on the top of the plot')

    args = parser.parse_args()

    main(args)
