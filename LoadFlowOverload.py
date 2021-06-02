from __future__ import division
import pandas as pd
import csv
import math
import lookup
from datetime import datetime

import pickle
import numpy as np
import time
from pytz import timezone
import sys
import difflib
import os


CYMPY_LOCATION = r"C:\Program Files (x86)\CYME\CYME 7.1"
sys.path.insert(1, CYMPY_LOCATION)
import cympy
import cympy.rm
import cympy.db
import cympy.study
import cympy.enums



import function_study_analysis
import ModifySpotLoad
from definitions import *
import random

def BaseNulls(model_filename):
    '''
    BaseNulls is the function responsible for pulling the number of errorous results from the base case
    These base values will be compared to each Load Flow overload start to ensure CYME doesn't have new errors
    '''
    start=datetime.now()
    cympy.study.Open(model_filename)
    lf = cympy.sim.LoadFlow()
    lf.Run()

    xfmr = function_study_analysis.list_devices(cympy.enums.DeviceType.Transformer)
    xfmr_byphase = function_study_analysis.list_devices(cympy.enums.DeviceType.TransformerByPhase)
    cable = function_study_analysis.list_devices(cympy.enums.DeviceType.OverheadByPhase)

    BaseXfmrNull = 0
    BaseXfmrByBhaseNull = 0
    BaseLineNull = 0
    XfmrNullName=[]
    XfmrByPhaseNullName=[]
    LineNullName=[]

    #This loop looks for invalid QueryInfoDevice, incrementing the asset bassnull value and
    #collecting the errorous asset name
    for name in xfmr['device_number']:
        if cympy.study.QueryInfoDevice("LOADING", name, 1) == '':
            BaseXfmrNull = BaseXfmrNull + 1
            XfmrNullName.append(name)

    for name in xfmr_byphase['device_number']:
        if cympy.study.QueryInfoDevice("LOADING", name, 33) == '':
            BaseXfmrByPhaseNull = BaseXfmrByBhaseNull + 1
            XfmrByPhaseNullName.append(name)

    for name in cable['device_number']:
        if cympy.study.QueryInfoDevice("LOADING", name, 13) == '':
            BaseLineNull = BaseLineNull + 1
            LineNullName.append(name)

    cympy.study.Close(False)
    end=datetime.now()
    print('BaseNulls Cars Done in ' + str((end - start).total_seconds()) + ' seconds')
    return BaseXfmrNull, BaseXfmrByBhaseNull, BaseLineNull, XfmrNullName, XfmrByPhaseNullName, LineNullName

def ArrayCreation(data):
    print data
    print type(data)
    dtype = [('Penetration', float)]


    dtype_new_column=('Transformers',float)
    dtype.append(dtype_new_column)
    dtype_new_column = ('TransformersByPhase', float)
    dtype.append(dtype_new_column)
    dtype_new_column = ('OverheadLines', float)
    dtype.append(dtype_new_column)



    print dtype

    nd = np.array(data, dtype=dtype)

    end_Real = datetime.now()

    print 'Overloads'
    print nd
    print type(nd)
    print nd['Penetration']
    print type(nd['Penetration'])
    print nd['Transformers']
    print nd['TransformersByPhase']
    print nd['OverheadLines']
    exit()


    return nd

def loadflow(data, truePen, xfmrStorage, xfmr_byphaseStorage,xfmr_cableStorage, aplace, BaseXfmrNull, BaseXfmrByBhaseNull, BaseLineNull, IntentionalNameStorage,IntentionalValueStorage, appliedNameStorage):
    '''
    loadflow is the section where loading values are found and calculated, and placed in their storage areas
    '''

    #Beginning of the row for total overloads
    start_phrase='({pen}'.format(pen=truePen)


    xfmr = function_study_analysis.list_devices(cympy.enums.DeviceType.Transformer)
    xfmr_byphase = function_study_analysis.list_devices(cympy.enums.DeviceType.TransformerByPhase)
    cable = function_study_analysis.list_devices(cympy.enums.DeviceType.OverheadByPhase)

    xfmrAppend = [[]]*(len(xfmr))
    ByPhaseAppend = [[]]*(len(xfmr_byphase))
    LineAppend = [[]]*(len(cable))

    #Runs a validity check on the study, to ensure no load flow problems
    reset=ValidityCheck(xfmr, xfmr_byphase, cable, BaseXfmrNull, BaseXfmrByBhaseNull, BaseLineNull)

    #If the validity check failed return to the penetration loop
    if reset == 1:
        return data,  reset, xfmrStorage, xfmr_byphaseStorage, xfmr_cableStorage, aplace

    device_increment=0
    xfmrOverload = 0
    IntentionalInt=0
    IntPhrase=start_phrase
    IntapplyPhrase = start_phrase
    #Loops through each of the transformer names
    if len(IntentionalNameStorage) == 0:
        IntentionalNameStorage.append('123456789')
    for name in xfmr['device_number']:
        print IntentionalInt
        if name == IntentionalNameStorage[IntentionalInt]:
            print IntentionalInt
            IntentionalInt=IntentionalInt+1
            print IntentionalInt
            IntPhrase=IntPhrase+",{val}".format(val=float(cympy.study.QueryInfoDevice("LOADING", name, deviceID)))
            IntapplyPhrase = IntapplyPhrase + ",{val}".format(val=name)
            if IntentionalInt == len(IntentionalNameStorage):
                IntPhrase=IntPhrase+")"
                IntapplyPhrase=IntapplyPhrase+')'



        #Transformers deviceID is 1
        deviceID=1
        #Checks too see if Query result is valid
        if cympy.study.QueryInfoDevice("LOADING", name, deviceID) != '':

            xfmrAppend[device_increment] = (truePen, name, float(cympy.study.QueryInfoDevice("LOADING", name, deviceID)))
        else:
            xfmrAppend[device_increment] = (truePen,name, 0)
        device_increment=device_increment+1
        '''

        print 'The IA Through is {val}'.format(val=cympy.study.QueryInfoDevice("IA", name, deviceID))
        print 'The IB Through is {val}'.format(val=cympy.study.QueryInfoDevice("IB", name, deviceID))
        print 'The IC Through is {val}'.format(val=cympy.study.QueryInfoDevice("IC", name, deviceID))
        print 'The IA Out is {val}'.format(val=cympy.study.QueryInfoDevice("IAout", name, deviceID))
        print 'The IB Out is {val}'.format(val=cympy.study.QueryInfoDevice("IBout", name, deviceID))
        print 'The IC Out is {val}'.format(val=cympy.study.QueryInfoDevice("ICout", name, deviceID))
        print 'The total kW is {val}'.format(val=cympy.study.QueryInfoDevice("KWTOT", name, deviceID))


        print 'Overloads with no historical feeder loadings for summer and winter, just kW overload values'
        print 'The Summer Overloading Phase A is {val}'.format(val=cympy.study.QueryInfoDevice("LoadingEqRating1A", name, deviceID))
        print 'The Summer Overloading Phase B is {val}'.format(val=cympy.study.QueryInfoDevice("LoadingEqRating1B", name, deviceID))
        print 'The Summer Overloading Phase C is {val}'.format(val=cympy.study.QueryInfoDevice("LoadingEqRating1C", name, deviceID))
        print 'The Summer Overloading Total is {val}'.format(val=cympy.study.QueryInfoDevice("LoadingEqRating1", name, deviceID))
        print 'The Winter Overloading Phase A is {val}'.format(val=cympy.study.QueryInfoDevice("LoadingEqRating2A", name, deviceID))
        print 'The Winter Overloading Phase B is {val}'.format(val=cympy.study.QueryInfoDevice("LoadingEqRating2B", name, deviceID))
        print 'The Winter Overloading Phase C is {val}'.format(val=cympy.study.QueryInfoDevice("LoadingEqRating2C", name, deviceID))
        print 'The Winter Overloading Total is {val}'.format(val=cympy.study.QueryInfoDevice("LoadingEqRating2", name, deviceID))
        '''
        #Checks too see if the loading value is above 100%, in which case it adds 1 to the number of overloaded
        #components
        if cympy.study.QueryInfoDevice("LOADING", name, deviceID) != '':
            if float(cympy.study.QueryInfoDevice("LOADING", name, deviceID)) > 100.0:
                xfmrOverload = xfmrOverload+1

    device_increment=0
    xfmrByPhaseOverload=0

    #Loops through each of the transformer by phase names
    for name in xfmr_byphase['device_number']:

        #Transformer By Phase has a DeviceID of 33
        deviceID = 33
        Loading_AccurateA=0
        Loading_AccurateB=0
        Loading_AccurateC=0

        #Checks the A phase of the ByPhase Transformers
        if cympy.study.QueryInfoDevice("NomKVAA", name, deviceID) != '' and cympy.study.QueryInfoDevice("KVAA", name, deviceID) != '':
            LimitA = float(cympy.study.QueryInfoDevice("NomKVAA", name, deviceID))
            kWVA = float(cympy.study.QueryInfoDevice("KVAA", name, deviceID))
            Loading_AccurateA = (kWVA / LimitA)*100

        # Checks the B phase of the ByPhase Transformers
        if cympy.study.QueryInfoDevice("NomKVAB", name, deviceID) != '' and cympy.study.QueryInfoDevice("KVAB", name, deviceID) != '':
            LimitB = float(cympy.study.QueryInfoDevice("NomKVAB", name, deviceID))
            kWVB = float(cympy.study.QueryInfoDevice("KVAB", name, deviceID))
            Loading_AccurateB = (kWVB / LimitB)*100

        # Checks the C phase of the ByPhase Transformers
        if cympy.study.QueryInfoDevice("NomKVAC", name, deviceID) != '' and cympy.study.QueryInfoDevice("KVAC", name, deviceID) != '':
            LimitC = float(cympy.study.QueryInfoDevice("NomKVAC", name, deviceID))
            kWVC = float(cympy.study.QueryInfoDevice("KVAC", name, deviceID))
            Loading_AccurateC = (kWVC / LimitC)*100

        #Gathers Penetration, device name, and each phases loadings into storage
        ByPhaseAppend[device_increment] = (truePen ,name, Loading_AccurateA,Loading_AccurateB,Loading_AccurateC)
        device_increment = device_increment + 1


        #Checks too see if any of the loading value are above 100%, in which case it adds 1 to the number of overloaded
        #components
        if cympy.study.QueryInfoDevice("LOADING", name, deviceID) != '':
            if Loading_AccurateA > 100.0 or Loading_AccurateB > 100.0 or Loading_AccurateC > 100.0:
                #print 'the overLoading is {L}'.format(L=Loading)
                xfmrByPhaseOverload = xfmrByPhaseOverload+1




    lineOverload=0
    device_increment=0

    #Loops through each of the cables names
    for name in cable['device_number']:

        #Overline per Phase deviceID = 13, Not per Phrase deviceID = 11
        deviceID=13

        #if any of the line ratings are 1A ignore them, this is the default value in CYME, which means the line ratings
        #are incomplete
        BadStorage=[]
        if cympy.study.QueryInfoDevice("NomAmpA", name, deviceID) == '1.0' or cympy.study.QueryInfoDevice("NomAmpB", name, deviceID) == '1.0' or cympy.study.QueryInfoDevice("NomAmpC", name, deviceID) == '1.0':
            if BadStorage == []:
                BadStorage == name
            else:
                BadStorage.append(name)
        #Checks to see if there are valid results
        if cympy.study.QueryInfoDevice("LOADING", name, deviceID) != '':

            #Doesn't record excessively high values determining such as invalid
            #Generally this would weed out devices that have a 10000% overload rating for the base study
            #If this were to impact an actual study if would be obvious from the drop from values to 0's
            if float(cympy.study.QueryInfoDevice("LOADING", name, deviceID)) <= 300.0:
                LineAppend[device_increment] = (truePen,name, float(cympy.study.QueryInfoDevice("LOADING", name, deviceID)))


            #In the case where devices are found invalid, set their recorded loading to 0
            else:
                LineAppend[device_increment] = (truePen, name, 0)

        #if the results aren't valid, record loading as 0
        else:
            LineAppend[device_increment] = (truePen,name, 0)
        device_increment = device_increment + 1


        if cympy.study.QueryInfoDevice("LOADING", name, deviceID) != '':
            if float(cympy.study.QueryInfoDevice("LOADING", name, deviceID)) > 100.0:
                lineOverload = lineOverload+1
    #Building on the incomplete phrase with number of overloads of each device type

    overloads = ',{val},{val2},{val3}'.format(val=xfmrOverload,val2=xfmrByPhaseOverload,val3=lineOverload)
    print xfmrOverload
    print xfmrByPhaseOverload
    print lineOverload

    #Completes phase
    phrase = start_phrase + overloads + ')'

    #Evaluate term to change from string
    real_phrase = eval(phrase)

    #Appending the new found penetration loop values to the main storage containers
    data.append(real_phrase)
    xfmrStorage.append(xfmrAppend)
    xfmr_byphaseStorage.append(ByPhaseAppend)
    xfmr_cableStorage.append(LineAppend)
    IntentionalValueStorage.append(IntPhrase)
    appliedNameStorage.append(IntapplyPhrase)




    return data, reset, xfmrStorage, xfmr_byphaseStorage, xfmr_cableStorage, aplace, IntentionalValueStorage, appliedNameStorage, BadStorage

def ValidityCheck(xfmr, xfmr_byphase,xfmr_cable, BaseXfmrNull, BaseXfmrByBhaseNull, BaseLineNull):
    '''
    Checks the null device values and compared to the value from BassNulls
    '''
    print 'Validity Check'
    ValidStudy=0
    RepeatVar=0

    #VoltageTol is the variable for loadgrowth by year %, 100 is 100% 1 is 1%
    VoltageTol=0.01
    lf = cympy.sim.LoadFlow()
    lf.Run()

    #While loop that ends if the study if found invalid
    while ValidStudy == 0:
        xfmrNull = 0
        xfmrByPhaseNull = 0
        lineNull = 0

        #if a study fails, this allows it to re-run with an adjusted voltage tolerance
        if RepeatVar != 0:
            lf = cympy.sim.LoadFlow()
            VoltageTol = lf.GetValue('ParametersConfigurations[0].VoltageTolerance')
            print VoltageTol
            lf.SetValue((float(VoltageTol) * 2), 'ParametersConfigurations[0].VoltageTolerance')
            lf.Run()

        #Three for loops for getting the null values from each device type
        for name in xfmr['device_number']:
            if cympy.study.QueryInfoDevice("LOADING", name, 1) == '':
                xfmrNull = xfmrNull + 1
        for name in xfmr_byphase['device_number']:

            if cympy.study.QueryInfoDevice("LOADING", name, 33) == '':
                xfmrByPhaseNull = xfmrByPhaseNull + 1
        for name in xfmr_cable['device_number']:
            if cympy.study.QueryInfoDevice("LOADING", name, 13) == '':
                lineNull = lineNull + 1

        #if any of the devices null values exceed the base call null values then there are new loadflow problems
        if xfmrNull > BaseXfmrNull or xfmrByPhaseNull > BaseXfmrByBhaseNull or lineNull > BaseLineNull:
            ValidStudy = 0
            RepeatVar = RepeatVar + 1
            print 'failure, excess of xfmr:{one} byphase:{two} lines:{three}'.format(one=(xfmrNull-BaseXfmrNull),two=(xfmrByPhaseNull-BaseXfmrByBhaseNull),three=(lineNull-BaseLineNull))

            print VoltageTol
            print type(VoltageTol)

            #if the study cannot complete loadflow near 10% voltage tolerance there are probably major problems
            if float(VoltageTol) >= 10.0:
                print 'Yea that doesn\'t make any sence'
                #model_filename = 'C:\\Users\\pwrlab07\\PycharmProjects\\PGEPython\\INPUT\\Mulino_PythonTest_CYME_Analysis_Test_VoltageTolProbs.sxst'
                model_filename = 'C:\\Users\\pwrlab07\\PycharmProjects\\PGEPython\\INPUT\\Test_VoltageTolProblems.sxst'
                Problems=1
                cympy.study.Save(model_filename)
                return Problems
        #If the study is fine, then return
        else:
            #print 'Well this worked'
            Problems=0
            ValidStudy = 1

            #Resets the loadflow voltage tolerance to 0.01% so other load flow's don't use the inflated value meant for
            #struggling studies
            lf.SetValue(0.01, 'ParametersConfigurations[0].VoltageTolerance')
            return Problems

