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

See https://twiki.cern.ch/twiki/bin/view/CMS/SWGuideHiggsAnalysisCombinedLimit#ROOT606_SLC6_CMSSW_8_1_X for the details.

## Checkout the limit calculation and plotting scripts

