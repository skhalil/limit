#! /usr/bin/env python
import sys
from array import array
from ROOT import TH1D,TH2D,TFile,TMath,TCanvas,THStack,TLegend,TPave,TLine,TLatex
from ROOT import gROOT,gStyle,gPad,gStyle
from ROOT import Double,kBlue,kRed,kOrange,kMagenta,kYellow,kCyan,kGreen,kGray,kTRUE

gROOT.Macro("~/rootlogon.C")
gStyle.SetOptStat(0)

def setCosmetics(hist, color, name, leg):
    hist.SetLineColor(color)
    if 'TbtH' in name:
        hist.SetLineWidth(2)
        leg.AddEntry(hist, name, 'l')
    else:
        hist.SetFillColor(color)
        leg.AddEntry(hist, name, 'f')
def prepareCanvas(c2):
    c2.Divide(1,2)
    scale = (1 - 0.3)/0.3

    pad = c2.cd(1)
    pad.SetPad(0, 0.2, 1, 1)
    pad.SetTopMargin(0.1)
    pad.SetLeftMargin(0.13)
    pad.SetRightMargin(0.03)
    pad.SetBottomMargin(0.125)

    pad = c2.cd(2)
    pad.SetPad(0, 0.0, 1, 0.3)
    pad.SetTopMargin(0.0)
    pad.SetLeftMargin(0.13)
    pad.SetRightMargin(0.03)
    pad.SetBottomMargin(0.3)
    pad.SetTickx(1)
    pad.SetTicky(1)

def prepareRatio(h_ratio, h_ratiobkg, xTitle):
    scale = (1 - 0.3)/0.3
    h_ratio.SetTitle("")
    h_ratio.GetYaxis().SetTitle("Data/Bkg")
    h_ratio.GetXaxis().SetTitle(xTitle)

    h_ratio_bkg.SetMarkerSize(0)
    h_ratio_bkg.SetFillColor(kGray+1)
    h_ratio_bkg.SetMaximum(2)
    h_ratio_bkg.SetMinimum(0)
    h_ratio_bkg.GetYaxis().SetLabelSize(0.04*scale)
    h_ratio_bkg.GetYaxis().SetTitleOffset(1.00/scale*0.9)
    h_ratio_bkg.GetYaxis().SetTitleSize(0.06*scale*1.00)
    h_ratio_bkg.GetYaxis().SetTitleFont(42)
    h_ratio_bkg.GetXaxis().SetLabelSize(0.04*scale*1.00)
    h_ratio_bkg.GetXaxis().SetTitleOffset(0.95*scale*0.39)
    h_ratio_bkg.GetXaxis().SetTitleSize(0.06*scale*1.00)
    h_ratio_bkg.GetYaxis().SetNdivisions(505)
    h_ratio_bkg.GetXaxis().SetNdivisions(510)
    h_ratio_bkg.SetTickLength(0.08,"X")

    h_ratio.SetMarkerStyle(8)
    h_ratio.SetMaximum(2)
    h_ratio.SetMinimum(0)
    h_ratio.GetYaxis().SetLabelSize(0.04*scale)
    h_ratio.GetYaxis().SetTitleOffset(1.00/scale*0.9)
    h_ratio.GetYaxis().SetTitleSize(0.06*scale*1.00)
    h_ratio.GetYaxis().SetTitleFont(42)
    h_ratio.GetXaxis().SetLabelSize(0.04*scale*1.00)
    h_ratio.GetXaxis().SetTitleOffset(0.95*scale*0.39)
    h_ratio.GetXaxis().SetTitleSize(0.06*scale*1.00)
    h_ratio.GetYaxis().SetNdivisions(505)
    h_ratio.GetXaxis().SetNdivisions(510)
    h_ratio.SetTickLength(0.08,"X")

def setTitle(hTop, hs, xTitle):
    title = hTop.GetTitle()
    yTitle= hTop.GetYaxis().GetTitle()
    if yTitle == "": yTitle = "Events/bin"
    y = hs.GetYaxis()
    x = hs.GetXaxis()
    y.SetTitle(yTitle)
    x.SetTitle(xTitle)
    y.SetTitleSize(0.05)
    y.SetTitleFont(42)
    x.SetTitleSize(0.05)
    x.SetTitleFont(42)

from optparse import OptionParser
parser = OptionParser()

parser.add_option('--infile', metavar='V', type='string', action='store',
                  default='templates_pT_H_300_pT_top_400_forwardJetsOne_29Sep17.root',#templates_pT_H_300_pT_top_400_29Sep17.root',
                  dest='infile',
                  help='file to read')

parser.add_option('--plot',action='store_true',
                  default=True,
                  dest='plot',
                  help='plot the distribution')

(options,args) = parser.parse_args()
# ==========end: options =============

Path = '../sourceFiles/'
f = TFile(Path+options.infile)
mass = ['800', '900', '1000', '1100', '1200', '1300', '1400', '1500', '1700', '1800']
histMass = []
templates = []
h_top  = f.Get('MTP_regionD_TTJets').Clone()
h_qcd  = f.Get('MTP_regionD_estQCD').Clone() #MC_QCD
h_data = f.Get('MTP_regionD_data_obs').Clone()
templates.append(h_top)
templates.append(h_qcd)

for m in mass:
    print 'MTP_regionD_TbtH_'+m+'_LH'
    h_VLQ =  f.Get('MTP_regionD_TbtH_'+m+'_LH')
    histMass.append(h_VLQ)
    if m == '1200':
        templates.append(h_VLQ)