def whichVal(val):
    '''
    WhichVals is a simple function checking which of three values is the largest
    '''
    output=0
    #print val
    if float(val[2]) > float(val[3]):

        if float(val[2]) > float(val[4]):
            output = [float(val[2])]
        else:
            output = [float(val[4])]
    elif float(val[2]) < float(val[3]):
        if float(val[3]) > float(val[4]):
            output = [float(val[3])]
        else:
            output = [float(val[4])]
    else:
        if float(val[2]) > float(val[4]):
            output = [float(val[2])]
        else:
            output = [float(val[4])]



    return output

def WorstEquipment(xfmrStorage, xfmr_byphaseStorage ,xfmr_cableStorage, HowMany, sizeVar):
    '''
    WorstEquipment is the function that deals with gathering the data for the worst overloads
    '''

    #The output are lists the length of HowMany, with the names of the worst equipment
    XfmrNameTop, TopByPhaseNames, CableNameTop = SortingWorst(xfmrStorage, xfmr_byphaseStorage,
                                                              xfmr_cableStorage, HowMany, sizeVar)
    print(XfmrNameTop)
    print(CableNameTop)
    print(TopByPhaseNames)
    
    one = 0
    two = 0
    three = 0
    four = 0
    five = 0
    six = 0
    seven = 0
    eight = 0
    nine = 0
    ten = 0
    Total_xfmr = []


    if len(xfmrStorage[0]) > HowMany:
        HowManyXfmr=HowMany
    else:
        HowManyXfmr = len(xfmrStorage[0])
    for i in range(len(xfmrStorage)):
        anotherInt = 0

        for name in XfmrNameTop:
            for j in range(len(xfmrStorage[i])):
                if xfmrStorage[i][j][1] == name:
                    if anotherInt == 0:
                        if one == 0:
                            one = [[float(xfmrStorage[i][j][2])]]
                        else:
                            one.append([float(xfmrStorage[i][j][2])])
                        anotherInt = anotherInt + 1
                    elif anotherInt == 1 and HowManyXfmr >= 2:
                        if two == 0:
                            two = [[float(xfmrStorage[i][j][2])]]
                        else:
                            two.append([float(xfmrStorage[i][j][2])])
                        anotherInt = anotherInt + 1
                    elif anotherInt == 2 and HowManyXfmr >= 3:
                        if three == 0:
                            three = [[float(xfmrStorage[i][j][2])]]
                        else:
                            three.append([float(xfmrStorage[i][j][2])])
                        anotherInt = anotherInt + 1
                    elif anotherInt == 3 and HowManyXfmr >= 4:
                        if four == 0:
                            four = [[float(xfmrStorage[i][j][2])]]
                        else:
                            four.append([float(xfmrStorage[i][j][2])])
                        anotherInt = anotherInt + 1
                    elif anotherInt == 4 and HowManyXfmr >= 5:
                        if five == 0:
                            five = [[float(xfmrStorage[i][j][2])]]
                        else:
                            five.append([float(xfmrStorage[i][j][2])])
                        anotherInt = anotherInt + 1
                    elif anotherInt == 5 and HowManyXfmr >= 6:
                        if six == 0:
                            six = [[float(xfmrStorage[i][j][2])]]
                        else:
                            six.append([float(xfmrStorage[i][j][2])])
                        anotherInt = anotherInt + 1
                    if anotherInt == 6 and HowManyXfmr >= 7:
                        if seven == 0:
                            seven = [[float(xfmrStorage[i][j][2])]]
                        else:
                            seven.append([float(xfmrStorage[i][j][2])])
                        anotherInt = anotherInt + 1
                    elif anotherInt == 7 and HowManyXfmr >= 8:
                        if eight == 0:
                            eight = [[float(xfmrStorage[i][j][2])]]
                        else:
                            eight.append([float(xfmrStorage[i][j][2])])
                        anotherInt = anotherInt + 1
                    elif anotherInt == 8 and HowManyXfmr >= 9:
                        if nine == 0:
                            nine = [[float(xfmrStorage[i][j][2])]]
                        else:
                            nine.append([float(xfmrStorage[i][j][2])])
                        anotherInt = anotherInt + 1
                    elif anotherInt == 9 and HowManyXfmr >= 10:
                        if ten == 0:
                            ten = [[float(xfmrStorage[i][j][2])]]
                        else:
                            ten.append([float(xfmrStorage[i][j][2])])
                        anotherInt = anotherInt + 1

    if HowManyXfmr >= 1:
        Total_xfmr.append(one)
    if HowManyXfmr >= 2:
        Total_xfmr.append(two)
    if HowManyXfmr >= 3:
        Total_xfmr.append(three)
    if HowManyXfmr >= 4:
        Total_xfmr.append(four)
    if HowManyXfmr >= 5:
        Total_xfmr.append(five)
    if HowManyXfmr >= 6:
        Total_xfmr.append(six)
    if HowManyXfmr >= 7:
        Total_xfmr.append(seven)
    if HowManyXfmr >= 8:
        Total_xfmr.append(eight)
    if HowManyXfmr >= 9:
        Total_xfmr.append(nine)
    if HowManyXfmr >= 10:
        Total_xfmr.append(ten)


    one = 0
    two = 0
    three = 0
    four = 0
    five = 0
    six = 0
    seven = 0
    eight = 0
    nine = 0
    ten = 0
    Total_ByPhase = []


    for i in range(len(xfmr_byphaseStorage)):
        anotherInt = 0
        for name in TopByPhaseNames:
            for j in range(len(xfmr_byphaseStorage[i])):
                if xfmr_byphaseStorage[i][j][1] == name:
                    if anotherInt == 0:
                        if one == 0:
                            one = [whichVal(xfmr_byphaseStorage[i][j])]
                        else:
                            one.append(whichVal(xfmr_byphaseStorage[i][j]))
                        anotherInt = anotherInt + 1

                    elif anotherInt == 1 and HowMany >= 2:
                        if two == 0:
                            two = [whichVal(xfmr_byphaseStorage[i][j])]
                        else:
                            two.append(whichVal(xfmr_byphaseStorage[i][j]))
                        anotherInt = anotherInt + 1
                    elif anotherInt == 2 and HowMany >= 3:
                        if three == 0:
                            three = [whichVal(xfmr_byphaseStorage[i][j])]
                        else:
                            three.append(whichVal(xfmr_byphaseStorage[i][j]))
                        anotherInt = anotherInt + 1
                    elif anotherInt == 3 and HowMany >= 4:
                        if four == 0:
                            four = [whichVal(xfmr_byphaseStorage[i][j])]
                        else:
                            four.append(whichVal(xfmr_byphaseStorage[i][j]))
                        anotherInt = anotherInt + 1
                    elif anotherInt == 4 and HowMany >= 5:
                        if five == 0:
                            five = [whichVal(xfmr_byphaseStorage[i][j])]
                        else:
                            five.append(whichVal(xfmr_byphaseStorage[i][j]))
                        anotherInt = anotherInt + 1
                    elif anotherInt == 5 and HowMany >= 6:
                        if six == 0:
                            six = [whichVal(xfmr_byphaseStorage[i][j])]
                        else:
                            six.append(whichVal(xfmr_byphaseStorage[i][j]))
                        anotherInt = anotherInt + 1
                    if anotherInt == 6 and HowMany >= 7:
                        if seven == 0:
                            seven = [whichVal(xfmr_byphaseStorage[i][j])]
                        else:
                            seven.append(whichVal(xfmr_byphaseStorage[i][j]))
                        anotherInt = anotherInt + 1
                    elif anotherInt == 7 and HowMany >= 8:
                        if eight == 0:
                            eight = [whichVal(xfmr_byphaseStorage[i][j])]
                        else:
                            eight.append(whichVal(xfmr_byphaseStorage[i][j]))
                        anotherInt = anotherInt + 1
                    elif anotherInt == 8 and HowMany >= 9:
                        if nine == 0:
                            nine = [whichVal(xfmr_byphaseStorage[i][j])]
                        else:
                            nine.append(whichVal(xfmr_byphaseStorage[i][j]))
                        anotherInt = anotherInt + 1
                    elif anotherInt == 9 and HowMany >= 10:
                        if ten == 0:
                            ten = [whichVal(xfmr_byphaseStorage[i][j])]
                        else:
                            ten.append(whichVal(xfmr_byphaseStorage[i][j]))
                        anotherInt = anotherInt + 1
    print 'ByPhase Started'
    if HowMany >= 1:
        Total_ByPhase.append(one)
    if HowMany >= 2:
        Total_ByPhase.append(two)
    if HowMany >= 3:
        Total_ByPhase.append(three)
    if HowMany >= 4:
        Total_ByPhase.append(four)
    if HowMany >= 5:
        Total_ByPhase.append(five)
    if HowMany >= 6:
        Total_ByPhase.append(six)
    if HowMany >= 7:
        Total_ByPhase.append(seven)
    if HowMany >= 8:
        Total_ByPhase.append(eight)
    if HowMany >= 9:
        Total_ByPhase.append(nine)
    if HowMany >= 10:
        Total_ByPhase.append(ten)
    print 'ByPhase Done'
    one = 0
    two = 0
    three = 0
    four = 0
    five = 0
    six = 0
    seven = 0
    eight = 0
    nine = 0
    ten = 0
    Total_Cable = []

    for i in range(len(xfmr_cableStorage)):
        anotherInt = 0
        for name in CableNameTop:
            for j in range(len(xfmr_cableStorage[i])):
                if xfmr_cableStorage[i][j][1] == name:

                    if anotherInt == 0:
                        if one == 0:
                            one = [[float(xfmr_cableStorage[i][j][2])]]
                        else:
                            one.append([float(xfmr_cableStorage[i][j][2])])
                        anotherInt = anotherInt + 1
                    elif anotherInt == 1 and HowMany >= 2:
                        if two == 0:
                            two = [[float(xfmr_cableStorage[i][j][2])]]
                        else:
                            two.append([float(xfmr_cableStorage[i][j][2])])
                        anotherInt = anotherInt + 1
                    elif anotherInt == 2 and HowMany >= 3:
                        if three == 0:
                            three = [[float(xfmr_cableStorage[i][j][2])]]
                        else:
                            three.append([float(xfmr_cableStorage[i][j][2])])
                        anotherInt = anotherInt + 1
                    elif anotherInt == 3 and HowMany >= 4:
                        if four == 0:
                            four = [[float(xfmr_cableStorage[i][j][2])]]
                        else:
                            four.append([float(xfmr_cableStorage[i][j][2])])
                        anotherInt = anotherInt + 1
                    elif anotherInt == 4 and HowMany >= 5:
                        if five == 0:
                            five = [[float(xfmr_cableStorage[i][j][2])]]
                        else:
                            five.append([float(xfmr_cableStorage[i][j][2])])
                        anotherInt = anotherInt + 1
                    elif anotherInt == 5 and HowMany >= 6:
                        if six == 0:
                            six = [[float(xfmr_cableStorage[i][j][2])]]
                        else:
                            six.append([float(xfmr_cableStorage[i][j][2])])
                        anotherInt = anotherInt + 1
                    if anotherInt == 6 and HowMany >= 7:
                        if seven == 0:
                            seven = [[float(xfmr_cableStorage[i][j][2])]]
                        else:
                            seven.append([float(xfmr_cableStorage[i][j][2])])
                        anotherInt = anotherInt + 1
                    elif anotherInt == 7 and HowMany >= 8:
                        if eight == 0:
                            eight = [[float(xfmr_cableStorage[i][j][2])]]
                        else:
                            eight.append([float(xfmr_cableStorage[i][j][2])])
                        anotherInt = anotherInt + 1
                    elif anotherInt == 8 and HowMany >= 9:
                        if nine == 0:
                            nine = [[float(xfmr_cableStorage[i][j][2])]]
                        else:
                            nine.append([float(xfmr_cableStorage[i][j][2])])
                        anotherInt = anotherInt + 1
                    elif anotherInt == 9 and HowMany >= 10:
                        if ten == 0:
                            ten = [[float(xfmr_cableStorage[i][j][2])]]
                        else:
                            ten.append([float(xfmr_cableStorage[i][j][2])])
                        anotherInt = anotherInt + 1

    if HowMany >= 1:
        Total_Cable.append(one)
    if HowMany >= 2:
        Total_Cable.append(two)
    if HowMany >= 3:
        Total_Cable.append(three)
    if HowMany >= 4:
        Total_Cable.append(four)
    if HowMany >= 5:
        Total_Cable.append(five)
    if HowMany >= 6:
        Total_Cable.append(six)
    if HowMany >= 7:
        Total_Cable.append(seven)
    if HowMany >= 8:
        Total_Cable.append(eight)
    if HowMany >= 9:
        Total_Cable.append(nine)
    if HowMany >= 10:
        Total_Cable.append(ten)

    #list of devices
    print Total_xfmr

    #list of overload values
    print Total_xfmr[0]

    #'list' of a single value
    print Total_xfmr[0][0]

    #float of a single value
    print Total_xfmr[0][0][0]

    print Total_ByPhase

    print Total_Cable

    print 'Worst Equipment is Done'

    return Total_xfmr, Total_ByPhase, Total_Cable, XfmrNameTop, TopByPhaseNames, CableNameTop

def takeFirst(elem):
    return elem[0]

def takeSecond(elem):

    '''
    Function used for sorting by final value
    '''

    return elem[1]

def takeThird(elem):

    '''
    Function used for sorting by final value
    '''

    return elem[2]

def takeFourth(elem):

    '''
    Function used for sorting by final value
    '''

    return elem[3]

def takeFifth(elem):

    '''
    Function used for sorting by final value
    '''

    return elem[4]

