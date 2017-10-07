#!/usr/bin/env python
import os
import re
import sys
import time
import commands

from os.path import join, getsize

masspoints = [800, 900, 1000, 1100, 1200, 1300, 1400, 1500, 1700, 1800]
sig = "TbtH"
#cardDir = 'datacards/Oct17/templates_H_pT_300_top_pT_400_4Oct17'
#cardDir = 'datacards/Oct17/templates_pT_H_300_pT_top_400_noIsoLeptons_4Oct17'
#cardDir = 'datacards/Oct17/templates_pT_H_300_pT_top_400_forwardJetOne_4Oct17'
#cardDir = 'datacards/Oct17/templates_pT_H_300_pT_top_400_extraJetOne_4Oct17'
#cardDir = 'datacards/Oct17/templates_pT_H_300_pT_top_400_extraForwardJetOne_4Oct17'
cardDir = 'datacards/Oct17/templates_2015_ht1100_H_pT_300_top_pT_500_4Oct17'
for m in masspoints:
    print '-----mass = ',m ,' ----------'
    mass = str(m)
    #--rMin=0.001 --rMax=0.2 
    print "combine -n _Expected_"+sig+"_M"+mass+" -M AsymptoticLimits --run=expected "+cardDir+"/"+sig+"_"+mass+"_LH_card.txt -t -1"
    #os.system("combine -M MaxLikelihoodFit --saveShapes --plots --saveWithUncertainties --saveOverallShapes datacards/"+sig+"_"+mass+"_card.txt") # -t -1

    os.system("combine -n _Expected_"+sig+"_M"+mass+" -M AsymptoticLimits --run=expected "+cardDir+"/"+sig+"_"+mass+"_LH_card.txt -t -1")

#os.system("hadd -f higgsCombine_Expected_"+sig+".Asymptotic.root higgsCombine_Expected_"+sig+"_M*.Asymptotic.mH*.root")
#os.system("rm -rf higgsCombine_Expected_"+sig+"_M*.Asymptotic.mH*.root")
os.system("mv higgsCombine_Expected_"+sig+"_M*.AsymptoticLimits.mH*.root limitFiles/"+cardDir.replace('datacards/', ''))
