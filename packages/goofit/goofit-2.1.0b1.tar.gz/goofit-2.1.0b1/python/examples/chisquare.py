#!/usr/bin/env python
# -*- coding: utf-8 -*-

from goofit import *

import numpy as np
import math


decayTime  = Observable("decayTime",0,10)
constaCoef = Variable("constaCoef",0)
linearCoef = Variable("linearCoef",0)
secondCoef = Variable("secondCoef",0)

def integralExpCon(lo, hi):
    return(np.exp(-lo) - np.exp(-hi))

def integralExpLin(lo, hi):
    return((lo + 1) * np.exp(-lo) - (hi + 1) * np.exp(-hi))

def integralExpSqu(lo, hi):
    return((lo * lo + 2 * lo + 2) * np.exp(-lo) - (hi * hi + 2 * hi + 2) * np.exp(-hi))

def generateEvents(rsEvtVec, wsEvtVec,decayTime,conCoef,linCoef,squCoef,eventsToGenerate):
    print("generateEvents")
    totalRSintegral = integralExpCon(0, 100)
    step            = (decayTime.upperlimit - decayTime.lowerlimit) / decayTime.numbins

    i=0
    while i < decayTime.numbins:

        binStart = i * step
        binStart += decayTime.lowerlimit
        binFinal = binStart + step

        rsIntegral = integralExpCon(binStart, binFinal)
        wsIntegral = conCoef * integralExpCon(binStart, binFinal)
        wsIntegral += linCoef * integralExpLin(binStart, binFinal)
        wsIntegral += squCoef * integralExpSqu(binStart, binFinal)

        expectedRSevts = eventsToGenerate * rsIntegral / totalRSintegral
        expectedWSevts = eventsToGenerate * wsIntegral / totalRSintegral

        rsEvts  = np.random.poisson(expectedRSevts)
        wsEvts  = np.random.poisson(expectedWSevts)
        rsEvtVec = np.append(rsEvtVec,rsEvts)
        wsEvtVec = np.append(wsEvtVec,wsEvts)

        if 0 == (i % 10):
            print ("Events in bin",i,"i",rsEvts,"(",expectedRSevts,")",wsEvts," (",expectedWSevts,")\n")

        i+=1


def fitRatio(rsEvts, wsEvts, plotName = ""):
    #ratioHist = TH1D("ratioHist", "", decayTime.numbins, decayTime.lowerlimit, decayTime.upperlimit)
    print("fitRatio")
    ratioData = BinnedDataSet(decayTime)

    i=0
    print("hi")
    while i < wsEvts.size:

        ratio = wsEvts[i]

        if 0 == rsEvts[i]:
            rsEvts[i] = 1 #Cheating to avoid div by zero.

        ratio /= rsEvts[i]

        if 0 == wsEvts[i]:
            wsEvts[i] = 1 #Avoid zero errors

        error = wsEvts[i] / pow(rsEvts[i], 2)
        error += pow(wsEvts[i], 2) / pow(rsEvts[i], 3)
        error = math.sqrt(error)

        ratioData.setBinContent(i, ratio)
        ratioData.setBinError(i, error)
        ratioHist.SetBinContent(i + 1, ratio)
        ratioHist.SetBinError(i + 1, error)
        i+=1

    constaCoef = Variable("constaCoef", 0.03, 0.01, -1, 1)
    constaCoef.value = 0.03
    constaCoef.error=0.01
    linearCoef = Variable("linearCoef", 0, 0.01, -1, 1)
    linearCoef.value=0.00
    linearCoef.error=0.01
    secondCoef = Variable("secondCoef", 0, 0.01, -1, 1)
    secondCoef.value=0.00
    secondCoef.error=0.01

    weights = (constaCoef,linearCoef,secondCoef)

    poly = PolynomialPdf("poly", decayTime, weights)
    poly.setFitControl = BinnedErrorFit()#NEED TO BE BINDED
    poly.setData(ratioData)
    fitter = FitManager(poly)
    fitter.fit()

    values = poly.evaluateAtPoints(decayTime)
    pdfHist = TH1D("pdfHist", "", decayTime.numbins, decayTime.lowerlimit, decayTime.upperlimit)


    return datapdf

