#!/usr/bin/env python
import ROOT
from ROOT import gROOT,gStyle,gPad,gStyle
from ROOT import Double,kBlue,kRed,kOrange,kAzure,kMagenta,kYellow,kCyan,kGreen,kGray,kBlack,kDotted,kTRUE
import imp
import sys
from array import array
from collections import OrderedDict
gROOT.Macro("~/rootlogon.C")
gStyle.SetOptStat(0)

# ===============
# options
# ===============
from optparse import OptionParser
parser = OptionParser()
parser.add_option('--model', metavar='V', type='string', action='store',
                  default='TbtH',
                  dest='model',
                  help='TbtH/TttH/TbtZ')
(options,args) = parser.parse_args()
# ==========end: options =============
model = options.model

def getLimit(model,masses,xs_th):
  print 'model to be plot', model, ' ', masses 
  grexplim = ROOT.TGraph(len(masses))
  grexp1sig = ROOT.TGraphAsymmErrors(len(masses))
  grexp2sig = ROOT.TGraphAsymmErrors(len(masses))
  
  grexplim .SetName('grexplim' +'_'+model) 
  grexp1sig.SetName('grexp1sig'+'_'+model) 
  grexp2sig.SetName('grexp2sig'+'_'+model)
 
  mass_xsec = zip(masses, xs_th)
  for mass, xsec in mass_xsec:
    i = masses.index(mass)
    #xsec = 1.
    f = ROOT.TFile.Open("limitFiles/noFwdJet/higgsCombine_Expected_"+model+"_M"+str(mass)+".Asymptotic.mH120.root", "r")
    limit = f.Get("limit")
    entries = limit.GetEntriesFast()
    obs = 0
    exp = 0
    exp1sLow  = 0
    exp1sHigh = 0
    exp2sLow  = 0
    exp2sHigh = 0
    for e in limit:
      quant = e.quantileExpected
      lim = e.limit
      if quant == -1: obs = lim 
      elif quant > 0.024 and quant < 0.026: exp2sLow = lim 
      elif quant > 0.15 and quant < 0.17: exp1sLow = lim 
      elif quant == 0.5: exp = lim
      elif quant > 0.83 and quant < 0.85: exp1sHigh = lim
      elif quant > 0.97 and quant < 0.98: exp2sHigh = lim 
    grexplim.SetPoint(i, mass, xsec*exp)
    grexp1sig.SetPoint(i, mass, xsec*exp)
    grexp2sig.SetPoint(i, mass, xsec*exp)
    grexp1sig.SetPointError(i, 0, 0, xsec*abs(exp-exp1sLow), xsec*abs(exp1sHigh-exp))
    grexp2sig.SetPointError(i, 0, 0, xsec*abs(exp-exp2sLow), xsec*abs(exp2sHigh-exp))
    print '{0:<2} GeV : {1:<7.2f} fb'.format(mass, xsec*exp*1000)
  return grexplim, grexp1sig, grexp2sig

###___________________________

