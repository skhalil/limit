# Scripts to calculate the expected limits for KU single T to tH analysis 

## Setting up Higgs combined tools

    export SCRAM_ARCH=slc6_amd64_gcc530
    cmsrel CMSSW_8_1_0
    cd CMSSW_8_1_0/src 
    cmsenv
    git clone https://github.com/cms-analysis/HiggsAnalysis-CombinedLimit.git HiggsAnalysis/CombinedLimit
    cd HiggsAnalysis/CombinedLimit
        
    git fetch origin
    git checkout v7.0.1 # for bayesian statistics
    scramv1 b clean; scramv1 b # always make a clean build

See the [link](https://twiki.cern.ch/twiki/bin/view/CMS/SWGuideHiggsAnalysisCombinedLimit#ROOT606_SLC6_CMSSW_8_1_X) for the details.

## Checkout the limit calculation and plotting scripts

    cd $CMSSW_BASE/src/HiggsAnalysis/
    git clone https://github.com/skhalil/limit.git limit

## Creating the card files and optionally plotting the input histogram
   
    python datacard.py
  
The script looks for the input root files in a directory <../sourceFiles>, so please keep it available. I usually also make soft links for the input root file in a directory where I execute the combine tool commands. Set the option <--plot> to <False> if not interested in plotting the histogram. The script will write the card files in a directory <datacards>. 

## Run the limits
    
    python runLimits.py

This script will calculate the limits for each mass point, and will move the resultant data root files in a directory <limitFiles>. Please create the directory first, in case the script will complaint about it.

## Plot the limits
   
    python plotLimits.py

This script plots the expected limits by reading them for each quantile in root files located in directory <limitFiles>. The theory x-sections are taken directly from VHF [twiki](https://twiki.cern.ch/twiki/bin/view/CMS/B2GVHF#Vector_like_quark_pair_and_singl). The expected limits are plotted as is as computed by combine tool, without normalizating them to any other number (x-section). To comply with CMS plotting rules, the script uses the following style files <CMS_lumi.py> and <tdrstyle.py>
  
       

  