def SortingWorst(xfmrStorage, xfmr_byphaseStorage, xfmr_cableStorage, HowMany, sizeVar):

    '''
    SortingWorse is a small function for sorting the loadings by magnitude, seperate storage for ByPhase phase loading
    storage
    '''

    '''Xfmr Section'''
    print xfmrStorage
    for val in xfmrStorage:
        #print val
        val.sort(key=takeThird, reverse=True)

    if len(xfmrStorage[0]) > HowMany:
        HowManyXfmr=HowMany
    else:
        HowManyXfmr = len(xfmrStorage[0])


    XfmrStorageTop = [[]] * HowManyXfmr
    XfmrNameTop = [[]] * HowManyXfmr
    XfmrThingsTop = [[]] * HowManyXfmr


    for i in range(len(XfmrStorageTop)):
        XfmrStorageTop[i]=0

    for i in range(len(XfmrStorageTop)):
        for j in range(len(xfmrStorage)):
            XfmrStorageTop[i] = XfmrStorageTop[i] + float(xfmrStorage[j][i][2])
            XfmrNameTop[i]=xfmrStorage[j][i][1]
    print XfmrStorageTop
    print XfmrNameTop


    '''Cable Section'''

    for val in xfmr_cableStorage:
        #print val
        val.sort(key=takeThird, reverse=True)

    if len(xfmr_cableStorage[0]) >= HowMany:
        CableStorageTop = [[]] * HowMany
        CableNameTop = [[]] * HowMany
        CableThingsTop = [[]] * HowMany
    else:
        CableStorageTop = [[]] * len(xfmr_cableStorage[0])
        CableNameTop = [[]] * len(xfmr_cableStorage[0])
        CableThingsTop = [[]] * len(xfmr_cableStorage[0])

    for i in range(len(CableStorageTop)):
        CableStorageTop[i]=0

    for i in range(len(CableStorageTop)):
        for j in range(len(xfmr_cableStorage)):
            CableStorageTop[i] = CableStorageTop[i] + float(xfmr_cableStorage[j][i][2])
            CableNameTop[i]=xfmr_cableStorage[j][i][1]
    print CableStorageTop
    print CableNameTop

    '''Xfmr ByPhase Section'''


    xfmr_byphaseAStorage=xfmr_byphaseStorage

    for val in xfmr_byphaseAStorage:
        #print val
        val.sort(key=takeThird, reverse=True)

    PhaseAStorage=[[]]*HowMany
    PhaseAName=[[]]*HowMany

    for i in range(len(PhaseAStorage)):
        PhaseAStorage[i]=0
    for i in range(len(PhaseAStorage)):
        for j in range(len(xfmr_byphaseAStorage)):
            #print 'Whats wrong?'
            #print i
            #print PhaseAStorage
            #print j
            #print len(PhaseAStorage)
            #print len(xfmr_byphaseAStorage)
            PhaseAStorage[i] = PhaseAStorage[i] + float(xfmr_byphaseAStorage[j][i][2])
            PhaseAName[i]=xfmr_byphaseAStorage[j][i][1]
    #print PhaseAName
    #print PhaseAStorage

    PhaseAThings=[[]]*HowMany

    for i in range(len(PhaseAThings)):
        PhaseAThings[i]=[PhaseAName[i],PhaseAStorage[i]]



    xfmr_byphaseBStorage = xfmr_byphaseStorage

    for val in xfmr_byphaseBStorage:
        #print val
        val.sort(key=takeFourth, reverse=True)

    if len(xfmr_byphaseStorage[0]) >= HowMany:
        PhaseBStorage = [[]] * HowMany
        PhaseBName = [[]] * HowMany
        PhaseBThings = [[]] * HowMany
    else:
        PhaseBStorage = [[]] * len(xfmr_byphaseStorage[0])
        PhaseBName = [[]] * len(xfmr_byphaseStorage[0])
        PhaseBThings = [[]] * len(xfmr_byphaseStorage[0])

    for i in range(len(PhaseBStorage)):
        PhaseBStorage[i] = 0

    for i in range(len(PhaseBStorage)):
        for j in range(len(xfmr_byphaseBStorage)):
            PhaseBStorage[i] = PhaseBStorage[i] + float(xfmr_byphaseBStorage[j][i][3])
            PhaseBName[i] = xfmr_byphaseBStorage[j][i][1]
    #print PhaseBName
    #print PhaseBStorage

    for i in range(len(PhaseBThings)):
        PhaseBThings[i] = [PhaseBName[i], PhaseBStorage[i]]



    xfmr_byphaseCStorage = xfmr_byphaseStorage

    for val in xfmr_byphaseCStorage:
        #print val
        val.sort(key=takeFifth, reverse=True)

    if len(xfmr_byphaseStorage[0]) >= HowMany:
        PhaseCStorage = [[]] * HowMany
        PhaseCName = [[]] * HowMany
        PhaseCThings = [[]] * HowMany
    else:
        PhaseCStorage = [[]] * len(xfmr_byphaseStorage[0])
        PhaseCName = [[]] * len(xfmr_byphaseStorage[0])
        PhaseCThings = [[]] * len(xfmr_byphaseStorage[0])

    for i in range(len(PhaseCStorage)):
        PhaseCStorage[i] = 0

    for i in range(len(PhaseCStorage)):
        for j in range(len(xfmr_byphaseCStorage)):
            PhaseCStorage[i] = PhaseCStorage[i] + float(xfmr_byphaseCStorage[j][i][4])
            PhaseCName[i] = xfmr_byphaseCStorage[j][i][1]

    #print PhaseCName
    #print PhaseCStorage

    for i in range(len(PhaseCThings)):
        PhaseCThings[i] = [PhaseCName[i], PhaseCStorage[i]]

    TopXfmrNames = xfmrStorage[0][0:3]

    PhaseStorageSorting=[]
    #print PhaseStorageSorting
    for i in range(len(PhaseAThings)):
        PhaseStorageSorting.append(PhaseAThings[i])
    #print PhaseStorageSorting
    for i in range(len(PhaseBThings)):
        PhaseStorageSorting.append(PhaseBThings[i])
    #print PhaseStorageSorting
    for i in range(len(PhaseCThings)):
        PhaseStorageSorting.append(PhaseCThings[i])

    PhaseStorageSorting.sort(key=takeSecond, reverse=True)


    TopByPhaseNames=PhaseStorageSorting[0:HowMany]
    TopByPhaseStorage = PhaseStorageSorting[0:HowMany]
    intval=0
    for val in TopByPhaseNames:

        TopByPhaseNames[intval]=val[0]
        TopByPhaseStorage[intval] = val[1]
        intval=intval+1
    print TopByPhaseStorage
    print TopByPhaseNames




    return XfmrNameTop,TopByPhaseNames,CableNameTop

def OverloadGathering(xfmrStorage, TimeRange, VoltProfile):
    one = -1

    StorageFull = []
    StorageFullWorst = []
    StorageVoltFull = []
    LenOverFull = []
    VoltagePart = []
    VoltageA = []
    VoltageB = []
    VoltageC = []
    VoltageTrendA = []
    VoltageTrendB = []
    VoltageTrendC = []
    LoadingTrendA = []
    LoadingTrendB = []
    LoadingTrendC = []
    VoltageTrend = []
    LoadingTrend = []

    for Pen in xfmrStorage:
        CheckingValue=-1
        one = one + 1
        two = -1
        VoltageATrend = []
        VoltageBTrend = []
        VoltageCTrend = []
        LoadingATrend = []
        LoadingBTrend = []
        LoadingCTrend = []
        StorageValue = []
        StorageValueWorst = []
        StorageVoltValue = []
        LenOverStorage = []
        VoltageAInside = 0
        VoltageBInside = 0
        VoltageCInside = 0
        # Pen Penetration follow by a list of each time step

        for place in Pen[1]:

            two = two + 1
            three = -1
            OverloadsATrend = 0
            OverloadsBTrend = 0
            OverloadsCTrend = 0
            UnderVoltATrend = 0
            UnderVoltBTrend = 0
            UnderVoltCTrend = 0
            # place is the list of a single timestep value values

            for asset in place:
                three = three + 1
                # Asset is a single asset

                i = -1
                if asset[1] >= 125.0:
                    OverloadsATrend = OverloadsATrend + 1
                if VoltProfile[one][1][two][three][1] <= 0.95 and VoltProfile[one][1][two][three][1] > 0.01:
                    UnderVoltATrend = UnderVoltATrend + 1
                if asset[2] >= 125.0:
                    OverloadsBTrend = OverloadsBTrend + 1
                if VoltProfile[one][1][two][three][2] <= 0.95 and VoltProfile[one][1][two][three][2] > 0.01:
                    UnderVoltBTrend = UnderVoltBTrend + 1
                if asset[3] >= 125.0:
                    OverloadsCTrend = OverloadsCTrend + 1
                if VoltProfile[one][1][two][three][3] <= 0.95 and VoltProfile[one][1][two][three][3] > 0.01:
                    UnderVoltCTrend = UnderVoltCTrend + 1
                '''
                print 'asset and xfmrStorage that should match it'
                print asset
                print xfmrStorage[one][1][0][three]
                if asset != xfmrStorage[one][1][0][three]:
                    print 'Broken with one = {oneval} three = {threeval}'.format(oneval=one, threeval=three)
                '''
            three=-1
            if two == 0:
                for asset in place:
                    three=three+1

                    OverloadsA = 0
                    OverloadsB = 0
                    OverloadsC = 0
                    UnderVoltA = 0
                    UnderVoltB = 0
                    UnderVoltC = 0

                    LenOverA = 0
                    LenOverB = 0
                    LenOverC = 0
                    LenOverAArray = []
                    LenOverBArray = []
                    LenOverCArray = []

                    i=-1
                    PhaseAWorstValue=0
                    PhaseBWorstValue = 0
                    PhaseCWorstValue = 0
                    for val in TimeRange:
                        #Gathering the Loading value from each time step
                        i = i + 1

                        if xfmrStorage[one][1][i][three][1] >= 125.0:

                            #print xfmrStorage[one][1][i][three]
                            if asset[0] == 'A:25 92686' or asset[0] == 'C:15 42625' or asset[0] == 'B:25 60157' or asset[0] == 'A:25 75658' or asset[0] == 'B:10 16617':
                                print 'A loading Over'
                                print val
                                print asset
                                print xfmrStorage[one][1][i][three]
                            OverloadsA = OverloadsA + 1
                            LenOverA = LenOverA + 1


                        else:
                            if LenOverA != 0:
                                LenOverAArray.append(LenOverA)
                                LenOverA = 0

                        if VoltProfile[one][1][i][three][1] <= 0.95 and VoltProfile[one][1][i][three][1] > 0.01:
                            #print 'undervoltage A'
                            #print asset[0]
                            #print VoltProfile[one][1][i][three]
                            UnderVoltA=UnderVoltA+1
                            VoltageAInside=VoltageAInside+1

                        if xfmrStorage[one][1][i][three][2] >= 125.0:


                            #print xfmrStorage[one][1][i][three]
                            if asset[0] == 'A:25 92686' or asset[0] == 'C:15 42625' or asset[0] == 'B:25 60157' or asset[0] == 'A:25 75658' or asset[0] == 'B:10 16617':
                                print 'B loading Over'
                                print val
                                print asset
                                print xfmrStorage[one][1][i][three]

                            OverloadsB = OverloadsB + 1
                            LenOverB = LenOverB + 1

                        else:
                            if LenOverB != 0:
                                LenOverBArray.append(LenOverB)
                                LenOverB = 0

                        if VoltProfile[one][1][i][three][2] <= 0.95 and VoltProfile[one][1][i][three][2] > 0.01:
                            #print 'undervoltage B'
                            #print asset[0]
                            #print VoltProfile[one][1][i][three]
                            UnderVoltB=UnderVoltB+1
                            VoltageBInside=VoltageBInside+1


                        if xfmrStorage[one][1][i][three][3] >= 125.0:

                            if asset[0] == 'A:25 92686' or asset[0] == 'C:15 42625' or asset[0] == 'B:25 60157' or asset[0] == 'A:25 75658' or asset[0] == 'B:10 16617':
                                print 'C loading Over'
                                print val
                                print asset
                                print xfmrStorage[one][1][i][three]

                            OverloadsC = OverloadsC + 1
                            LenOverC = LenOverC + 1

                        else:
                            if LenOverC != 0:
                                LenOverCArray.append(LenOverC)
                                LenOverC = 0

                        if VoltProfile[one][1][i][three][3] <= 0.95 and VoltProfile[one][1][i][three][3] > 0.01:
                            #print 'undervoltage C'
                            #print asset[0]
                            #print VoltProfile[one][1][i][three]
                            UnderVoltC=UnderVoltC+1
                            VoltageCInside=VoltageCInside+1

                        PhaseAWorstValue = PhaseAWorstValue + xfmrStorage[one][1][i][three][1]
                        PhaseBWorstValue = PhaseBWorstValue + xfmrStorage[one][1][i][three][2]
                        PhaseCWorstValue = PhaseCWorstValue + xfmrStorage[one][1][i][three][3]


                    if LenOverA != 0:
                        LenOverAArray.append(LenOverA)
                    if LenOverB != 0:
                        LenOverBArray.append(LenOverB)
                    if LenOverC != 0:
                        LenOverCArray.append(LenOverC)

                    StorageValueAppend = [asset[0], OverloadsA, OverloadsB, OverloadsC]
                    StorageValue.append(StorageValueAppend)
                    StorageValueAppendWorst = [asset[0], PhaseAWorstValue, PhaseBWorstValue, PhaseCWorstValue]
                    StorageValueWorst.append(StorageValueAppendWorst)
                    StorageVoltValueAppend = [asset[0], UnderVoltA, UnderVoltB, UnderVoltC]
                    StorageVoltValue.append(StorageVoltValueAppend)

                    LenOverAppend = [asset[0], LenOverAArray, LenOverBArray, LenOverCArray]
                    #print LenOverAppend
                    LenOverStorage.append(LenOverAppend)

            VoltageATrend.append(UnderVoltATrend)
            VoltageBTrend.append(UnderVoltBTrend)
            VoltageCTrend.append(UnderVoltCTrend)
            LoadingATrend.append(OverloadsATrend)
            LoadingBTrend.append(OverloadsBTrend)
            LoadingCTrend.append(OverloadsCTrend)


        VoltageA.append(VoltageAInside)
        VoltageB.append(VoltageBInside)
        VoltageC.append(VoltageCInside)
        '''
        print 'Below are the Storage value of overloads followed by the LenOverAppend'
        for i in range(0,len(StorageValue)):
            print StorageValue[i]
            print LenOverAppend[i]
        exit()
        '''
        StorageFull.append(StorageValue)
        StorageFullWorst.append(StorageValueWorst)
        StorageVoltFull.append(StorageVoltValue)
        LenOverFull.append(LenOverStorage)
        VoltageTrendA.append(VoltageATrend)
        VoltageTrendB.append(VoltageBTrend)
        VoltageTrendC.append(VoltageCTrend)
        LoadingTrendA.append(LoadingATrend)
        LoadingTrendB.append(LoadingBTrend)
        LoadingTrendC.append(LoadingCTrend)

    # print 'Len over'
    VoltagePart.append(VoltageA)

    VoltagePart.append(VoltageB)
    VoltagePart.append(VoltageC)
    VoltageTrend.append(VoltageTrendA)

    print 'voltageTrend a single phase, then TimeRange'
    print VoltageTrend[0][0]
    print len(VoltageTrend[0][0])
    print TimeRange
    print len(TimeRange)

    VoltageTrend.append(VoltageTrendB)
    VoltageTrend.append(VoltageTrendC)

    LoadingTrend.append(LoadingTrendA)
    LoadingTrend.append(LoadingTrendB)
    LoadingTrend.append(LoadingTrendC)

    # print LenOverFull

    return StorageFull, LenOverFull, StorageVoltFull,VoltagePart, VoltageTrend, LoadingTrend, StorageFullWorst

def WorstOverStoringPlaceHolder(StorageFull):

    MostStore=[]

    for Asset in StorageFull[0]:
        MaxVal=0
        MostAppending=0
        if Asset[1] >= Asset[2]:
            if Asset[1] >= Asset[3]:
                MaxVal=Asset[1]
            else:
                MaxVal=Asset[3]
        else:
            if Asset[2] >= Asset[3]:
                MaxVal=Asset[2]
            else:
                MaxVal=Asset[3]
        MostAppending= [Asset[0],MaxVal]
        MostStore.append(MostAppending)
    MostStore.sort(key=takeSecond, reverse=True)
    return MostStore