def cpvFitFcn(npar, gin, fun, fp, iflag):
    print(cpvFitFcn)
    conCoef = fp[0]
    linCoef = fp[1]
    squCoef = fp[2]

    chisq = 0
    step  = (decayTime.upperlimit - decayTime.lowerlimit) / decayTime.numbins

    i=0
    while i < ratios.size():
        currDTime = decayTime.lowerlimit + (i + 0.5) * step
        pdfval    = conCoef + linCoef * currDTime + squCoef * currDTime * currDTime
        chisq += pow((pdfval - ratios[i]) / errors[i], 2)
        i+=1

    fun = chisq


def fitRatioCPU(rsEvts, wsEvts):
    print("fitRatioCPU")
    ratioHist = TH1D("ratioHist", "", decayTime.numbins, decayTime.lowerlimit, decayTime.upperlimit)

    ratios.resize(wsEvts.size())
    errors.resize(wsEvts.size())

    i=0
    while i < wsEvts.size():
        ratio = wsEvts[i]

        if 0 == rsEvts[i]:
            rsEvts[i] = 1 # Cheating to avoid div by zero.

        ratio /= rsEvts[i]

        if 0 == wsEvts[i]:
            wsEvts[i] = 1 # Avoid zero errors

        error = wsEvts[i] / pow(rsEvts[i], 2)
        error += pow(wsEvts[i], 2) / pow(rsEvts[i], 3)
        error = sqrt(error)

        ratios[i] = ratio
        errors[i] = error
        ratioHist.SetBinContent(i + 1, ratio)
        ratioHist.SetBinError(i + 1, error)
        i+=1

def main():
    print("main")
    rSubD = 0.03
    rBarD = 0.03
    delta = 0
    wpPhi = 0
    x_mix = 0.0016
    y_mix = 0.0055
    magPQ = 1.0
    magQP = 1.0 / magPQ

    eventsToGenerate = 10000000

    dZeroEvtsWS = np.array([])
    dZeroEvtsRS = np.array([])
    d0barEvtsWS = np.array([])
    d0barEvtsRS = np.array([])

    dZeroLinearCoef = magPQ * math.sqrt(rSubD) * (y_mix * math.cos(delta + wpPhi) - x_mix * math.sin(delta + wpPhi))
    d0barLinearCoef = magQP * math.sqrt(rBarD) * (y_mix * math.cos(delta - wpPhi) - x_mix * math.sin(delta - wpPhi))

    dZeroSecondCoef = 0.25 * magPQ * magPQ * (x_mix * x_mix + y_mix * y_mix)
    d0barSecondCoef = 0.25 * magQP * magQP * (x_mix * x_mix + y_mix * y_mix)

    generateEvents(dZeroEvtsRS, dZeroEvtsWS, decayTime, rSubD, dZeroLinearCoef, dZeroSecondCoef, eventsToGenerate)
    generateEvents(d0barEvtsRS, d0barEvtsWS, decayTime, rBarD, d0barLinearCoef, d0barSecondCoef, eventsToGenerate)

    gpuTime = 0
    cpuTime = 0

    retval = fitRatio(dZeroEvtsRS, dZeroEvtsWS, "dzeroEvtRatio.png")
    if retval != 0:
        return retval

    timersub(stopTime, startTime, totalTime)
    gpuTime += totalTime.tv_sec + totalTime.tv_usec / 1000000.0
    retval = fitRatio(d0barEvtsRS, d0barEvtsWS, "dzbarEvtRatio.png")
    if retval != 0:
        return retval

    timersub(stopTime, startTime, totalTime)
    gpuTime += totalTime.tv_sec + totalTime.tv_usec / 1000000.0

    fitRatioCPU(dZeroEvtsRS, dZeroEvtsWS)
    timersub(stopTime, startTime, totalTime)
    cpuTime += totalTime.tv_sec + totalTime.tv_usec / 1000000.0
    fitRatioCPU(d0barEvtsRS, d0barEvtsWS)
    timersub(stopTime, startTime, totalTime)
    cpuTime += totalTime.tv_sec + totalTime.tv_usec / 1000000.0


    print( "GPU time [seconds] : ",gpuTime,"\nCPU time [seconds] : ",cpuTime)
    return 0;

main()
