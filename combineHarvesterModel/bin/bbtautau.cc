//primary model for the bbtautau analysis
#include <string>
#include <map>
#include <set>
#include <iostream>
#include <utility>
#include <vector>
#include <cstdlib>
#include "CombineHarvester/CombineTools/interface/CombineHarvester.h"
#include "CombineHarvester/CombineTools/interface/Observation.h"
#include "CombineHarvester/CombineTools/interface/Process.h"
#include "CombineHarvester/CombineTools/interface/Utilities.h"
#include "CombineHarvester/CombineTools/interface/Systematics.h"
#include "CombineHarvester/CombineTools/interface/BinByBin.h"
#include "CombineHarvester/CombineTools/interface/AutoRebin.h"

using namespace std;

int main(int argc, char **argv)
{
  //shapes location
  string auxShapes = string(getenv("CMSSW_BASE")) + "/src/bbtautau_Combine/combineHarvesterModel/data/";

  //Analysis categories
  ch::Categories cats = {
    {1, "all"}
  };
  
  //We need this for signal mass points later
  vector< string > signalMasses = {"1000","1200","1400","1600","1800","2000","2500","3000","3500","4000","4500"};

  //Add data observations. No differences between mass points
  ch::CombineHarvester cb;
  cb.AddObservations({"*"},
		     {"bbtt"},
		     {"2016"},
		     {"mt"},
		     cats);
  
  //Add background processes. These are also not distinct between signal mass points
  vector< string > bkgProcs = {"DY", "QCD", "WJets", "TT", "ST", "VV"};
  cb.AddProcesses({"*"},
		  {"bbtt"},
		  {"2016"},
		  {"mt"},
		  bkgProcs,
		  cats,
		  false);

  //Add the one signal. This has multiple mass points.
  vector< string > sigProcs = {"RadionHH"};
  cb.AddProcesses(signalMasses,
		  {"bbtt"},
		  {"2016"},
		  {"mt"},
		  sigProcs,
		  cats,
		  true);
  
  // ******************************
  // *          lNN               *
  // ******************************

  //Higgs branching ratio uncertainties
  cb.cp().signals().AddSyst(cb, "BR_hbb_THU", "lnN", ch::syst::SystMapAsymm<>::init(1.0065, 1.0065));
  cb.cp().signals().AddSyst(cb, "BR_hbb_PU_mq", "lnN", ch::syst::SystMapAsymm<>::init(1.0072, 1.0074));
  cb.cp().signals().AddSyst(cb, "BR_hbb_PU_alphas", "lnN", ch::syst::SystMapAsymm<>::init(1.0077, 1.0079));

  cb.cp().signals().AddSyst(cb, "BR_htt_THU", "lnN", ch::syst::SystMapAsymm<>::init(1.0117, 1.0116));
  cb.cp().signals().AddSyst(cb, "BR_htt_PU_mq", "lnN", ch::syst::SystMapAsymm<>::init(1.0098, 1.0098));
  cb.cp().signals().AddSyst(cb, "BR_htt_PU_alphas", "lnN", ch::syst::SystMapAsymm<>::init(1.0062, 1.0060));

  //XS uncertainties
  
  //TODO: Verify these. Especially the QCD one.
  cb.cp().process({"TT"}).AddSyst(cb, "CMS_htt_hbb_tjXsec", "lnN", ch::syst::SystMap<>::init(1.042));
  cb.cp().process({"VV"}).AddSyst(cb, "CMS_htt_hbb_vvXsec", "lnN", ch::syst::SystMap<>::init(1.05));
  cb.cp().process({"ST"}).AddSyst(cb, "CMS_htt_hbb_stXsec", "lnN", ch::syst::SystMap<>::init(1.05));
  cb.cp().process({"DY"}).AddSyst(cb, "CMS_htt_hbb_zjXsec", "lnN", ch::syst::SystMap<>::init(1.02));
  cb.cp().process({"QCD"}).AddSyst(cb, "CMS_htt_hbb_qcdXsec", "lnN", ch::syst::SystMap<>::init(1.003));

  //Lumi Uncertainties
  //TODO: Verify that this is the correct scheme for UL samples

  cb.cp().era({"2016"}).AddSyst(cb, "lumi_13TeV_2016", "lnN", ch::syst::SystMap<>::init(1.010));
  cb.cp().AddSyst(cb, "lumi_13TeV_correlated", "lnN", ch::syst::SystMap<>::init(1.006));

  
  //TODO: add quite a few missing lnN's

  // ******************************
  // *         Shapes             *
  // ******************************

  //TODO: add quite a few missing shapes

  //Extract all the shapes
  cb.cp().backgrounds().ExtractShapes(
				      auxShapes + "bbtt_2016_mt.root",
				      "$BIN/$PROCESS",
				      "$BIN/$PROCESS_$SYSTEMATIC");
  cb.cp().signals().ExtractShapes(
				  auxShapes + "bbtt_2016_mt.root",
				  "$BIN/$PROCESS$MASS",
				  "$BIN/$PROCESS$MASS_$SYSTEMATIC");
  //Write cards out
  set< string > bins = cb.bin_set();

  //file to store output shapes in
  TFile output("bbtt.input.root","RECREATE");
  
  for (auto b : bins)
    {
      for (auto m : signalMasses)
	{
	  cout<<">> Writing datacard for bin: " << b << " and mass: "<< m <<endl;
	  cb.cp().bin({b}).mass({m, "*"}).WriteDatacard(b + "_" + m +".txt", output);
	}
    }
}