def HowManyStoring(StorageFull):

    MostStore=[]
    length=len(StorageFull)
    baseval=-1
    for Asset in StorageFull[0]:
        baseval=baseval+1
        AssetA=0
        AssetB=0
        AssetC=0
        for i in range(0,length):
            AssetA=StorageFull[i][baseval][1]+AssetA
            AssetB = StorageFull[i][baseval][2] + AssetB
            AssetC = StorageFull[i][baseval][3] + AssetC
        MaxVal=0
        MostAppending=0
        if AssetA >= AssetB:
            if AssetA >= AssetC:
                MaxVal=AssetA
            else:
                MaxVal=AssetC
        else:
            if AssetB >= AssetC:
                MaxVal=AssetB
            else:
                MaxVal=AssetC
        MostAppending= [Asset[0],MaxVal]
        MostStore.append(MostAppending)
    MostStore.sort(key=takeSecond, reverse=True)
    return MostStore

def ExcelFormatCreation(xfmrStorage,MostStore,StorageFull,StorageVoltFull, HowMany):
    ExcelNameHolder=[]
    XfmrExcelFull=[]
    XfmrExcelFullHM=[]

    holding=-1
    for PenStore in xfmrStorage:
        holding=holding+1
        XfmrExcelSinglePen=[]
        XfmrExcelSinglePenHM=[]
        rownum=0

        for Time in PenStore[1]:
            LoadStore = 'nothing'
            OverRow='nothing'
            UnderRow = 'nothing'
            LoadStoreHM = 'nothing'
            OverRowHM='nothing'
            UnderRowHM = 'nothing'
            HowManyInt = 0
            for AssetOrder in MostStore:

                OtherTimes = -1
                for Asset in Time:
                    OtherTimes=OtherTimes+1
                    if AssetOrder[0] == Asset[0]:
                        NewLen = len(MostStore)


                        OtherTimes=OtherTimes+1
                        if rownum == 0:
                            HowManyInt = 0
                            OtherLen = 0
                            for place in MostStore:
                                for place2 in StorageFull[holding]:
                                    if place[0] == place2[0]:
                                        #OverLoading Row
                                        if OverRow == 'nothing':
                                            OverRow = '[{val},{val2},{val3}'.format(val=place2[1],val2=place2[2],val3=place2[3])
                                        else:
                                            OverRow = OverRow+',{val},{val2},{val3}'.format(val=place2[1],val2=place2[2],val3=place2[3])

                                        if HowManyInt < HowMany and OtherLen < NewLen:
                                            if OverRowHM == 'nothing':
                                                OverRowHM = '[{val},{val2},{val3}'.format(val=place2[1],val2=place2[2],val3=place2[3])
                                            else:
                                                OverRowHM = OverRowHM+',{val},{val2},{val3}'.format(val=place2[1],val2=place2[2],val3=place2[3])
                                            OtherLen=OtherLen+1
                                            '''
                                            print OverRowHM
                                            print OverRow
                                            '''
                                            HowManyInt=HowManyInt+1

                            OtherLen=0
                            OverRow=OverRow+']'
                            OverRowHM = OverRowHM + ']'
                            AppendingVal=eval(OverRow)
                            XfmrExcelSinglePen.append(AppendingVal)
                            AppendingValHM=eval(OverRowHM)
                            XfmrExcelSinglePenHM.append(AppendingValHM)
                            '''
                            print 'values'
                            print AppendingVal
                            print AppendingValHM
                            '''

                            rownum = 1

                        if rownum == 1:
                            HowManyInt = 0
                            for place in MostStore:
                                for place2 in StorageVoltFull[holding]:
                                    if place[0] == place2[0]:
                                        #UnderVoltage Row
                                        if UnderRow == 'nothing':
                                            UnderRow = '[{val},{val2},{val3}'.format(val=place2[1],val2=place2[2],val3=place2[3])
                                        else:
                                            UnderRow = UnderRow+',{val},{val2},{val3}'.format(val=place2[1],val2=place2[2],val3=place2[3])

                                        if HowManyInt < HowMany and OtherLen < NewLen:
                                            if UnderRowHM == 'nothing':
                                                UnderRowHM = '[{val},{val2},{val3}'.format(val=place2[1],val2=place2[2],val3=place2[3])
                                            else:
                                                UnderRowHM = UnderRowHM+',{val},{val2},{val3}'.format(val=place2[1],val2=place2[2],val3=place2[3])

                                            HowManyInt=HowManyInt+1
                                            OtherLen=OtherLen+1
                            OtherLen = 0
                            UnderRow=UnderRow+']'
                            AppendingVal=eval(UnderRow)
                            XfmrExcelSinglePen.append(AppendingVal)
                            UnderRowHM=UnderRowHM+']'
                            AppendingValHM=eval(UnderRowHM)
                            XfmrExcelSinglePenHM.append(AppendingValHM)
                            rownum = 2
                            HowManyInt = 0
                            '''
                            print 'values'
                            print AppendingVal
                            print AppendingValHM
                            '''

                        if rownum == 2:
                            if len(ExcelNameHolder)<len(MostStore):
                                ExcelNameHolder.append(Asset[0])
                            if LoadStore == 'nothing':
                                LoadStore = '[{val},{val2},{val3}'.format(val=Asset[1],val2=Asset[2],val3=Asset[3])
                            else:
                                LoadStore = LoadStore + ',{val},{val2},{val3}'.format(val=Asset[1],val2=Asset[2],val3=Asset[3])
                            if HowManyInt < HowMany:
                                if LoadStoreHM == 'nothing':
                                    LoadStoreHM = '[{val},{val2},{val3}'.format(val=Asset[1], val2=Asset[2],
                                                                              val3=Asset[3])
                                else:
                                    LoadStoreHM = LoadStoreHM + ',{val},{val2},{val3}'.format(val=Asset[1], val2=Asset[2],
                                                                                          val3=Asset[3])
                                HowManyInt=HowManyInt+1
            LoadStore=LoadStore+']'
            AppendingVal=eval(LoadStore)
            XfmrExcelSinglePen.append(AppendingVal)
            LoadStoreHM = LoadStoreHM + ']'
            AppendingValHM = eval(LoadStoreHM)
            XfmrExcelSinglePenHM.append(AppendingValHM)
        XfmrExcelFull.append(XfmrExcelSinglePen)
        XfmrExcelFullHM.append(XfmrExcelSinglePenHM)


    return XfmrExcelFull,ExcelNameHolder, XfmrExcelFullHM

def HistogramFormat(LengthRecord,MostStore, HowMany):
    #Data=[# 3 or less, #3 to 6, #6 to 9, 9 to 12, 12 to 15, 15 to 18]
    BinningVal=[3,6,9,12,15,18]
    print 'start of Histogram Format'
    print LengthRecord
    HistogramFullStorage=[]
    HistogramFullStorageHM=[]
    GraphStore = []
    GraphStoreA=[]
    GraphStoreB=[]
    GraphStoreC=[]

    value2=-1
    for Penetration in LengthRecord:
        value2=value2+1
        HistogramPenStorage=[]
        HistogramPenStorageHM=[]
        StoreBinsAGraph = [0, 0, 0, 0]
        StoreBinsBGraph = [0, 0, 0, 0]
        StoreBinsCGraph = [0, 0, 0, 0]
        HowManyInt=0
        for place in MostStore:
            value=0

            for asset in Penetration:
                if place[0] == asset[0]:
                    #print asset
                    StoreBinsA = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                    StoreBinsB = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                    StoreBinsC = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                    setA = 0
                    setB = 0
                    setC = 0
                    set=0

                    if asset[1] != []:
                        for Aval in asset[1]:
                            if Aval < 3:
                                StoreBinsA[0]=StoreBinsA[0]+1
                            elif Aval >= 3 and Aval < 6:
                                StoreBinsA[1] = StoreBinsA[1] + 1
                            elif Aval >= 6 and Aval < 9:
                                StoreBinsA[2] = StoreBinsA[2] + 1
                            elif Aval >= 9 and Aval < 12:
                                StoreBinsA[3] = StoreBinsA[3] + 1
                            elif Aval >= 12 and Aval < 15:
                                StoreBinsA[4] = StoreBinsA[4] + 1
                            elif Aval >= 15 and Aval < 18:
                                StoreBinsA[5] = StoreBinsA[5] + 1
                            elif Aval >= 18 and Aval < 21:
                                StoreBinsA[6] = StoreBinsA[6] + 1
                            elif Aval >= 21 and Aval < 24:
                                StoreBinsA[7] = StoreBinsA[7] + 1
                            elif Aval >= 24 and Aval < 27:
                                StoreBinsA[8] = StoreBinsA[8] + 1
                            else:
                                StoreBinsA[9] = StoreBinsA[9] + 1

                            if Aval >= 12 and Aval < 18:
                                StoreBinsAGraph[0] = StoreBinsAGraph[0] + 1
                            elif Aval >= 18 and Aval < 24:
                                StoreBinsAGraph[1] = StoreBinsAGraph[1] + 1
                            elif Aval >= 24 and Aval < 30:
                                StoreBinsAGraph[2] = StoreBinsAGraph[2] + 1
                            elif Aval >= 30:
                                StoreBinsAGraph[3] = StoreBinsAGraph[3] + 1

                            if Aval >= 3:
                                setA=1

                    if asset[2] != []:
                        for Aval in asset[2]:
                            if Aval < 3:
                                StoreBinsB[0]=StoreBinsB[0]+1
                            elif Aval >= 3 and Aval < 6:
                                StoreBinsB[1] = StoreBinsB[1] + 1
                            elif Aval >= 6 and Aval < 9:
                                StoreBinsB[2] = StoreBinsB[2] + 1
                            elif Aval >= 9 and Aval < 12:
                                StoreBinsB[3] = StoreBinsB[3] + 1
                            elif Aval >= 12 and Aval < 15:
                                StoreBinsB[4] = StoreBinsA[4] + 1
                            elif Aval >= 15 and Aval < 18:
                                StoreBinsB[5] = StoreBinsB[5] + 1
                            elif Aval >= 18 and Aval < 21:
                                StoreBinsB[6] = StoreBinsB[6] + 1
                            elif Aval >= 21 and Aval < 24:
                                StoreBinsB[7] = StoreBinsB[7] + 1
                            elif Aval >= 24 and Aval < 27:
                                StoreBinsB[8] = StoreBinsB[8] + 1
                            else:
                                StoreBinsB[9] = StoreBinsB[9] + 1

                            if Aval >= 12 and Aval < 18:
                                StoreBinsBGraph[0] = StoreBinsBGraph[0] + 1
                            elif Aval >= 18 and Aval < 24:
                                StoreBinsBGraph[1] = StoreBinsBGraph[1] + 1
                            elif Aval >= 24 and Aval < 30:
                                StoreBinsBGraph[2] = StoreBinsBGraph[2] + 1
                            elif Aval >= 30:
                                StoreBinsBGraph[3] = StoreBinsBGraph[3] + 1

                            if Aval >= 3:
                                setB=1
                    if asset[3] != []:
                        for Aval in asset[3]:
                            if Aval < 3:
                                StoreBinsC[0]=StoreBinsC[0]+1
                            elif Aval >= 3 and Aval < 6:
                                StoreBinsC[1] = StoreBinsC[1] + 1
                            elif Aval >= 6 and Aval < 9:
                                StoreBinsC[2] = StoreBinsC[2] + 1
                            elif Aval >= 9 and Aval < 12:
                                StoreBinsC[3] = StoreBinsC[3] + 1
                            elif Aval >= 12 and Aval < 15:
                                StoreBinsC[4] = StoreBinsC[4] + 1
                            elif Aval >= 15 and Aval < 18:
                                StoreBinsC[5] = StoreBinsC[5] + 1
                            elif Aval >= 18 and Aval < 21:
                                StoreBinsC[6] = StoreBinsC[6] + 1
                            elif Aval >= 21 and Aval < 24:
                                StoreBinsC[7] = StoreBinsC[7] + 1
                            elif Aval >= 24 and Aval < 27:
                                StoreBinsC[8] = StoreBinsC[8] + 1
                            else:
                                StoreBinsC[9] = StoreBinsC[9] + 1

                            if Aval >= 12 and Aval < 18:
                                StoreBinsCGraph[0] = StoreBinsCGraph[0] + 1
                            elif Aval >= 18 and Aval < 24:
                                StoreBinsCGraph[1] = StoreBinsCGraph[1] + 1
                            elif Aval >= 24 and Aval < 30:
                                StoreBinsCGraph[2] = StoreBinsCGraph[2] + 1
                            elif Aval >= 30:
                                StoreBinsCGraph[3] = StoreBinsCGraph[3] + 1

                            if Aval >= 3:
                                setC=1
                    if setA == 1 or setB == 1 or setC == 1:
                        value=value+1

                    if setA == 1 or setB == 1 or setC ==1:
                        AppendPhrase=[asset[0]]
                    else:
                        AppendPhrase=[]
                    AppendBlank = []

                    if HowManyInt < HowMany:
                        if setA == 1 or setB == 1 or setC == 1:
                            AppendPhraseHM = [asset[0]]
                        else:
                            AppendPhraseHM = []
                        if setA == 1:
                            AppendPhraseHM.append(StoreBinsA)
                        else:
                            AppendPhraseHM.append(AppendBlank)

                        if setB == 1:
                            AppendPhraseHM.append(StoreBinsB)
                        else:
                            AppendPhraseHM.append(AppendBlank)

                        if setC == 1:
                            AppendPhraseHM.append(StoreBinsC)
                        else:
                            AppendPhraseHM.append(AppendBlank)
                        HistogramPenStorageHM.append(AppendPhraseHM)



                    if setA == 1:
                        AppendPhrase.append(StoreBinsA)
                    else:
                        AppendPhrase.append(AppendBlank)

                    if setB == 1:
                        AppendPhrase.append(StoreBinsB)
                    else:
                        AppendPhrase.append(AppendBlank)

                    if setC == 1:
                        AppendPhrase.append(StoreBinsC)
                    else:
                        AppendPhrase.append(AppendBlank)
                    HistogramPenStorage.append(AppendPhrase)
            HowManyInt=HowManyInt+1
        GraphStoreA.append(StoreBinsAGraph)
        GraphStoreB.append(StoreBinsBGraph)
        GraphStoreC.append(StoreBinsCGraph)
        print 'penetration'
        print HistogramPenStorage
        HistogramFullStorage.append(HistogramPenStorage)
        HistogramFullStorageHM.append(HistogramPenStorageHM)
    GraphStore.append(GraphStoreA)
    GraphStore.append(GraphStoreB)
    GraphStore.append(GraphStoreC)



    return HistogramFullStorage, GraphStore,HistogramFullStorageHM