def plotLimits(model, masses, th_xs):
  grthlim = ROOT.TGraph(len(masses))

  # for theory curve
  map_th  = zip(masses,th_xs)
  p_th=0; 
  for m,x in map_th:
    grthlim.SetPoint(p_th, m, x)
    #print 'm: ', m, 'x: ', x
    p_th +=1

  # expected limit curves
  grexplim, grexp1sig, grexp2sig = getLimit(model, masses, th_xs)
  print grthlim.GetN(), ' ',grexplim.GetN(), ' ', grexp1sig.GetN(), ' ', grexp2sig.GetN(), ' '

  #return
  #cosmetics
  tdrstyle = imp.load_source('tdrstyle', 'tdrstyle.py')
  CMS_lumi = imp.load_source('CMS_lumi', 'CMS_lumi.py')
  ROOT.gROOT.SetBatch()
  ROOT.gROOT.SetStyle("Plain")
  ROOT.gStyle.SetOptStat()
  ROOT.gStyle.SetOptTitle(0)
  ROOT.gStyle.SetPalette(1)
  ROOT.gStyle.SetNdivisions(405,"x");
  ROOT.gStyle.SetEndErrorSize(0.)
  ROOT.gStyle.SetErrorX(0.001)
  ROOT.gStyle.SetPadTickX(1)
  ROOT.gStyle.SetPadTickY(1)

  canv = ROOT.TCanvas("ExpLimit_"+model,"ExpLimit_"+model,800,600)
  pad=canv.GetPad(0)
  pad.SetBottomMargin(.12)
  pad.SetLeftMargin(.12)
  pad.SetLogy()

  grexp2sig.SetFillColor(401)
  grexp2sig.SetLineColor(41)
  grexp1sig.SetFillColor(3)
  grexp1sig.SetLineColor(3)
  grexplim.SetLineWidth(2)
  grexplim.SetLineStyle(7)
 
  ymax = grexp2sig.GetHistogram().GetMaximum()*500.0
  ymin = grexp2sig.GetHistogram().GetMaximum()*0.001 
  print ymax, ymin
  #grthlim.SetMinimum(1.)
  #grthlim.SetMaximum(1000.)
  grthlim.SetLineStyle(kDotted)
  grthlim.SetLineColor(kRed)
  grthlim.SetLineWidth(3)
  grthlim.SetMaximum(ymax)
  grthlim.SetMinimum(ymin)

  grexplim.Draw("al")
  grexp2sig.Draw("3")
  grexp1sig.Draw("3")
  grexplim.Draw("l")
  grthlim.Draw("Lsame")
  ##grthlim.GetXaxis().SetRangeUser(1000.,2000.);

  grexplim.GetXaxis().SetRangeUser(799,3000)  
  grexplim.GetYaxis().SetLabelSize(0.04)
  grexplim.GetYaxis().SetTitleSize(0.04)
  grexplim.GetYaxis().SetTitleOffset(1.20)
  grexplim.GetXaxis().SetLabelSize(0.04)
  grexplim.GetXaxis().SetLabelSize(0.04)
  grexplim.GetXaxis().SetTitleSize(0.04)
  grexplim.GetXaxis().SetNdivisions(506)
  grexplim.GetXaxis().SetTitleOffset(1.12)
  grexplim.GetXaxis().SetLabelFont(62)
  grexplim.GetYaxis().SetLabelFont(62)
  grexplim.GetXaxis().SetTitleFont(62)
  grexplim.GetYaxis().SetTitleFont(62)
  grexplim.GetXaxis().SetNdivisions(510,1);
  grexplim.GetXaxis().SetTitle("M(T) [GeV]")
  if model == 'TbtH':
    grexplim.GetYaxis().SetTitle("#sigma(pp#rightarrow Tbq)#times#font[52]{B}(T#rightarrow tH) [pb]")
  elif model == 'TttH':
    grexplim.GetYaxis().SetTitle("#sigma(pp#rightarrow Ttq)#times#font[52]{B}(T#rightarrow tH) [pb]")
  
  grexplim.SetMinimum(ymin)
  grexplim.SetMaximum(ymax)
  
  text = ["CMS"]
  textsize = 0.028; 
  ntxt = 0
  nleglines = 5.

  xstart = 0.50;
  ystart = 0.60; 
  ystartleg = 0.95 

  legend = ROOT.TLegend(xstart, ystart, xstart+0.45, ystartleg)
  legend.SetFillColor(0)
  legend.SetBorderSize(0)
  legend.SetTextSize(textsize)
  legend.SetColumnSeparation(0.0)
  legend.SetEntrySeparation(0.1)
  legend.SetMargin(0.2)
  legend.SetHeader("")
  legend.AddEntry(grexplim  , "Expected ","l")
  legend.AddEntry(grexp1sig , "1 s.d.","f")
  legend.AddEntry(grexp2sig , "2 s.d.","f")
  
  if model == 'TbtH':
    legend.AddEntry(grthlim, "Tbq, c^{bW}_{L}=0.5, #bf{#it{#Beta}}(T #rightarrow tH)=25%", "l") 
  if model == 'TttH':
    legend.AddEntry(grthlim, "Ttq, c^{tZ}_{R}=0.5, #bf{#it{#Beta}}(T #rightarrow tH)=50%", "l")
  
  legend.Draw()
  
  ### Embellishment
  CMS_lumi.lumi_13TeV = ""
  CMS_lumi.writeExtraText = 1
  CMS_lumi.extraText = "Preliminary"
   
  iPos = 11 ###HTshape
  if( iPos==0 ): CMS_lumi.relPosX = 0.12
  CMS_lumi.CMS_lumi(pad, 4, iPos)
  
  latex = ROOT.TLatex()
  latex.SetNDC()
  latex.SetTextAlign(13)
  latex.SetTextSize(0.04)
  latex.SetTextFont(62);
  latex.DrawLatex(0.68, 0.95, "36 fb^{-1} (13 TeV)")
  
  pad.RedrawAxis()
  
  pad.Update()
  ###
  
  for end in [".pdf",".png", ".root"]:
    canv.SaveAs("ExpLim_TbtH_13TeV_"+model+"_03Oct2017"+end)

####_______________________________________________________________________________________
masses = [800, 900, 1000, 1100, 1200, 1300, 1400, 1500, 1700, 1800]
c = 0.5

if model == 'TbtH':
  br = 0.25
  xs = [3.860, 2.720, 1.950, 1.350, 0.982, 0.716, 0.540, 0.408, 0.230, 0.174]
   
if model == 'TttH':
  br = 0.50
  xs = [0.365, 0.271, 0.203, 0.152, 0.116, 0.0894, 0.0692, 0.0540, 0.0330, 0.0259] 

xs_th = [a*br*c*c for a in xs]

plotLimits(model, masses, xs_th)

raw_input("hold on")
