#!/usr/bin/env python
import os
import re
import sys
import time
import commands

from os.path import join, getsize

masspoints = [800, 900, 1000, 1100, 1200, 1300, 1400, 1500, 1700, 1800]
sig = "TbtH"

for m in masspoints:
    print '-----mass = ',m ,' ----------'
    mass = str(m)
    #--rMin=0.001 --rMax=0.2 
    print "combine -n _Expected_"+sig+"_M"+mass+" -M Asymptotic --run=expected datacards/"+sig+"_"+mass+"_LH_card.txt"
    #os.system("combine -M MaxLikelihoodFit --saveShapes --plots --saveWithUncertainties --saveOverallShapes datacards/"+sig+"_"+mass+"_card.txt") # -t -1

    os.system("combine -n _Expected_"+sig+"_M"+mass+" -M Asymptotic --run=expected datacards/"+sig+"_"+mass+"_LH_card.txt")

#os.system("hadd -f higgsCombine_Expected_"+sig+".Asymptotic.root higgsCombine_Expected_"+sig+"_M*.Asymptotic.mH*.root")
#os.system("rm -rf higgsCombine_Expected_"+sig+"_M*.Asymptotic.mH*.root")
os.system("mv higgsCombine_Expected_"+sig+"_M*.Asymptotic.mH*.root limitFiles")