def Processing(xfmrStorage, xfmr_byphaseStorage, cableStorage, TimeRange, XfmrVolt, ByPhaseVolt, CableVolt, IntByPhaseStorage,IntByPhaseVolt, NamesAll, HowMany, ByPhaseVoltDrop, CableVoltDrop, XfmrVoltOut):
    print 'xfmr'
    print '\n'
    print xfmrStorage[0]
    print 'Things I need'
    print xfmrStorage
    print XfmrVolt



    XfmrStorageFull, XfmrLenOverFull, XfmrVoltStorageFull, XfmrVoltOutput,XfmrVoltageTrend, XfmrLoadingTrend, WorstValues=OverloadGathering(xfmrStorage, TimeRange, XfmrVolt)
    print '1'
    print XfmrLoadingTrend[0]
    print len(XfmrLoadingTrend[0])
    print type(XfmrLoadingTrend[0])
    print '2'
    print XfmrLoadingTrend[1]
    print len(XfmrLoadingTrend[1])
    print type(XfmrLoadingTrend[1])
    print '3'
    print XfmrVoltageTrend[0]
    print len(XfmrVoltageTrend[0])
    print type(XfmrVoltageTrend[0])
    print '4'
    print XfmrVoltageTrend[1]
    print len(XfmrVoltageTrend[1])
    print type(XfmrVoltageTrend[1])
    print '5'
    print XfmrVoltOutput[0]
    print len(XfmrVoltOutput[0])
    print type(XfmrVoltOutput[0])
    print '6'
    print XfmrVoltOutput[1]
    print len(XfmrVoltOutput[1])
    print type(XfmrVoltOutput[1])


    XfmrMostStore=HowManyStoring(WorstValues)


    XfmrExcel,ExcelNameHolder, XfmrExcelHM=ExcelFormatCreation(xfmrStorage,XfmrMostStore,XfmrStorageFull,XfmrVoltStorageFull, HowMany)

    XfmrVoltExcel,ExcelNameHolderVolt,XfmrVoltExcelHM=ExcelFormatCreation(XfmrVolt,XfmrMostStore,XfmrStorageFull,XfmrVoltStorageFull, HowMany)

    XfmrVoltOutExcel,Nul1,Nul2=ExcelFormatCreation(XfmrVoltOut,XfmrMostStore,XfmrStorageFull,XfmrVoltStorageFull, HowMany)
    XfmrVoltOut=0
    XfmrHist,XfmrGraph,XfmrHistHM=HistogramFormat(XfmrLenOverFull, XfmrMostStore, HowMany)

    ByPhaseStorageFull, ByPhaseLenOverFull,ByPhaseVoltStorageFull, ByPhaseVoltOutput,ByPhaseVoltageTrend, ByPhaseLoadingTrend, WorstValues=OverloadGathering(xfmr_byphaseStorage, TimeRange, ByPhaseVolt)

    Dropvar1,           Null1,              Dropvar2, Null2,Null3, Null4, Null5=OverloadGathering(xfmr_byphaseStorage, TimeRange, ByPhaseVoltDrop)

    ByPhaseMostStore=HowManyStoring(WorstValues)



    print 'len over, the storage'
    print 'yea'
    assetstore=[]
    print ByPhaseLenOverFull
    print ByPhaseLenOverFull[1]
    '''
    for asset in ByPhaseLenOverFull[2]:
        if asset[1] != [] or asset[2] != [] or asset[3] != []:
            print 'huh'
            assetstore.append(asset)
    print 'bet'
    assetstore2 = []
    for asset in ByPhaseStorageFull[2]:
        if asset[1] != 0 or asset[2] != 0 or asset[3] != 0:
            print 'let'
            assetstore2.append(asset)
    print 'prints of len over and storage after finding non nulls'
    print assetstore
    print assetstore2
    assetall=[]
    for asset in assetstore:
        for asset2 in assetstore2:
            if asset[0] == asset2[0]:
                print 'asset one, then two'
                print asset
                print asset2
                assetall.append(asset)
                assetall.append(asset2)
    '''

    ByPhaseExcel,ExcelNameHolder, ByPhaseExcelHM = ExcelFormatCreation(xfmr_byphaseStorage, ByPhaseMostStore, ByPhaseStorageFull,ByPhaseVoltStorageFull, HowMany)

    ByPhaseVoltExcel,ExcelNameHolder, ByPhaseVoltExcelHM = ExcelFormatCreation(ByPhaseVolt, ByPhaseMostStore, ByPhaseStorageFull,ByPhaseVoltStorageFull, HowMany)

    ByPhaseVoltDropExcel, Null1, Null2 = ExcelFormatCreation(ByPhaseVoltDrop, ByPhaseMostStore, Dropvar1, Dropvar2, HowMany)

    ByPhaseHist,ByPhaseGraph,ByPhaseHistHM = HistogramFormat(ByPhaseLenOverFull, ByPhaseMostStore, HowMany)
    '''
    print 'values'
    LenOverVal=[]
    for val in ByPhaseLenOverFull[1]:
        Check=0


        if val[1] != [] or val[2] != [] or val[3] != []:
            for value in val[1]:
                if value >= 3:
                    Check=1
            for value in val[2]:
                if value >= 3:
                    Check=1
            for value in val[3]:
                if value >= 3:
                    Check=1
            if Check == 1:
                LenOverVal.append(val)

    ByPhaseVal=[]
    for val in ByPhaseHist[1]:
        if val != []:
            ByPhaseVal.append(val)
    print ByPhaseVal
    print 'blah'
    namestore=[]
    valuestorage=0
    print ByPhaseMostStore
    print ByPhaseMostStore[0]
    print ByPhaseVal
    print LenOverVal
    print LenOverVal[0]
    
    for val in ByPhaseMostStore:
        namestore.append(val[0])
        for value in LenOverVal:
            if value[0] == val[0]:

                if valuestorage < 10:
                    print 'stuff'
                    print value
                    print value[1]
                    print type(value[1])
                    if value[1] != [len(TimeRange)] and value[1] != [] or value[2] != [len(TimeRange)] and value[2] != [] or value[3] != [len(TimeRange)] and value[3] != []:
                        print 'value'
                        print value
                        valuestorage=valuestorage+1
    
    stopping=0
    print '1'
    for i in range(0, len(ByPhaseVal)):
        if ByPhaseVal[i][1] != [0, 0, 0, 0, 0, 0, 0, 0, 0, 1] and stopping < 9:
            print ByPhaseVal[i]
            for val in ByPhaseLenOverFull[1]:
                if val[0] == ByPhaseVal[i][0]:
                    print val

    print '2'
    print ExcelNameHolder[0:9]
    print '3'
    print ByPhaseMostStore[0:9]
    print 'hmm'
    for val in ByPhaseLenOverFull[0]:
        if val[1] != [] or val[2] != [] or val[3] != []:
            print val
    print '1'
    for val in ByPhaseLenOverFull[1]:
        if val[1] != [] or val[2] != [] or val[3] != []:
            print val

    print '2'
    print '2'

    for val in ByPhaseHist[0]:
        if val != []:
            print val

    print '3'
    for val in ByPhaseHist[1]:
        if val != []:
            print val
    print 'Processing Use Case'
    '''

    if NamesAll != []:
        IntByPhaseStorageFull, IntByPhaseLenOverFull,IntByPhaseVoltStorageFull, IntByPhaseVoltOutput,IntByPhaseVoltageTrend, IntByPhaseLoadingTrend, WorstValues=OverloadGathering(IntByPhaseStorage, TimeRange, IntByPhaseVolt)

        IntByPhaseMostStore=HowManyStoring(WorstValues)

        IntByPhaseExcel,ExcelNameHolder ,IntByPhaseExcelHM= ExcelFormatCreation(IntByPhaseStorage, IntByPhaseMostStore, IntByPhaseStorageFull,IntByPhaseVoltStorageFull, HowMany)

        IntByPhaseVoltExcel,ExcelNameHolder,IntByPhaseVoltExcelHM = ExcelFormatCreation(IntByPhaseVolt, IntByPhaseMostStore, IntByPhaseStorageFull,IntByPhaseVoltStorageFull, HowMany)

        IntByPhaseHist,IntByPhaseGraph,IntByPhaseHistHM = HistogramFormat(IntByPhaseLenOverFull, IntByPhaseMostStore, HowMany)
    else:
        IntByPhaseExcel=0
        IntByPhaseMostStore=0
        IntByPhaseVoltExcel=0
        IntByPhaseHist=0
        IntByPhaseExcelHM=0
        IntByPhaseVoltExcelHM=0
        IntByPhaseHistHM=0

    CableStorageFull, CableLenOverFull,CableVoltStorageFull, CableVoltOutput,CableVoltageTrend, CableLoadingTrend, WorstValues=OverloadGathering(cableStorage, TimeRange, CableVolt)

    #Dropvar1,           Null1,              Dropvar2, Null2,Null3, Null4, Null5=OverloadGathering(cableStorage, TimeRange, CableVoltDrop)
    CableMostStore=HowManyStoring(WorstValues)

    CableExcel,ExcelNameHolder,CableExcelHM = ExcelFormatCreation(cableStorage, CableMostStore, CableStorageFull,CableVoltStorageFull, HowMany)

    CableVoltExcel,ExcelNameHolder, CableVoltExcelHM= ExcelFormatCreation(CableVolt, CableMostStore, CableStorageFull, CableVoltStorageFull, HowMany)
    CableVoltDropExcel=[]
    #CableVoltDropExcel, Null1, Null2 = ExcelFormatCreation(CableVoltDrop, CableMostStore, Dropvar1, Dropvar2, HowMany)

    CableHist, CableGraph,CableHistHM = HistogramFormat(CableLenOverFull,CableMostStore, HowMany)


    FullVoltage=[]
    FullVoltage.append(XfmrVoltOutput)
    FullVoltage.append(ByPhaseVoltOutput)
    FullVoltage.append(CableVoltOutput)
    if NamesAll != []:
        FullVoltage.append(IntByPhaseVoltOutput)
    GraphStorage=[]
    GraphStorage.append(XfmrGraph)
    GraphStorage.append(ByPhaseGraph)
    GraphStorage.append(CableGraph)
    if NamesAll != []:
        GraphStorage.append(IntByPhaseGraph)
    VoltageTrendStore=[]
    VoltageTrendStore.append(XfmrVoltageTrend)
    VoltageTrendStore.append(ByPhaseVoltageTrend)
    VoltageTrendStore.append(CableVoltageTrend)
    if NamesAll != []:
        VoltageTrendStore.append(IntByPhaseVoltageTrend)
    LoadingTrendStore=[]
    LoadingTrendStore.append(XfmrLoadingTrend)
    LoadingTrendStore.append(ByPhaseLoadingTrend)
    LoadingTrendStore.append(CableLoadingTrend)
    if NamesAll != []:
        LoadingTrendStore.append(IntByPhaseLoadingTrend)

    xfmrStorage=0
    xfmr_byphaseStorage=0
    cableStorage=0
    XfmrVolt=0
    ByPhaseVolt=0
    CableVolt=0
    IntByPhaseStorage=0
    IntByPhaseVolt=0

    XfmrVoltOutput = 0
    ByPhaseVoltOutput = 0
    CableVoltOutput = 0
    IntByPhaseVoltOutput = 0

    XfmrGraph = 0
    ByPhaseGraph = 0
    CableGraph = 0
    IntByPhaseGraph = 0

    XfmrVoltageTrend = 0
    ByPhaseVoltageTrend = 0
    CableVoltageTrend = 0
    IntByPhaseVoltageTrend = 0

    XfmrLoadingTrend = 0
    ByPhaseLoadingTrend = 0
    CableLoadingTrend = 0
    IntByPhaseLoadingTrend = 0
    XfmrStorageFull=0
    XfmrLenOverFull=0
    XfmrVoltStorageFull=0
    ByPhaseStorageFull = 0
    ByPhaseLenOverFull = 0
    ByPhaseVoltStorageFull = 0
    CableStorageFull = 0
    CableLenOverFull = 0
    CableVoltStorageFull = 0
    IntByPhaseStorageFull = 0
    IntByPhaseLenOverFull = 0
    IntByPhaseVoltStorageFull = 0
    ExcelNameHolder=0
    CableVoltDrop=0
    ByPhaseVoltDrop=0

    return XfmrExcel, XfmrMostStore,XfmrVoltExcel, ByPhaseExcel, ByPhaseMostStore,ByPhaseVoltExcel,CableExcel, CableMostStore,CableVoltExcel, XfmrHist,ByPhaseHist,FullVoltage,GraphStorage,IntByPhaseExcel, IntByPhaseMostStore,IntByPhaseVoltExcel,IntByPhaseHist, VoltageTrendStore, LoadingTrendStore,XfmrExcelHM,XfmrVoltExcelHM,XfmrHistHM,ByPhaseExcelHM,ByPhaseVoltExcelHM,ByPhaseHistHM,IntByPhaseExcelHM,IntByPhaseVoltExcelHM,IntByPhaseHistHM,CableExcelHM,CableVoltExcelHM,CableHistHM, ByPhaseVoltDropExcel, CableVoltDropExcel , XfmrVoltOutExcel