nBins = h_top.GetNbinsX()
bMin = h_top.GetBinLowEdge(1)
bMax = h_top.GetBinLowEdge(nBins+1)
bin1 = h_top.GetXaxis().FindBin(bMin)
bin2 = h_top.GetXaxis().FindBin(bMax)

integralError = Double(5)

for h in histMass:
    vlq = h.GetName()
    vlq = vlq.replace('MTP_regionD_', '')#.replace('_LH', '')    

    h.IntegralAndError(bin1,bin2,integralError)
    sig = h.Integral(bin1,bin2)  ; sig_e = integralError
    #print '{0:<10} & {1:<7.2f} $\pm$ {2:<7.2f} \n'.format(vlq, sig, sig_e)
    h_top.IntegralAndError(bin1,bin2,integralError)
    top = h_top.Integral(bin1,bin2) ; top_e = integralError
    #print '{0:<10} & {1:<7.2f} $\pm$ {2:<7.2f} \n'.format('ttbar', top, top_e)
    h_qcd.IntegralAndError(bin1,bin2,integralError)
    qcd = h_qcd.Integral(bin1,bin2)  ; qcd_e = integralError
    #print '{0:<10} & {1:<7.2f} $\pm$ {2:<7.2f} \n'.format('qcd', qcd, qcd_e)
    dataName = h_data.GetName().split('_')[2]
    data = h_data.Integral(bin1,bin2)
    
    
 
    binN = 'MTP_regionD'
    d_out = open('datacards/'+vlq+'_card.txt', 'w')
    d_out.write("imax 1  number of channels \n")
    d_out.write("jmax 2  number of backgrounds \n")
    d_out.write("kmax *  number of nuisance parameters \n")
    d_out.write("------------------------------------------- \n")
    d_out.write("shapes * * {0:<8} $CHANNEL_$PROCESS $CHANNEL_$PROCESS_$SYSTEMATIC \n".format(options.infile))#f.GetName()))
    d_out.write("------------------------------------------- \n")

    d_out.write("# we have just one channel, in which we observe x data events \n")
    d_out.write("bin         {0:<8} \n".format(binN))
    d_out.write("observation {0:<8} \n".format(data))#'0'

    d_out.write("# now we list the expected events for sig and all backgrounds in that bin \n")
    d_out.write("# the second 'process' line must have a positive number for backgrounds, and 0 for signal \n")
    d_out.write("# then we list the independent sources of uncertainties, and give their effect (syst. error) \n")
    d_out.write("# on each process and bin \n")
    d_out.write("bin                         {0:<10}  {1:<10}  {2:<10}   \n".format(binN, binN, binN) )
    d_out.write("process                     {0:<10}  {1:<10}  {2:<10}   \n".format(vlq, 'estQCD', 'TTJets'))
    d_out.write("process                     {0:<10}  {1:<10}  {2:<10}   \n".format('0', '1', '2'))
    d_out.write("rate                        {0:<10.4f}  {1:<10.4f}  {2:<10.4f}  \n".format(sig, qcd, top))
    d_out.write("--------------------------------------------------------------------------\n")
   
    d_out.write("lumi         lnN            {0:<10.4f}  {1:<10.4f}  {2:<10.4f}  lumi \n".format(1.026, 0.974/1.026, 1.026/0.974))
    d_out.write("purewt       lnN            {0:<10.4f}  {1:<10.4f}  {2:<10.4f}  pileup \n".format(1.03, 0.97/1.03, 1.03/0.97))
    d_out.write("topxsec      lnN            {0:<10}     {1:<10.4f}  {2:<10.4f}  ttbar norm \n".format('-', 0.938/1.061, 0.938/1.061) )
    d_out.close()

if options.plot:
    leg = TLegend(0.75,0.50,0.95,0.92)
    leg.SetBorderSize(1)
    leg.SetFillColor(10)

    h_data.SetMarkerStyle(8)
    #leg.AddEntry(h_data, "Data 36 fb^{-1}", 'pl')    
    
    setCosmetics(h_top, 8, 'TTJets',leg)
    setCosmetics(h_qcd, 90, 'QCD',leg)
        
    hs = THStack("","")
    for ihist in reversed(templates[0:2]):
        hs.Add(ihist)
        print 'histo added', ihist.GetName()
    if h_VLQ.GetMaximum() > hs.GetMaximum() :
        hs.SetMaximum(h_VLQ.GetMaximum()+6)#+3

    ## Canvas
    c1 = TCanvas('c1', 'c1', 1000, 800)
    #prepareCanvas(c1)
    #c1.cd(1)
    gPad.SetLogy()
    hs.SetMinimum(0.1)
    hs.Draw("Hist")
    it = 0
    for h in histMass:
        sigN = h.GetName().replace('MTP_regionD_', '').replace('_LH', '') 
        setCosmetics(h, kBlue+it, sigN,leg); it = it+2;  
        #if it%2 == 0:
        h.Draw("hist,same")
    #h_data.Draw("esame")
    #setCosmetics(h_VLQ, kBlue, sigN, leg); 
    #h_VLQ.Draw("hist,same")
    leg.Draw()

    ll = TLatex()
    ll.SetNDC(kTRUE)
    ll.SetTextSize(0.04)
    ll.DrawLatex(0.1,0.92, "CMS Preliminary, #sqrt{s} = 13 TeV, 36 fb^{-1}");

    xTitle = 'M_{T}(GeV)'
    setTitle(h_top, hs, xTitle)
    gPad.RedrawAxis()
    
    c1.SaveAs("TMass_FwdJet.pdf")
    c1.SaveAs("TMass-FwdJet.gif")


raw_input("hold on")