def TimeFlow(num,xfmr, xfmr_byphase, cable,AppliedNames, UnAppliedNames,Current_Filename, cable_true):


    if num == 3:

        start = datetime.now()
        cympy.study.Save(Current_Filename)
        cympy.study.Close(False)
        cympy.study.Close(False)
        cympy.study.Open(Current_Filename)
        end = datetime.now()
        print('if num == 3 in ' + str((end - start).total_seconds()) + ' seconds')
        print 'saved and opened'
        num=0


    num=num+1
    load_flow = cympy.sim.LoadFlow()
    start = datetime.now()


    load_flow.Run()
    end = datetime.now()
    print('Try Except Done in ' + str((end - start).total_seconds()) + ' seconds')


    xfmrAppend =[]
    ByPhaseAppend = []
    LineAppend = []
    LineAppend2 = []
    xfmrAppendVolt = []
    ByPhaseAppendVolt = []
    ByPhaseAppendVoltExtra =[]
    LineAppendVolt = []
    LineAppendVolt2 = []
    LineAppendVoltExtra=[]
    IntByPhaseAppend = []
    IntByPhaseAppendVolt = []
    ByPhaseAppendVoltDrop=[]
    LineAppendVoltDrop = []
    xfmrAppendVoltOut=[]

    XfmrInvalid=0
    ByPhaseInvalid=0
    CableInvalid=0

    device_increment = 0
    start = datetime.now()

    for name in xfmr['device_number']:

        #Transformers deviceID is 1
        deviceID=1
        #Checks too see if Query result is valid
        LoadA=0.0
        LoadB=0.0
        LoadC=0.0
        if cympy.study.QueryInfoDevice("LOADINGA", name, deviceID) != '':
            LoadA=float(cympy.study.QueryInfoDevice("LOADINGA", name, deviceID))
        if cympy.study.QueryInfoDevice("LOADINGB", name, deviceID) != '':
            LoadB=float(cympy.study.QueryInfoDevice("LOADINGB", name, deviceID))
        if cympy.study.QueryInfoDevice("LOADINGC", name, deviceID) != '':
            LoadC=float(cympy.study.QueryInfoDevice("LOADINGC", name, deviceID))
        VoltA = 0.0
        VoltB = 0.0
        VoltC = 0.0
        VoltAOut = 0.0
        VoltBOut = 0.0
        VoltCOut = 0.0
        if cympy.study.QueryInfoDevice("VpuAinput", name, deviceID) != '':
            VoltA = float(cympy.study.QueryInfoDevice("VpuAinput", name, deviceID))
            VoltAOut = float(cympy.study.QueryInfoDevice("VpuA", name, deviceID))
        if cympy.study.QueryInfoDevice("VpuBinput", name, deviceID) != '':
            VoltB = float(cympy.study.QueryInfoDevice("VpuBinput", name, deviceID))
            VoltBOut = float(cympy.study.QueryInfoDevice("VpuB", name, deviceID))
        if cympy.study.QueryInfoDevice("VpuCinput", name, deviceID) != '':
            VoltC = float(cympy.study.QueryInfoDevice("VpuCinput", name, deviceID))
            VoltCOut = float(cympy.study.QueryInfoDevice("VpuC", name, deviceID))
        xfmrAppendAdd = (name, LoadA, LoadB, LoadC)


        xfmrAppendVoltAdd=(name,VoltA, VoltB, VoltC)
        #print xfmrAppendVoltAdd
        xfmrAppendVolt.append(xfmrAppendVoltAdd)
        xfmrAppendVoltAddOut=(name,VoltAOut, VoltBOut, VoltCOut)
        #print xfmrAppendVoltAdd
        xfmrAppendVoltOut.append(xfmrAppendVoltAddOut)


        xfmrAppend.append(xfmrAppendAdd)
    end = datetime.now()
    print('Transformers Done in ' + str((end - start).total_seconds()) + ' seconds')
    start = datetime.now()

    for name in xfmr_byphase['device_number']:

        # Transformer By Phase has a DeviceID of 33
        deviceID = 33
        Loading_AccurateA = 0.0
        Loading_AccurateB = 0.0
        Loading_AccurateC = 0.0
        VoltA=0.0
        VoltB=0.0
        VoltC=0.0
        VoltAExtra=0
        VoltBExtra = 0
        VoltCExtra = 0
        VoltADrop = 0
        VoltBDrop = 0
        VoltCDrop = 0

        if cympy.study.QueryInfoDevice("LOADINGA", name, deviceID) != '':
            Loading_AccurateA=float(cympy.study.QueryInfoDevice("LOADINGA", name, deviceID))
            VoltADrop = cympy.study.QueryInfoDevice("DvA", name, deviceID)
            VoltA = float(cympy.study.QueryInfoDevice("VpuAinput", name, deviceID))

        if cympy.study.QueryInfoDevice("LOADINGB", name, deviceID) != '':
            Loading_AccurateB=float(cympy.study.QueryInfoDevice("LOADINGB", name, deviceID))
            VoltBDrop = cympy.study.QueryInfoDevice("DvB", name, deviceID)

            VoltB = float(cympy.study.QueryInfoDevice("VpuBinput", name, deviceID))
        if cympy.study.QueryInfoDevice("LOADINGC", name, deviceID) != '':
            Loading_AccurateC=float(cympy.study.QueryInfoDevice("LOADINGC", name, deviceID))
            VoltCDrop = cympy.study.QueryInfoDevice("DvC", name, deviceID)

            VoltC = float(cympy.study.QueryInfoDevice("VpuCinput", name, deviceID))

        '''        
        # Checks the A phase of the ByPhase Transformers
        if cympy.study.QueryInfoDevice("NomKVAA", name, deviceID) != '' and cympy.study.QueryInfoDevice("KVAA", name,
                                                                                                        deviceID) != '':
            LimitA = float(cympy.study.QueryInfoDevice("NomKVAA", name, deviceID))
            kWVA = float(cympy.study.QueryInfoDevice("KVAA", name, deviceID))
            Loading_AccurateA = (kWVA / LimitA) * 100
            VoltA=float(cympy.study.QueryInfoDevice("VpuAinput", name, deviceID))

            VoltADrop = cympy.study.QueryInfoDevice("DvA", name, deviceID)
            if name == 'C:25 59851':
                VoltAExtra=cympy.study.QueryInfoDevice("VpuA", name, deviceID)

        # Checks the B phase of the ByPhase Transformers
        if cympy.study.QueryInfoDevice("NomKVAB", name, deviceID) != '' and cympy.study.QueryInfoDevice("KVAB", name,
                                                                                                          deviceID) != '':
            LimitB = float(cympy.study.QueryInfoDevice("NomKVAB", name, deviceID))
            kWVB = float(cympy.study.QueryInfoDevice("KVAB", name, deviceID))
            Loading_AccurateB = (kWVB / LimitB) * 100
            VoltB = float(cympy.study.QueryInfoDevice("VpuBinput", name, deviceID))

            VoltBDrop = cympy.study.QueryInfoDevice("DvB", name, deviceID)
            if name == 'C:25 59851': #"C:50 3249-XFO"
                VoltBExtra=cympy.study.QueryInfoDevice("VpuB", name, deviceID)

        # Checks the C phase of the ByPhase Transformers
        if cympy.study.QueryInfoDevice("NomKVAC", name, deviceID) != '' and cympy.study.QueryInfoDevice("KVAC", name,
                                                                                                          deviceID) != '':
            LimitC = float(cympy.study.QueryInfoDevice("NomKVAC", name, deviceID))
            kWVC = float(cympy.study.QueryInfoDevice("KVAC", name, deviceID))
            Loading_AccurateC = (kWVC / LimitC) * 100
            VoltC = float(cympy.study.QueryInfoDevice("VpuCinput", name, deviceID))

            VoltCDrop = cympy.study.QueryInfoDevice("DvC", name, deviceID)
            if name == 'C:25 59851':
                VoltCExtra=cympy.study.QueryInfoDevice("VpuC", name, deviceID)

        '''

        #Only provides valid output for phases it considers
        ByPhaseAppendVoltAdd=(name,VoltA, VoltB, VoltC)

        ByPhaseAppendVolt.append(ByPhaseAppendVoltAdd)
        ByPhaseAppendVoltAddDrop = (name,VoltADrop, VoltBDrop, VoltCDrop)
        ByPhaseAppendVoltDrop.append(ByPhaseAppendVoltAddDrop)

        # Gathers Penetration, device name, and each phases loadings into storage
        ByPhaseAppendAdd = (name, Loading_AccurateA, Loading_AccurateB, Loading_AccurateC)
        #print ByPhaseAppendVoltAdd
        ByPhaseAppend.append(ByPhaseAppendAdd)
    end = datetime.now()
    print('ByPhase Done in ' + str((end - start).total_seconds()) + ' seconds')
    start = datetime.now()

    if AppliedNames != []:
        for name in AppliedNames:
            name=name[0]+'-3'
            # Transformer By Phase has a DeviceID of 33
            deviceID = 33
            Loading_AccurateA = 0.0
            Loading_AccurateB = 0.0
            Loading_AccurateC = 0.0
            VoltA = 0.0
            VoltB = 0.0
            VoltC = 0.0
            VoltAExtra = 0
            VoltBExtra = 0
            VoltCExtra = 0

            # Checks the A phase of the ByPhase Transformers
            if cympy.study.QueryInfoDevice("NomKVAA", name, deviceID) != '' and cympy.study.QueryInfoDevice("KVAA", name,
                                                                                                            deviceID) != '':
                LimitA = float(cympy.study.QueryInfoDevice("NomKVAA", name, deviceID))
                kWVA = float(cympy.study.QueryInfoDevice("KVAA", name, deviceID))
                Loading_AccurateA = (kWVA / LimitA) * 100
                VoltA = float(cympy.study.QueryInfoDevice("VpuAinput", name, deviceID))

            # Checks the B phase of the ByPhase Transformers
            if cympy.study.QueryInfoDevice("NomKVAB", name, deviceID) != '' and cympy.study.QueryInfoDevice("KVAB", name,
                                                                                                              deviceID) != '':
                LimitB = float(cympy.study.QueryInfoDevice("NomKVAB", name, deviceID))
                kWVB = float(cympy.study.QueryInfoDevice("KVAB", name, deviceID))
                Loading_AccurateB = (kWVB / LimitB) * 100
                VoltB = float(cympy.study.QueryInfoDevice("VpuBinput", name, deviceID))
            # Checks the C phase of the ByPhase Transformers
            if cympy.study.QueryInfoDevice("NomKVAC", name, deviceID) != '' and cympy.study.QueryInfoDevice("KVAC", name,
                                                                                                              deviceID) != '':
                LimitC = float(cympy.study.QueryInfoDevice("NomKVAC", name, deviceID))
                kWVC = float(cympy.study.QueryInfoDevice("KVAC", name, deviceID))
                Loading_AccurateC = (kWVC / LimitC) * 100
                VoltC = float(cympy.study.QueryInfoDevice("VpuCinput", name, deviceID))



            # Only provides valid output for phases it considers
            IntByPhaseAppendVoltAdd = (name, VoltA, VoltB, VoltC)
            IntByPhaseAppendVolt.append(IntByPhaseAppendVoltAdd)

            # Gathers Penetration, device name, and each phases loadings into storage
            IntByPhaseAppendAdd = (name, Loading_AccurateA, Loading_AccurateB, Loading_AccurateC)
            # print ByPhaseAppendVoltAdd
            IntByPhaseAppend.append(IntByPhaseAppendAdd)

    if UnAppliedNames != []:
        for name in UnAppliedNames:
            name=name[0]+'-3'
            # Transformer By Phase has a DeviceID of 33
            deviceID = 33
            Loading_AccurateA = 0.0
            Loading_AccurateB = 0.0
            Loading_AccurateC = 0.0
            VoltA = 0.0
            VoltB = 0.0
            VoltC = 0.0



            # Only provides valid output for phases it considers
            IntByPhaseAppendVoltAdd = (name, 0.0, 0.0, 0.0)
            IntByPhaseAppendVolt.append(IntByPhaseAppendVoltAdd)

            # Gathers Penetration, device name, and each phases loadings into storage
            IntByPhaseAppendAdd = (name, 0.0, 0.0, 0.0)
            # print ByPhaseAppendVoltAdd
            IntByPhaseAppend.append(IntByPhaseAppendAdd)
    end = datetime.now()
    print('Intentional Transformers Done in ' + str((end - start).total_seconds()) + ' seconds')
    start = datetime.now()
    Storesection=[]
    for name in cable['device_number']:

        #Overline per Phase deviceID = 13, Not per Phrase deviceID = 11
        deviceID=13

        #Checks to see if there are valid results
        LoadA = 0.0
        LoadB = 0.0
        LoadC = 0.0
        if cympy.study.QueryInfoDevice("LOADINGA", name, deviceID) != '':
            LoadA = float(cympy.study.QueryInfoDevice("LOADINGA", name, deviceID))
        if cympy.study.QueryInfoDevice("LOADINGB", name, deviceID) != '':
            LoadB = float(cympy.study.QueryInfoDevice("LOADINGB", name, deviceID))
        if cympy.study.QueryInfoDevice("LOADINGC", name, deviceID) != '':
            LoadC = float(cympy.study.QueryInfoDevice("LOADINGC", name, deviceID))
        VoltA = 0.0
        VoltB = 0.0
        VoltC = 0.0
        VoltADrop = 0.0
        VoltBDrop = 0.0
        VoltCDrop = 0.0
        LineAppendAdd = (name, LoadA, LoadB, LoadC)
        if cympy.study.QueryInfoDevice("VpuAinput", name, deviceID) != '':
            VoltA=float(cympy.study.QueryInfoDevice("VpuAinput", name, deviceID))
            #VoltADrop = cympy.study.QueryInfoDevice("DvA", name, deviceID)
        if cympy.study.QueryInfoDevice("VpuBinput", name, deviceID) != '':
            VoltB=float(cympy.study.QueryInfoDevice("VpuBinput", name, deviceID))
            #VoltBDrop = cympy.study.QueryInfoDevice("DvB", name, deviceID)
        if cympy.study.QueryInfoDevice("VpuCinput", name, deviceID) != '':
            VoltC=float(cympy.study.QueryInfoDevice("VpuCinput", name, deviceID))

            #VoltCDrop = cympy.study.QueryInfoDevice("DvC", name, deviceID)
        #pu value of voltage at each phase
        LineAppendVoltAdd=(name,VoltA, VoltB, VoltC)

        LineAppendVolt.append(LineAppendVoltAdd)
        #LineAppendVoltAddDrop=(name,VoltADrop, VoltBDrop, VoltCDrop)

        #LineAppendVoltDrop.append(LineAppendVoltAddDrop)

        LineAppend.append(LineAppendAdd)

    for name in cable_true['device_number']:

        #Overline per Phase deviceID = 13, Not per Phrase deviceID = 11
        deviceID=10

        #Checks to see if there are valid results
        LoadA = 0.0
        LoadB = 0.0
        LoadC = 0.0
        if cympy.study.QueryInfoDevice("LOADINGA", name, deviceID) != '':
            LoadA = float(cympy.study.QueryInfoDevice("LOADINGA", name, deviceID))
        if cympy.study.QueryInfoDevice("LOADINGB", name, deviceID) != '':
            LoadB = float(cympy.study.QueryInfoDevice("LOADINGB", name, deviceID))
        if cympy.study.QueryInfoDevice("LOADINGC", name, deviceID) != '':
            LoadC = float(cympy.study.QueryInfoDevice("LOADINGC", name, deviceID))
        VoltA = 0.0
        VoltB = 0.0
        VoltC = 0.0
        VoltADrop = 0.0
        VoltBDrop = 0.0
        VoltCDrop = 0.0
        LineAppendAdd = (name, LoadA, LoadB, LoadC)
        if cympy.study.QueryInfoDevice("VpuAinput", name, deviceID) != '':
            VoltA=float(cympy.study.QueryInfoDevice("VpuAinput", name, deviceID))
            #VoltADrop = cympy.study.QueryInfoDevice("DvA", name, deviceID)
        if cympy.study.QueryInfoDevice("VpuBinput", name, deviceID) != '':
            VoltB=float(cympy.study.QueryInfoDevice("VpuBinput", name, deviceID))
            #VoltBDrop = cympy.study.QueryInfoDevice("DvB", name, deviceID)
        if cympy.study.QueryInfoDevice("VpuCinput", name, deviceID) != '':
            VoltC=float(cympy.study.QueryInfoDevice("VpuCinput", name, deviceID))

            #VoltCDrop = cympy.study.QueryInfoDevice("DvC", name, deviceID)
        #pu value of voltage at each phase
        LineAppendVoltAdd=(name,VoltA, VoltB, VoltC)

        LineAppendVolt2.append(LineAppendVoltAdd)
        #LineAppendVoltAddDrop=(name,VoltADrop, VoltBDrop, VoltCDrop)

        #LineAppendVoltDrop.append(LineAppendVoltAddDrop)

        LineAppend2.append(LineAppendAdd)


    end = datetime.now()
    print('Cables Done in ' + str((end - start).total_seconds()) + ' seconds')
    start = datetime.now()

    TrueHolder=[]

    variable1=LineAppend
    variable2=LineAppend2

    for value in variable2:

        variable1.append(value)
    TrueHolder.append(variable1)

    TrueHolderVolt=[]

    variable1=LineAppendVolt
    variable2=LineAppendVolt2

    for value in variable2:

        variable1.append(value)
    TrueHolderVolt.append(variable1)



    size=0
    size = size + sys.getsizeof(xfmrAppend)
    for val in xfmrAppend:
        size = size + sys.getsizeof(val)
        for place in val:
            #print type(place)
            size = size + sys.getsizeof(place)
    size = size + sys.getsizeof(ByPhaseAppend)
    for val in ByPhaseAppend:
        size = size + sys.getsizeof(val)
        for place in val:
            #print type(place)
            size = size + sys.getsizeof(place)
    size = size + sys.getsizeof(LineAppend)
    for val in LineAppend:
        size = size + sys.getsizeof(val)
        for place in val:
            #print type(place)
            size = size + sys.getsizeof(place)
    end = datetime.now()
    print('SizeArrival Done in ' + str((end - start).total_seconds()) + ' seconds')
    print 'full size of loading, looped into elements, and looped inside elements is {value}'.format(value=size)
    return xfmrAppend, ByPhaseAppend, TrueHolder[0], xfmrAppendVolt, ByPhaseAppendVolt, TrueHolderVolt[0],num,IntByPhaseAppend, IntByPhaseAppendVolt,ByPhaseAppendVoltExtra,LineAppendVoltExtra,ByPhaseAppendVoltDrop,LineAppendVoltDrop, xfmrAppendVoltOut

def ExportExcel(Penetration,times, XfmrExcel,XfmrWorst, ARealName):
    os.chdir("C:\Users\pwrlab07\Desktop\Sheeran Folder\CSVHolder\\")
    Columns = []
    for name in XfmrWorst:
        AppendName = name[0] + '-A'
        Columns.append(AppendName)
        AppendName = name[0] + '-B'
        Columns.append(AppendName)
        AppendName = name[0] + '-C'
        Columns.append(AppendName)

    val = -1
    for Pen in Penetration:
        val = val + 1
        print 'This is a place, yes'
        print XfmrExcel[val]
        print times
        print Columns
        print type(XfmrExcel[val])
        print type(times)
        print type(Columns)
        EndPoint=(len(XfmrExcel[val][0]))
        print 'huhuhuhuh'
        print XfmrExcel[val][0]
        print len(XfmrExcel[val][0])
        print EndPoint
        print Columns[0:EndPoint]
        string = 'df{pen} = pd.DataFrame(XfmrExcel[val], index=times,columns= Columns[0:EndPoint])'.format(pen=Pen)
        print 'string'
        print string
        print ' Yet Another Test'
        print XfmrExcel[val]
        print times
        print Columns
        print len(XfmrExcel[val])
        print len(times)
        print len(Columns)
        exec (string)


    writer = pd.ExcelWriter(ARealName, engine='xlsxwriter')
    print 'before df.to_excel'
    for Pen in Penetration:
        string = 'df{pen}.to_excel(writer, sheet_name=\'Penetraion {pen}\')'.format(pen=Pen)
        print 'string2'
        print string
        exec (string)
    print 'before writer save'
    writer.save()
    print 'after writer save'
    return

def ExportExcelComplex(Penetration,times, XfmrExcel,ARealName):
    os.chdir("C:\Users\pwrlab07\Desktop\Sheeran Folder\CSVHolder\\")
    Columns = ['real','imag']

    Columns
    val = -1
    for Pen in Penetration:
        val = val + 1
        print 'This is a place, yes'
        print XfmrExcel[val]
        print times
        print Columns
        print type(XfmrExcel[val])
        print type(times)
        print type(Columns)
        EndPoint=(len(XfmrExcel[val][0]))
        print 'huhuhuhuh'
        print XfmrExcel[val][0]
        print len(XfmrExcel[val][0])
        print EndPoint
        print Columns[0:EndPoint]
        string = 'df{pen} = pd.DataFrame(XfmrExcel[val], index=times,columns= Columns[0:EndPoint])'.format(pen=Pen)
        print 'string'
        print string
        print ' Yet Another Test'
        print XfmrExcel[val]
        print times
        print Columns
        print len(XfmrExcel[val])
        print len(times)
        print len(Columns)
        exec (string)


    writer = pd.ExcelWriter(ARealName, engine='xlsxwriter')
    print 'before df.to_excel'
    for Pen in Penetration:
        string = 'df{pen}.to_excel(writer, sheet_name=\'Penetraion {pen}\')'.format(pen=Pen)
        print 'string2'
        print string
        exec (string)
    print 'before writer save'
    writer.save()
    print 'after writer save'
    return

def ExportHistogram(XfmrHist, excelTitle,intval):

    writer = pd.ExcelWriter(excelTitle, engine='xlsxwriter')
    os.chdir("C:\Users\pwrlab07\Desktop\Sheeran Folder\ChartHolder\\")
    # Create a Pandas dataframe from some data.

    for val in XfmrHist[intval]:
        #XfmrHist[intval] is a whole penetration
        #val is a single assets loading
        if val != []:
            intval=-1
            store=[0,0,0]
            print 'val'
            print val
            for place in val:
                print 'place'
                print place
                intval=intval+1
                if intval == 0:
                    assetname=place
                    assetnamebase=assetname
                else:
                    if place != []:

                        if intval == 1:
                            print 'A'
                            assetname=assetname+'_A'
                            store[0]=1
                        elif intval == 2:
                            print 'B'
                            assetname=assetname+'_B'
                            store[1] = 1
                        elif intval == 3:
                            print 'C'
                            assetname=assetname+'_C'
                            store[2] = 1
            step=0
            applied=0
            SetStorage=[]
            for value in store:
                print 'inside'
                print value
                step=step+1
                if value == 1:
                    applied=applied+1

                    for size in val[step]:
                        SetStorage.append(size)
            df = pd.DataFrame({'Data': SetStorage})
            assetname2=''

            h = -1
            for letter in assetname:
                h = h + 1
                if h <= 28:

                    if letter == ':':
                        assetname2 = assetname2 + '-'
                    else:
                        assetname2 = assetname2 + letter
            print "assetname2"
            print assetname2
            print type(assetname2)
            df.to_excel(writer, sheet_name=assetname2)

            workbook = writer.book
            worksheet = writer.sheets[assetname2]
            i=0
            j=0
            for value in store:
                j=j+1
                if value == 1:
                    i=i+1
                    chart = workbook.add_chart({'type': 'column'})
                    num1 = i * 10 - 8
                    num2=i*10+1
                    sheetstring='=\'{sheetname}\'!$B${number1}:$B${number2}'.format(sheetname=assetname2,number1=num1, number2=num2)
                    chart.add_series({'values': sheetstring,
                                      'gap':20})
                    if j ==1:
                        titlestring=assetnamebase+'_A'
                        chart.set_title({'name': titlestring,
                                        'name_font': {'size': 14, 'bold': True}})
                    if j ==2:
                        titlestring=assetnamebase+'_B'
                        chart.set_title({'name': titlestring,
                                        'name_font': {'size': 14, 'bold': True}})
                    if j ==3:
                        titlestring=assetnamebase+'_C'
                        chart.set_title({'name': titlestring,
                                        'name_font': {'size': 14, 'bold': True}})

                    chart.set_x_axis({
                        'name': 'Length of Overload Events (1 = 30 minute bin)',
                        'name_font': {'size': 12, 'bold': True}
                    })

                    chart.set_y_axis({
                        'name': 'Occurance of Events',
                        'name_font': {'size': 12, 'bold': True},
                        'major_gridlines': {'visible': True}
                    })

                    # Insert the chart into the worksheet.
                    worksheet.insert_chart('D2', chart)


                    chart=0

                # Close the Pandas Excel writer and output the Excel file.
    writer.save()
    # Create a Pandas Excel writer using XlsxWriter as the engine.


    # Convert the dataframe to an XlsxWriter Excel object.


    # Get the xlsxwriter workbook and worksheet objects.


    # Create a chart object.


    # Close the Pandas Excel writer and output the Excel file.
    return

def VoltageOutput(FullVoltage, Penetration,excelTitle):
    os.chdir("C:\Users\pwrlab07\Desktop\Sheeran Folder\ChartHold\\")

    writer = pd.ExcelWriter(excelTitle, engine='xlsxwriter')
    value = -1
    print 'Original FullVoltage'
    print FullVoltage
    #FullVoltage=[[[1,4,9],[3,2,6],[9,12,8]],[[2,8,3],[9,2,6],[4,7,1]],[[1,6,2],[7,2,9],[6,2,4]]]
    for Device in FullVoltage:
        value = value + 1
        value2=-1
        storeval=[]
        for phase in Device:
            value2=value2+1
            for val in phase:
                storeval.append(val)
        FullPenetration=[]
        for i in range(0,3):
            for val in Penetration:
                FullPenetration.append(val)

        df = pd.DataFrame(storeval,
                           index= FullPenetration,
        )
        workbook = writer.book
        if value == 0:
            sheetname='Transformer'
        if value == 1:
            sheetname='TransformerByPhase'
        if value == 2:
            sheetname='DistributionLine'
        if value == 3:
            sheetname='IntentionalXfmrByPhase'
        df.to_excel(writer, sheet_name=sheetname)
        Length=len(phase)
        workbook = writer.book
        worksheet = writer.sheets[sheetname]

        chart = workbook.add_chart({'type': 'line'})

        chart.set_title({'name': '{xfmr} Under Voltage Events'.format(xfmr=sheetname),
                                        'name_font': {'size': 14, 'bold': True}})

        chart.set_x_axis({
            'name': 'EV Penetration',
            'name_font': {'size': 12, 'bold': True},
            'major_gridlines': {'visible': True}
        })

        chart.set_y_axis({
            'name': 'Number of Under Voltage Time Periods',
            'name_font': {'size': 12, 'bold': True},
            'major_gridlines': {'visible': True}
        })
        for i in range(0,3):
            AddSheet='={val}!$B${val2}:$B${val3}'.format(val=sheetname,val2=i*Length+2,val3=(i+1)*Length+1)
            AddSheetIndex = '={val}!$A${val2}:$A${val3}'.format(val=sheetname, val2=i * Length + 2,val3=(i + 1) * Length + 1)
            if i == 0:
                seriesname='Phase A'
            if i == 1:
                seriesname='Phase B'
            if i == 2:
                seriesname='Phase C'
            chart.add_series({'values': AddSheet,
                              'name': seriesname,
                              'categories': AddSheetIndex,
                              'line':{'width':1.5}})
        chart.set_legend({'position': 'bottom'})



        # Insert the chart into the worksheet.
        worksheet.insert_chart('D2', chart)
        # Create a Pandas dataframe from some data.
    writer.save()


    return

def VoltageOutputPen(VoltageTrends, Penetration,excelTitle, times):
    os.chdir("C:\Users\pwrlab07\Desktop\Sheeran Folder\ChartHold\\")

    writer = pd.ExcelWriter(excelTitle, engine='xlsxwriter')
    value = -1
    print 'Original VoltageTrends'
    print VoltageTrends[1]
    print Penetration
    print times
    '''
    Penetration=[40,80]
    times=[1,2,3,4,5,6,7,8]
    VoltageTrends=[[[2,5,9,7,2,8,3,1],[4,7,5,9,2,6,3,3]][[6,2,8,3,9,1,6,3],[6,2,7,4,8,2,7,3]][[5,7,2,6,3,1,6,3],[6,3,6,2,1,9,9,9]],[[2,5,9,7,2,8,3,1],[4,7,5,9,2,6,3,3]][[6,2,8,3,9,1,6,3],[6,2,7,4,8,2,7,3]][[5,7,2,6,3,1,6,3],[6,3,6,2,1,9,9,9]],[[2,5,9,7,2,8,3,1],[4,7,5,9,2,6,3,3]][[6,2,8,3,9,1,6,3],[6,2,7,4,8,2,7,3]][[5,7,2,6,3,1,6,3],[6,3,6,2,1,9,9,9]]]
    excelTitle = 'Asset_Under_Voltage_Trends_Use_Case_Per_Penetration.xlsx'
    '''
    for Device in VoltageTrends:
        value = value + 1
        value2=-1
        storeval=[]
        FullTimestep = []
        for phase in Device:
            value2=value2+1
            for timestep in phase:
                x=-1
                for val in timestep:
                    x=x+1


                    storeval.append(val)
                    FullTimestep.append(times[x])


        df = pd.DataFrame(storeval,
                           index= FullTimestep
        )
        workbook = writer.book
        if value == 0:
            sheetname='Transformer'
        if value == 1:
            sheetname='TransformerByPhase'
        if value == 2:
            sheetname='DistributionLine'
        if value == 3:
            sheetname='IntentionalXfmrByPhase'
        df.to_excel(writer, sheet_name=sheetname)
        Length=len(timestep)
        workbook = writer.book
        worksheet = writer.sheets[sheetname]

        chartA = workbook.add_chart({'type': 'line'})
        chartB = workbook.add_chart({'type': 'line'})
        chartC = workbook.add_chart({'type': 'line'})

        chartA.set_title({'name': '{xfmr} Under Voltage Events Phase A'.format(xfmr=sheetname)})
        chartB.set_title({'name': '{xfmr} Under Voltage Events Phase B'.format(xfmr=sheetname)})
        chartC.set_title({'name': '{xfmr} Under Voltage Events Phase C'.format(xfmr=sheetname)})

        chartA.set_x_axis({
            'name': 'Timestep',
            'name_font': {'size': 14, 'bold': True},
            'date_axis': True
        })
        chartB.set_x_axis({
            'name': 'Timestep',
            'name_font': {'size': 14, 'bold': True},
            'date_axis': True
        })
        chartC.set_x_axis({
            'name': 'Timestep',
            'name_font': {'size': 14, 'bold': True},
            'date_axis': True
        })

        chartA.set_y_axis({
            'name': 'Number of Under Voltage Time Periods',
            'name_font': {'size': 14, 'bold': True},
        })
        chartB.set_y_axis({
            'name': 'Number of Under Voltage Time Periods',
            'name_font': {'size': 14, 'bold': True},
        })
        chartC.set_y_axis({
            'name': 'Number of Under Voltage Time Periods',
            'name_font': {'size': 14, 'bold': True},
        })

        for i in range(0,3):
            PenIndex=-1
            for j in range(0,len(phase)):
                PenIndex=PenIndex+1
                AddSheet='={val}!$B${val2}:$B${val3}'.format(val=sheetname,val2=j*Length+i*len(phase)*Length+2,val3=(j+1)*Length+i*len(phase)*Length+1)
                AddSheetIndex = '={val}!$A${val2}:$A${val3}'.format(val=sheetname, val2=j*Length+i*len(phase)*Length+2,val3=(j+1)*Length+i*len(phase)*Length+1)
                seriesname = str(Penetration[PenIndex])
                if i == 0:
                    chartA.add_series({'values': AddSheet,
                                  'name': seriesname,
                                  'categories': AddSheetIndex,
                                  'line':{'width':1.5}})
                if i == 1:
                    chartB.add_series({'values': AddSheet,
                                  'name': seriesname,
                                  'categories': AddSheetIndex,
                                  'line':{'width':1.5}})
                if i == 2:
                    chartC.add_series({'values': AddSheet,
                                  'name': seriesname,
                                  'categories': AddSheetIndex,
                                  'line':{'width':1.5}})
        chartA.set_legend({'position': 'right'})
        chartB.set_legend({'position': 'right'})
        chartC.set_legend({'position': 'right'})

        # Insert the chart into the worksheet.
        worksheet.insert_chart('D2', chartA)
        worksheet.insert_chart('D2', chartB)
        worksheet.insert_chart('D2', chartC)
        # Create a Pandas dataframe from some data.
    writer.save()


    return

def LoadingOutputPen(VoltageTrends, Penetration,excelTitle, times):
    os.chdir("C:\Users\pwrlab07\Desktop\Sheeran Folder\ChartHold\\")

    writer = pd.ExcelWriter(excelTitle, engine='xlsxwriter')
    value = -1
    print 'Original VoltageTrends'
    print VoltageTrends[1]
    print Penetration
    print times
    '''
    Penetration=[40,80]
    times=[1,2,3,4,5,6,7,8]
    VoltageTrends=[[[2,5,9,7,2,8,3,1],[4,7,5,9,2,6,3,3]][[6,2,8,3,9,1,6,3],[6,2,7,4,8,2,7,3]][[5,7,2,6,3,1,6,3],[6,3,6,2,1,9,9,9]],[[2,5,9,7,2,8,3,1],[4,7,5,9,2,6,3,3]][[6,2,8,3,9,1,6,3],[6,2,7,4,8,2,7,3]][[5,7,2,6,3,1,6,3],[6,3,6,2,1,9,9,9]],[[2,5,9,7,2,8,3,1],[4,7,5,9,2,6,3,3]][[6,2,8,3,9,1,6,3],[6,2,7,4,8,2,7,3]][[5,7,2,6,3,1,6,3],[6,3,6,2,1,9,9,9]]]
    excelTitle = 'Asset_Under_Voltage_Trends_Use_Case_Per_Penetration.xlsx'
    '''
    for Device in VoltageTrends:
        value = value + 1
        value2=-1
        storeval=[]
        FullTimestep = []
        for phase in Device:
            value2=value2+1
            for timestep in phase:
                x=-1
                for val in timestep:
                    x=x+1


                    storeval.append(val)
                    FullTimestep.append(times[x])


        df = pd.DataFrame(storeval,
                           index= FullTimestep
        )
        workbook = writer.book
        if value == 0:
            sheetname='Transformer'
        if value == 1:
            sheetname='TransformerByPhase'
        if value == 2:
            sheetname='DistributionLine'
        if value == 3:
            sheetname='IntentionalXfmrByPhase'
        df.to_excel(writer, sheet_name=sheetname)
        Length=len(timestep)
        workbook = writer.book
        worksheet = writer.sheets[sheetname]

        chartA = workbook.add_chart({'type': 'line'})
        chartB = workbook.add_chart({'type': 'line'})
        chartC = workbook.add_chart({'type': 'line'})

        chartA.set_title({'name': '{xfmr} Over Loading Events Per Time Step Phase A'.format(xfmr=sheetname)})
        chartB.set_title({'name': '{xfmr} Over Loading Events Per Time Step Phase B'.format(xfmr=sheetname)})
        chartC.set_title({'name': '{xfmr} Over Loading Events Per Time Step Phase C'.format(xfmr=sheetname)})

        chartA.set_x_axis({
            'name': 'Timestep',
            'name_font': {'size': 14, 'bold': True},
            'date_axis': True
        })
        chartB.set_x_axis({
            'name': 'Timestep',
            'name_font': {'size': 14, 'bold': True},
            'date_axis': True
        })
        chartC.set_x_axis({
            'name': 'Timestep',
            'name_font': {'size': 14, 'bold': True},
            'date_axis': True
        })

        chartA.set_y_axis({
            'name': 'Number of Overloaded Time Periods',
            'name_font': {'size': 14, 'bold': True},
        })
        chartB.set_y_axis({
            'name': 'Number of Overloaded Time Periods',
            'name_font': {'size': 14, 'bold': True},
        })
        chartC.set_y_axis({
            'name': 'Number of Overloaded Time Periods',
            'name_font': {'size': 14, 'bold': True},
        })

        for i in range(0,3):
            PenIndex=-1
            for j in range(0,len(phase)):
                PenIndex=PenIndex+1
                AddSheet='={val}!$B${val2}:$B${val3}'.format(val=sheetname,val2=j*Length+i*len(phase)*Length+2,val3=(j+1)*Length+i*len(phase)*Length+1)
                AddSheetIndex = '={val}!$A${val2}:$A${val3}'.format(val=sheetname, val2=j*Length+i*len(phase)*Length+2,val3=(j+1)*Length+i*len(phase)*Length+1)
                seriesname = str(Penetration[PenIndex])
                if i == 0:
                    chartA.add_series({'values': AddSheet,
                                  'name': seriesname,
                                  'categories': AddSheetIndex,
                                  'line':{'width':1.5}})
                if i == 1:
                    chartB.add_series({'values': AddSheet,
                                  'name': seriesname,
                                  'categories': AddSheetIndex,
                                  'line':{'width':1.5}})
                if i == 2:
                    chartC.add_series({'values': AddSheet,
                                  'name': seriesname,
                                  'categories': AddSheetIndex,
                                  'line':{'width':1.5}})
        chartA.set_legend({'position': 'bottom'})
        chartB.set_legend({'position': 'bottom'})
        chartC.set_legend({'position': 'bottom'})

        # Insert the chart into the worksheet.
        worksheet.insert_chart('D2', chartA)
        worksheet.insert_chart('D2', chartB)
        worksheet.insert_chart('D2', chartC)
        # Create a Pandas dataframe from some data.
    writer.save()


    return

def LoadingGraphOutput(GraphStorage, Penetration):
    os.chdir("C:\Users\pwrlab07\Desktop\Sheeran Folder\ChartHold\\")
    excelTitle = 'Asset_Loading_Trends_Use_Case.xlsx'
    writer = pd.ExcelWriter(excelTitle, engine='xlsxwriter')
    value=-1
    for Device in GraphStorage:
        value=value+1
        storeval = []
        for phase in Device:
            for pen in phase:
                for val in pen:
                    storeval.append(val)
        Bins=[1,2,3,4]
        FullSteps=[]
        for j in range(0,len(Penetration)):
            for i in range(0,3):
                for val in Bins:
                    FullSteps.append(val)
        print 'val'
        print val
        print type(val)
        print pen
        print type(pen)
        print phase
        print type(phase)
        print Device
        print type(Device)
        print 'storeval'
        print storeval
        print FullSteps
        df = pd.DataFrame(storeval,
                           index= FullSteps
                            )
        workbook = writer.book
        if value == 0:
            sheetname = 'Transformer'
        if value == 1:
            sheetname = 'TransformerByPhase'
        if value == 2:
            sheetname = 'DistributionLine'
        if value == 3:
            sheetname = 'IntentionalXfmrByPhase'
        df.to_excel(writer, sheet_name=sheetname)
        workbook = writer.book
        worksheet = writer.sheets[sheetname]
        Length=len(Penetration)
        for j in range(0,3):

            chart = workbook.add_chart({'type': 'line'})
            if j == 0:
                stringTitle = 'A'
            if j == 1:
                stringTitle = 'B'
            if j == 2:
                stringTitle = 'C'

            chart.set_title({
                'name': '{xfmr} Over-Loading Events Phase {string}'.format(xfmr=sheetname,string=stringTitle),
                'name_font': {'size': 12},
            })


            chart.set_legend({'position': 'bottom'})
            for i in range(0,Length):
                AddSheet='={val}!$B${val2}:$B${val3}'.format(val=sheetname,val2=i*4+2+4*Length*j,val3=(i+1)*4+1+4*Length*j)
                AddSheetIndex = '={val}!$A${val2}:$A${val3}'.format(val=sheetname,val2=i*4+2+4*Length*j,val3=(i+1)*4+1+4*Length*j)
                seriesname='Penetraiton_{val}'.format(val=Penetration[i])
                #seriesname='Penetration_{val}'.format(val=Penetration[i])
                chart.add_series({'values': AddSheet,
                                  'name': seriesname,
                                  'categories': AddSheetIndex,
                                  'line':{'width':1.5}
                                  })
            chart.set_x_axis({
                'name': 'Bin Duration values (1 = 1:00-1:59)',
                'name_font': {'size': 12},
            })

            chart.set_y_axis({
                'name': 'Number of Loading Events',
                'name_font': {'size': 12},
            })
            worksheet.insert_chart('D2', chart)
    writer.save()

    return

def CSVOutputs(Penetration, XfmrExcel,XfmrWorst, ByPhaseExcel,ByPhaseWorst, CableExcel,CableWorst, XfmrVoltExcel, ByPhaseVoltExcel, CableVoltExcel,XfmrHist,ByPhaseHist,FullVoltage,GraphStorage,IntByPhaseExcel,IntByPhaseWorst, IntByPhaseVoltExcel,IntByPhaseHist, VoltageTrendStore, LoadingTrendStore, NamesAll, TimeRange,XfmrExcelHM,XfmrVoltExcelHM,XfmrHistHM,ByPhaseExcelHM,ByPhaseVoltExcelHM,ByPhaseHistHM,IntByPhaseExcelHM,IntByPhaseVoltExcelHM,IntByPhaseHistHM,CableExcelHM,CableVoltExcelHM,CableHistHM,times, ByPhaseVoltDropExcel,CableVoltDropExcel,XfmrVoltOutExcel):
    print 'huh?'

    timesExcel=times
    timesExcel.insert(0, '1/1/2010 0:00')

    timesExcel.insert(0, '1/1/2010 0:00')
    '''
    print times
    print 'These values'
    print XfmrExcel
    print len(XfmrExcel)
    print XfmrExcelHM
    print len(XfmrExcelHM)
    print 'First value'
    print XfmrExcel[0]
    print len(XfmrExcel[0])
    print XfmrExcelHM[0]
    print len(XfmrExcelHM[0])
    print 'done with this part'
    '''
    print '1'
    name = ('Transformer_Loading.xlsx')
    ExportExcel(Penetration,timesExcel, XfmrExcel,XfmrWorst, name)
    XfmrExcel=0
    '''
    name = ('Transformer_Loading_Worst_Assets.xlsx')
    ExportExcel(Penetration, timesExcel, XfmrExcelHM, XfmrWorst, name)
    '''
    XfmrExcelHM = 0
    print '2'
    name = ('By_Phase_Transformer_Loading.xlsx')
    ExportExcel(Penetration,timesExcel, ByPhaseExcel,ByPhaseWorst, name)
    ByPhaseExcel = 0
    '''
    name = ('By_Phase_Transformer_Loading_Worst_Assets.xlsx')
    ExportExcel(Penetration, timesExcel, ByPhaseExcelHM, ByPhaseWorst, name)
    '''
    ByPhaseExcelHM = 0

    print '3'
    name = ('Transmission_Line_Loading.xlsx')
    ExportExcel(Penetration,timesExcel, CableExcel,CableWorst, name)
    CableExcel = 0
    '''
    name = ('Transmission_Line_Loading_Worst_Assets.xlsx')
    ExportExcel(Penetration,timesExcel, CableExcelHM,CableWorst, name)
    CableExcelHM = 0
    '''
    print '4'
    name = ('Transformer_Voltage_Level.xlsx')
    ExportExcel(Penetration,timesExcel, XfmrVoltExcel,XfmrWorst, name)
    XfmrVoltExcel=0
    name = ('Transformer_Voltage_Level_Distribution_Side.xlsx')
    ExportExcel(Penetration,timesExcel, XfmrVoltOutExcel,XfmrWorst, name)
    XfmrVoltExcel=0
    '''
    name = ('Transformer_Voltage_Level_Worst_Assets.xlsx')
    ExportExcel(Penetration,timesExcel, XfmrVoltExcelHM,XfmrWorst, name)
    '''
    XfmrVoltExcelHM = 0
    print '5'
    name = ('By_Phase_Transformer_Voltage_Level.xlsx')
    ExportExcel(Penetration,timesExcel, ByPhaseVoltExcel,ByPhaseWorst, name)
    ByPhaseVoltExcel=0

    name = ('By_Phase_Transformer_Voltage_Drop.xlsx')
    ExportExcel(Penetration,timesExcel, ByPhaseVoltDropExcel,ByPhaseWorst, name)
    ByPhaseVoltDropExcel=0
    '''
    name = ('By_Phase_Transformer_Voltage_Level_Worst_Assets.xlsx')
    ExportExcel(Penetration,timesExcel, ByPhaseVoltExcelHM,ByPhaseWorst, name)
    '''
    ByPhaseVoltExcelHM=0
    print '6'

    name = ('Transmission_Line_Voltage_Level.xlsx')
    ExportExcel(Penetration,timesExcel, CableVoltExcel,CableWorst, name)
    CableVoltExcel=0
    #name = ('Transmission_Line_Voltage_Drop.xlsx')
    #ExportExcel(Penetration,timesExcel, CableVoltDropExcel,CableWorst, name)
    CableVoltDropExcel=0

    '''
    name = ('Transmission_Line_Voltage_Level_Worst_Assets.xlsx')
    ExportExcel(Penetration,timesExcel, CableVoltExcelHM,CableWorst, name)
    '''
    CableVoltExcel=0
    if NamesAll != []:
        name = ('Intentional_By_Phase_Transformer_Loading.xlsx')
        ExportExcel(Penetration,timesExcel, IntByPhaseExcel,IntByPhaseWorst, name)
        IntByPhaseExcel=0
        name = ('Intentional_By_Phase_Transformer_Loading_Worst_Assets.xlsx')
        ExportExcel(Penetration, timesExcel, IntByPhaseExcelHM, IntByPhaseWorst, name)
        IntByPhaseExcelHM = 0
        name = ('Intentional_By_Phase_Transformer_Voltage_Level.xlsx')
        ExportExcel(Penetration,timesExcel, IntByPhaseVoltExcel,IntByPhaseWorst, name)
        IntByPhaseVoltExcel=0
        name = ('Intentional_By_Phase_Transformer_Voltage_Level_Worst_Assets.xlsx')
        ExportExcel(Penetration,timesExcel, IntByPhaseVoltExcelHM,IntByPhaseWorst, name)
        IntByPhaseVoltExcelHM=0



    val = -1
    for Pen in Penetration:
        val = val + 1
        excelTitle = 'Transformer_Loading_Histograms_{penetration}.xlsx'.format(penetration=Pen)
        ExportHistogram(XfmrHist,excelTitle,val)
    XfmrHist=0
    val = -1
    for Pen in Penetration:
        val = val + 1
        excelTitleByPhase = 'By_Phase_Transformer_Loading_Histograms_{penetration}.xlsx'.format(penetration=Pen)
        ExportHistogram(ByPhaseHist, excelTitleByPhase, val)
    ByPhaseHist=0
    val = -1
    for Pen in Penetration:
        val = val + 1
        excelTitle = 'Transformer_Loading_Histograms_{penetration}_Worst_Assets.xlsx'.format(penetration=Pen)
        ExportHistogram(XfmrHistHM,excelTitle,val)
    XfmrHistHM=0
    val = -1
    for Pen in Penetration:
        val = val + 1
        excelTitleByPhase = 'By_Phase_Transformer_Loading_Histograms_{penetration}_Worst_Assets.xlsx'.format(penetration=Pen)
        ExportHistogram(ByPhaseHistHM, excelTitleByPhase, val)
    ByPhaseHistHM=0
    if NamesAll != []:
        val = -1
        for Pen in Penetration:
            val = val + 1
            excelTitleByPhase = 'Intentional_By_Phase_Transformer_Loading_Histograms_{penetration}.xlsx'.format(penetration=Pen)
            ExportHistogram(IntByPhaseHist, excelTitleByPhase, val)
        IntByPhaseHist=0
        val = -1
        for Pen in Penetration:
            val = val + 1
            excelTitleByPhase = 'Intentional_By_Phase_Transformer_Loading_Histograms_{penetration}_Worst_Assets.xlsx'.format(
                penetration=Pen)
            ExportHistogram(IntByPhaseHistHM, excelTitleByPhase, val)
        IntByPhaseHistHM = 0





    excelTitle = 'Asset_Under_Voltage_Trends_Use_Case.xlsx'
    VoltageOutput(FullVoltage, Penetration,excelTitle)
    FullVoltage=0
    excelTitle = 'Asset_Under_Voltage_Trends_Use_Case_Per_Pen.xlsx'
    VoltageOutputPen(VoltageTrendStore, Penetration, excelTitle, times)
    excelTitle = 'Asset_Over_Loading_Trends_Use_Case_Per_Pen.xlsx'
    LoadingOutputPen(LoadingTrendStore, Penetration, excelTitle, times)
    VoltageTrendStore=0
    print 'did OutputPen'

    LoadingGraphOutput(GraphStorage, Penetration)

    print 'full completion'

    return
