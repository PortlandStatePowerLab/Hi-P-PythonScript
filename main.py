# -*- coding: utf-8 -*-
# *************************************
# this program completes a full CYME Analysis
# using data from cyme sxst file
# and creates the needed reports
#
#
# PPPPPPPPPPPPPPPPP           GGGGGGGGGGGGGEEEEEEEEEEEEEEEEEEEEEE
# P::::::::::::::::P       GGG::::::::::::GE::::::::::::::::::::E
# P::::::PPPPPP:::::P    GG:::::::::::::::GE::::::::::::::::::::E
# PP:::::P     P:::::P  G:::::GGGGGGGG::::GEE::::::EEEEEEEEE::::E
#   P::::P     P:::::P G:::::G       GGGGGG  E:::::E       EEEEEE
#   P::::P     P:::::PG:::::G                E:::::E
#   P::::PPPPPP:::::P G:::::G                E::::::EEEEEEEEEE
#   P:::::::::::::PP  G:::::G    GGGGGGGGGG  E:::::::::::::::E
#   P::::PPPPPPPPP    G:::::G    G::::::::G  E:::::::::::::::E
#   P::::P            G:::::G    GGGGG::::G  E::::::EEEEEEEEEE
#   P::::P            G:::::G        G::::G  E:::::E
#   P::::P             G:::::G       G::::G  E:::::E       EEEEEE
# PP::::::PP            G:::::GGGGGGGG::::GEE::::::EEEEEEEE:::::E
# P::::::::P             GG:::::::::::::::GE::::::::::::::::::::E
# P::::::::P               GGG::::::GGG:::GE::::::::::::::::::::E
# PPPPPPPPPP                  GGGGGG   GGGGEEEEEEEEEEEEEEEEEEEEEE
#
# *************************************
# -----------------------------------------------------------------------------
# Copyright (c) 2018, Portland General's T&D Planning Team
# All rights reserved.
# -----------------------------------------------------------------------------
#
# 888b     d888        d8888 8888888 888b    888       .d8888b.   .d88888b.  8888888b.  8888888888
# 8888b   d8888       d88888   888   8888b   888      d88P  Y88b d88P" "Y88b 888  "Y88b 888
# 88888b.d88888      d88P888   888   88888b  888      888    888 888     888 888    888 888
# 888Y88888P888     d88P 888   888   888Y88b 888      888        888     888 888    888 8888888
# 888 Y888P 888    d88P  888   888   888 Y88b888      888        888     888 888    888 888
# 888  Y8P  888   d88P   888   888   888  Y88888      888    888 888     888 888    888 888
# 888   "   888  d8888888888   888   888   Y8888      Y88b  d88P Y88b. .d88P 888  .d88P 888
# 888       888 d88P     888 8888888 888    Y888       "Y8888P"   "Y88888P"  8888888P"  8888888888
#
# *********************************************
# Importing needed Libraries from Python
# *********************************************
from __future__ import division
import pandas
import string
import locale
import os
import lookup
from datetime import datetime
import StringIO
import pickle

import numpy as np
import time
from pytz import timezone
import json
import sys
import re
import csv

import math
import ModifySpotLoad
import LoadFlowOverload
import UserInput
import xlwings as xw
from ModifySpotLoad import open_study

pacific = timezone('US/Pacific')

# *********************************************
# Importing CYMPY Library from CYME EXE Folder
# *********************************************
CYMPY_LOCATION = r"C:\Program Files (x86)\CYME\CYME"
sys.path.insert(1, CYMPY_LOCATION)
import cympy
import cympy.rm
import cympy.db
import cympy.eq
import cympy.utils
cympy.app.ActivateRefresh(False)

import function_study_analysis
from definitions import *
import random

# *********************************************
# Opening Self Contained File from directory
# *********************************************
#import cympy
#This adds the EV loads
'''
For a truly correct simulation houses that already have EV's would be ignored, but I don't have access to that information

For a true penetration at least partly, needs to ask user what current penetration is, Real_Pen=Pen .- User_Pen
'''
'''
#CSV Output Use Case
times1=range(60,72)
Penetration=[40,60,80]
LoadStore=[[40, [[('CEDA_WR1', 47.7, 42.1, 43.6), ('CEDA_WR2', 65.5, 53.3, 63.4)], [('CEDA_WR1', 47.8, 42.2, 43.7), ('CEDA_WR2', 65.7, 53.5, 63.7)], [('CEDA_WR1', 47.9, 42.2, 43.7), ('CEDA_WR2', 65.7, 53.4, 63.5)], [('CEDA_WR1', 47.8, 42.2, 43.6), ('CEDA_WR2', 65.6, 53.3, 63.2)], [('CEDA_WR1', 47.9, 42.1, 43.7), ('CEDA_WR2', 65.7, 53.3, 63.4)], [('CEDA_WR1', 48.0, 42.1, 43.8), ('CEDA_WR2', 65.7, 53.3, 63.2)], [('CEDA_WR1', 47.9, 42.2, 44.0), ('CEDA_WR2', 66.0, 53.5, 63.3)], [('CEDA_WR1', 48.3, 42.3, 44.1), ('CEDA_WR2', 66.6, 54.0, 64.1)], [('CEDA_WR1', 48.0, 42.4, 44.1), ('CEDA_WR2', 66.7, 53.8, 64.3)], [('CEDA_WR1', 48.1, 42.3, 44.0), ('CEDA_WR2', 66.3, 53.5, 63.9)], [('CEDA_WR1', 48.0, 42.3, 43.9), ('CEDA_WR2', 66.6, 53.7, 64.1)], [('CEDA_WR1', 48.1, 42.3, 44.0), ('CEDA_WR2', 66.3, 53.6, 63.9)]]], [60, [[('CEDA_WR1', 50.6, 44.8, 46.4), ('CEDA_WR2', 70.3, 56.8, 67.9)], [('CEDA_WR1', 50.8, 44.9, 46.6), ('CEDA_WR2', 70.7, 57.5, 68.5)], [('CEDA_WR1', 50.8, 44.8, 46.6), ('CEDA_WR2', 70.6, 57.0, 68.3)], [('CEDA_WR1', 50.7, 44.7, 46.4), ('CEDA_WR2', 70.3, 56.7, 67.8)], [('CEDA_WR1', 50.8, 44.8, 46.5), ('CEDA_WR2', 70.6, 56.9, 67.9)], [('CEDA_WR1', 50.8, 44.7, 46.5), ('CEDA_WR2', 70.3, 57.0, 67.7)], [('CEDA_WR1', 51.0, 44.8, 46.9), ('CEDA_WR2', 70.8, 57.1, 67.7)], [('CEDA_WR1', 51.4, 45.0, 47.3), ('CEDA_WR2', 71.7, 57.9, 69.1)], [('CEDA_WR1', 51.2, 45.2, 47.2), ('CEDA_WR2', 71.9, 57.8, 69.3)], [('CEDA_WR1', 51.2, 45.1, 46.9), ('CEDA_WR2', 71.5, 57.3, 68.9)], [('CEDA_WR1', 51.1, 45.2, 46.9), ('CEDA_WR2', 71.8, 57.6, 69.1)], [('CEDA_WR1', 51.1, 45.2, 46.9), ('CEDA_WR2', 71.4, 57.5, 68.9)]]], [80, [[('CEDA_WR1', 53.1, 47.0, 48.6), ('CEDA_WR2', 74.2, 59.8, 71.6)], [('CEDA_WR1', 53.3, 47.3, 48.9), ('CEDA_WR2', 74.6, 60.7, 72.6)], [('CEDA_WR1', 53.3, 47.0, 48.9), ('CEDA_WR2', 74.4, 60.0, 72.1)], [('CEDA_WR1', 53.1, 46.9, 48.7), ('CEDA_WR2', 74.2, 59.6, 71.5)], [('CEDA_WR1', 53.2, 47.1, 48.8), ('CEDA_WR2', 74.5, 59.8, 71.8)], [('CEDA_WR1', 53.3, 46.9, 48.8), ('CEDA_WR2', 74.2, 60.0, 71.5)], [('CEDA_WR1', 53.6, 47.0, 49.4), ('CEDA_WR2', 74.9, 60.3, 71.5)], [('CEDA_WR1', 53.9, 47.3, 49.9), ('CEDA_WR2', 75.8, 61.3, 73.1)], [('CEDA_WR1', 53.7, 47.6, 49.8), ('CEDA_WR2', 76.2, 61.2, 73.4)], [('CEDA_WR1', 53.7, 47.6, 49.3), ('CEDA_WR2', 75.6, 60.6, 72.8)], [('CEDA_WR1', 53.6, 47.6, 49.3), ('CEDA_WR2', 75.9, 61.0, 73.1)], [('CEDA_WR1', 53.6, 47.5, 49.3), ('CEDA_WR2', 75.5, 60.8, 72.9)]]]]
VoltStore=[[40, [[('CEDA_WR1', 0.983, 0.984, 0.983), ('CEDA_WR2', 0.983, 0.984, 0.983)], [('CEDA_WR1', 0.983, 0.984, 0.983), ('CEDA_WR2', 0.983, 0.984, 0.983)], [('CEDA_WR1', 0.983, 0.984, 0.983), ('CEDA_WR2', 0.983, 0.984, 0.983)], [('CEDA_WR1', 0.983, 0.984, 0.983), ('CEDA_WR2', 0.983, 0.984, 0.983)], [('CEDA_WR1', 0.983, 0.984, 0.983), ('CEDA_WR2', 0.983, 0.984, 0.983)], [('CEDA_WR1', 0.983, 0.984, 0.983), ('CEDA_WR2', 0.983, 0.984, 0.983)], [('CEDA_WR1', 0.983, 0.984, 0.983), ('CEDA_WR2', 0.983, 0.984, 0.983)], [('CEDA_WR1', 0.983, 0.984, 0.983), ('CEDA_WR2', 0.983, 0.984, 0.983)], [('CEDA_WR1', 0.983, 0.984, 0.983), ('CEDA_WR2', 0.983, 0.984, 0.983)], [('CEDA_WR1', 0.983, 0.984, 0.983), ('CEDA_WR2', 0.983, 0.984, 0.983)], [('CEDA_WR1', 0.983, 0.984, 0.983), ('CEDA_WR2', 0.983, 0.984, 0.983)], [('CEDA_WR1', 0.983, 0.984, 0.983), ('CEDA_WR2', 0.983, 0.984, 0.983)]]], [60, [[('CEDA_WR1', 0.983, 0.983, 0.983), ('CEDA_WR2', 0.983, 0.983, 0.983)], [('CEDA_WR1', 0.983, 0.983, 0.983), ('CEDA_WR2', 0.983, 0.983, 0.983)], [('CEDA_WR1', 0.983, 0.983, 0.983), ('CEDA_WR2', 0.983, 0.983, 0.983)], [('CEDA_WR1', 0.983, 0.983, 0.983), ('CEDA_WR2', 0.983, 0.983, 0.983)], [('CEDA_WR1', 0.983, 0.983, 0.983), ('CEDA_WR2', 0.983, 0.983, 0.983)], [('CEDA_WR1', 0.983, 0.983, 0.983), ('CEDA_WR2', 0.983, 0.983, 0.983)], [('CEDA_WR1', 0.983, 0.983, 0.983), ('CEDA_WR2', 0.983, 0.983, 0.983)], [('CEDA_WR1', 0.983, 0.983, 0.983), ('CEDA_WR2', 0.983, 0.983, 0.983)], [('CEDA_WR1', 0.983, 0.983, 0.983), ('CEDA_WR2', 0.983, 0.983, 0.983)], [('CEDA_WR1', 0.983, 0.983, 0.983), ('CEDA_WR2', 0.983, 0.983, 0.983)], [('CEDA_WR1', 0.983, 0.983, 0.983), ('CEDA_WR2', 0.983, 0.983, 0.983)], [('CEDA_WR1', 0.983, 0.983, 0.983), ('CEDA_WR2', 0.983, 0.983, 0.983)]]], [80, [[('CEDA_WR1', 0.983, 0.983, 0.983), ('CEDA_WR2', 0.983, 0.983, 0.983)], [('CEDA_WR1', 0.983, 0.983, 0.983), ('CEDA_WR2', 0.983, 0.983, 0.983)], [('CEDA_WR1', 0.983, 0.983, 0.983), ('CEDA_WR2', 0.983, 0.983, 0.983)], [('CEDA_WR1', 0.983, 0.983, 0.983), ('CEDA_WR2', 0.983, 0.983, 0.983)], [('CEDA_WR1', 0.983, 0.983, 0.983), ('CEDA_WR2', 0.983, 0.983, 0.983)], [('CEDA_WR1', 0.983, 0.983, 0.983), ('CEDA_WR2', 0.983, 0.983, 0.983)], [('CEDA_WR1', 0.983, 0.983, 0.983), ('CEDA_WR2', 0.983, 0.983, 0.983)], [('CEDA_WR1', 0.983, 0.983, 0.983), ('CEDA_WR2', 0.983, 0.983, 0.983)], [('CEDA_WR1', 0.983, 0.983, 0.983), ('CEDA_WR2', 0.983, 0.983, 0.983)], [('CEDA_WR1', 0.983, 0.983, 0.983), ('CEDA_WR2', 0.983, 0.983, 0.983)], [('CEDA_WR1', 0.983, 0.983, 0.983), ('CEDA_WR2', 0.983, 0.983, 0.983)], [('CEDA_WR1', 0.983, 0.983, 0.983), ('CEDA_WR2', 0.983, 0.983, 0.983)]]]]
XfmrStorageFull, XfmrLenOverFull, XfmrVoltStorageFull, XfmrVoltOutput=LoadFlowOverload.OverloadGathering(LoadStore, times1, VoltStore)
XfmrMostStore=LoadFlowOverload.WorstOverStoring(XfmrStorageFull)
XfmrExcel=LoadFlowOverload.ExcelFormatCreation(LoadStore,XfmrMostStore,XfmrStorageFull,XfmrVoltStorageFull)
XfmrVoltExcel=LoadFlowOverload.ExcelFormatCreation(VoltStore,XfmrMostStore,XfmrStorageFull,XfmrVoltStorageFull)
XfmrHist,XfmrGraph=LoadFlowOverload.HistogramFormat(XfmrLenOverFull)
FullVoltage=[]
FullVoltage.append(XfmrVoltOutput)
FullVoltage.append(XfmrVoltOutput)
FullVoltage.append(XfmrVoltOutput)
GraphStorage=[]
GraphStorage.append(XfmrGraph)
GraphStorage.append(XfmrGraph)
GraphStorage.append(XfmrGraph)


times2=range(58,72)
name = ('Transformer_Loading_Use_Case.xlsx')
LoadFlowOverload.ExportExcel(Penetration,times2, XfmrExcel,XfmrMostStore, name)

name = ('By_Phase_Transformer_Loading_Use_Case.xlsx')
LoadFlowOverload.ExportExcel(Penetration,times2, XfmrExcel,XfmrMostStore, name)

name = ('Transmission_Line_Loading_Use_Case.xlsx')
LoadFlowOverload.ExportExcel(Penetration,times2, XfmrExcel,XfmrMostStore, name)

name = ('Transformer_Voltage_Level_Use_Case.xlsx')
LoadFlowOverload.ExportExcel(Penetration,times2, XfmrVoltExcel,XfmrMostStore, name)

name = ('By_Phase_Transformer_Voltage_Level_Use_Case.xlsx')
LoadFlowOverload.ExportExcel(Penetration,times2, XfmrVoltExcel,XfmrMostStore, name)

name = ('Transmission_Line_Voltage_Level_Use_Case.xlsx')
LoadFlowOverload.ExportExcel(Penetration,times2, XfmrVoltExcel,XfmrMostStore, name)

val = -1
for Pen in Penetration:
    val = val + 1
    excelTitle = 'Transformer_Loading_Histograms_Use_Case_{penetration}.xlsx'.format(penetration=Pen)
    LoadFlowOverload.ExportHistogram(XfmrHist,excelTitle,val)
    excelTitleByPhase = 'By_Phase_Transformer_Loading_Histograms_Use_Case_{penetration}.xlsx'.format(penetration=Pen)
    LoadFlowOverload.ExportHistogram(XfmrHist, excelTitleByPhase, val)

LoadFlowOverload.VoltageOutput(FullVoltage, Penetration)

LoadFlowOverload.LoadingGraphOutput(GraphStorage, Penetration)
print 'done'
exit()
'''


from pandas.core.frame import DataFrame
#Exporting EVSE demand profiles from CSV to Python
#path is the computer address
path = "C:\\Users\\pwrlab07\\Downloads\\PEV-Profiles-L1.csv"

#Places CSV into the a list of columns with a special format, which skips household and vehicle titles
MDataL1 = pandas.read_csv(path, skiprows=2)
L1Store=[]
DeviceTimeStep=[]
for value in MDataL1['Time']:
    DeviceTimeStep.append(value)

#This converts the list above into a standard format, first index column number, second index time step
for val in MDataL1.columns:
    if val != 'Time':
        df=MDataL1[val]
        L1Store.append(df)


PVStore=[]

path = "C:\\Users\\pwrlab07\\Downloads\\44672PVDP.csv"
Data44672 = pandas.read_csv(path, skiprows=17)
name=Data44672.columns[10]
InterestedColumn= Data44672[Data44672.columns[10]]
AppendValue= ["44672",InterestedColumn]
PVStore.append(AppendValue)

path = "C:\\Users\\pwrlab07\\Downloads\\72113PVDP.csv"
Data72113 = pandas.read_csv(path, skiprows=17)

InterestedColumn= Data72113[Data72113.columns[10]]

AppendValue= ["72113",InterestedColumn]
PVStore.append(AppendValue)



path = "C:\\Users\\pwrlab07\\Downloads\\SystemPercentageChangesUse.csv"
SPCU = pandas.read_csv(path)
SPCUHold=[]

colplace=[1,2,3,4,5]


for place in colplace:
    colvalue= SPCU[SPCU.columns[place]]
    HoldSingle = []
    x=-1
    for value in colvalue:
        x=x+1
        value1=colvalue[x]
        #print colvalue
        #This is fine as long as the final datapoint isn't reached
        if x == len(colvalue)-1:
            value2=colvalue[x]
        else:
            value2=colvalue[x+1]

        First=value1
        Second=value1+(value2-value1)/6
        Third = value1 + ((value2 - value1)*2) / 6
        Fourth = value1 + ((value2 - value1)*3) / 6
        Fifth = value1 + ((value2 - value1)*4) / 6
        Sixth = value1 + ((value2 - value1)*5) / 6
        HoldSingle.append(First)
        HoldSingle.append(Second)
        HoldSingle.append(Third)
        HoldSingle.append(Fourth)
        HoldSingle.append(Fifth)
        HoldSingle.append(Sixth)
    SPCUHold.append(HoldSingle)




path = "C:\\Users\\pwrlab07\\Downloads\\PEV-Profiles-L2.csv"
MDataL2 = pandas.read_csv(path, skiprows=2)
L2Store=[]

for val in MDataL2.columns:
    if val != 'Time':
        df=MDataL2[val]

        L2Store.append(df)

IntProfileFull=[]
IntProfileAll=[]
checkvar=0
for address in int_demandprofiles:
    testval=pandas.ExcelFile(address)
    h=-1
    IntProfileAppend = [[], [], [], [], [], []]
    testint=-1
    for value in testval.sheet_names:

        testint=testint+1
        h=h+1

        string2="testval.parse({value2}, skiprows=1)".format(value2=h)
        exec("testval0"+"="+string2)
        #print'testin'
        #print testval0
        #print 'success?'


        for value in testval0:

            #print value
            #print testint
            if value != 'Time':


                if IntProfileAppend[testint] == '':
                    IntProfileAppend[testint] = (testval0[value])
                else:
                    IntProfileAppend[testint].append((testval0[value]))
    IntProfileFull.append(IntProfileAppend)
    #print 'wacko! {value}'.format(value=checkvar)
    #print address
    checkvar=checkvar+1



'''


path = "C:\\Users\\pwrlab07\\Downloads\\BatteryDP.csv"
values = pandas.read_csv(path, skiprows=1)

InterestedColumnGeneration= values[values.columns[1]]

AppendValue= ['BATTGEN',InterestedColumnGeneration]

BatteryDP[0]=AppendValue
InterestedColumnLoad= values[values.columns[2]]

AppendValue= ['OID_1269223',InterestedColumnLoad]
BatteryDP[1]=AppendValue

'''

#Chance of EVSE between Level 1 and Level 2, which can be changed
L1_chance = 90
L2_chance = 10

#Function asking if the User wants to use a different Level 1 and Level 2 composition
L1_chance, L2_chance= UserInput.ChargerDecisions(L1_chance, L2_chance)

#Asks user for number of devices to keep track of, Currently not in use along with related function
HowMany=UserInput.HowManyWorst()

#Assigns and creates storage for number of vehicles each customer and other records based off house power consumption
CustVehicleStorage, new_filename, spotlist_through,CarsFull=ModifySpotLoad.HouseholdVehicles(model_filename, L1_chance, L2_chance)


#Gets the number of invalid devices, signified by a QueryInfoDevice charactor of  ''
#This retrieves Asset BassNulls before adding intentional loads
BaseXfmrNull_Base, BaseXfmrByPhaseNull_Base, BaseLineNull_Base, XfmrNullName, XfmrByPhaseNullName, LineNullName = LoadFlowOverload.BaseNulls(new_filename)
print BaseXfmrNull_Base, BaseXfmrByPhaseNull_Base, BaseLineNull_Base


#Intentional Load asks the user if there are specific larger EV loads they're adding, and adds them
Current_Filename, LaterStorage, AppliedNames, UnAppliedNames, NamesAll= ModifySpotLoad.IntentionalLoad(new_filename, IntProfileFull)

BESRead = pandas.read_excel("C:\\Users\\pwrlab07\\Desktop\\BESHolder\\Medium\\ExamplePieces.xlsx")
BESReadStored=[]
skipvar=0
for val in BESRead.columns:
        if skipvar != 0:
            ColumnInfo=BESRead[val]
            #print ColumnInfo

            #print type(str(ColumnInfo[0]))
            #print str(ColumnInfo[0])
            #print type(ColumnInfo[1])

            BESReadStored.append(ColumnInfo)
        skipvar=skipvar+1


BatteryDP=[]



for value in BESReadStored:

    ws = xw.Book(r"C:\Users\pwrlab07\Documents\EVSEHourlyDataTemplate2.xlsx")
    ws2=ws.sheets('Scenerio1')
    #print value
    Charge, Discharge= ModifySpotLoad.BESProfPull(ws2, value[1],value[2],value[3],value[4])


    AppendValue=[value[0], Charge, Discharge]
    BatteryDP.append(AppendValue)
    print 'appendval'
    print AppendValue

New_Filename=ModifySpotLoad.BESCreation(BatteryDP,Current_Filename)
#ModifySpotLoad.BESCreation(BatteryDP, Current_Filename)
#function_study_analysis.save_study(Current_Filename+'BES')
LoadTimeXfmrSingle = []
LoadTimeByPhaseSingle = []
LoadTimeTransSingle = []

#Asks for the penetrations used for this study
Current_Filename, CurPen, MaxVal, IntValPen,CustVehicleStorage, Applied, Type,AppliedCars, NamesApplied,AppliedNames, UnAppliedNames =UserInput.CurrentPen(New_Filename, L1_chance, L2_chance,CustVehicleStorage, spotlist_through, LaterStorage, L1Store, L2Store,AppliedNames, UnAppliedNames)


#start of Add_EV Use Case
'''
Current_Filename = 'C:\\Users\\pwrlab07\\PycharmProjects\\PGEPython\\INPUT\\Cedar Hills AddEV Use Case.sxst'
function_study_analysis.save_study(Current_Filename)
function_study_analysis.open_study(Current_Filename)
CarsToApply=(CarsFull*int(CurPen)/100)
PenCarStore=[]
PenetrationCarStorage=(CurPen,AppliedCars, CarsToApply)
PenCarStore.append(PenetrationCarStorage)
Range=[15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100]
value=-1
for val in Range:

    value = value+1
    if value == 0:
        RealPen=float(IntValPen)/(100.0-float(CurPen))*100
        CarsToApply = (CarsFull * (int(val-CurPen) )/ 100)
    else:
        RealPen = float(IntValPen) / (100.0 - float(Range[value-1])) * 100
        CarsToApply = (CarsFull * (int(Range[value]) - int(Range[value-1] )) / 100)

    Current_Filename, CustCarStorage, SpotnumOrder, AppliedCars = ModifySpotLoad.Add_EV(Current_Filename, L1_chance, L2_chance,
                                                                                    RealPen, model_filename, val,
                                                                                    CustCarStorage, spotlist_through,
                                                                                    Type, LaterStorage, L1_size,
                                                                                    L2_size, L1Store, L2Store)
    function_study_analysis.save_study(Current_Filename)
    function_study_analysis.open_study(Current_Filename)
    PenetrationCarStorage = (val, AppliedCars, CarsToApply)
    PenCarStore.append(PenetrationCarStorage)
print 'Done'
for val in PenCarStore:
    print val
exit()
'''
#End of Add_EV Use Case

#Another access of BaseNulls, to pull invalid devices after intentional load addition
BaseXfmrNull, BaseXfmrByPhaseNull, BaseLineNull ,XfmrNullName, XfmrByPhaseNullName, LineNullName= LoadFlowOverload.BaseNulls(Current_Filename)

#Checks to make sure there were no changes from the base study, to the study with intentional loads added brought to the
#Current EV penetration
if BaseXfmrNull_Base != BaseXfmrNull or BaseXfmrByPhaseNull_Base != BaseXfmrByPhaseNull or BaseLineNull_Base != BaseLineNull:
    print 'Your intentional load additions have caused load flow errors'
    print 'I\'m not sure why this would happen, possibly due to too large of a load added'
    exit()

data_overload_precent=[]
IntentionalLoadingStorage=[]
IntappliedStorage=[]

start_main1=datetime.now()

#Ensures Penetration value are integers, then creates range of EV Penetration used
CurPen=int(CurPen)
MaxVal=int(MaxVal)
IntValPen=int(IntValPen)
Penetration = range((CurPen), (MaxVal + 1), IntValPen)

'''
#Probably not going to be using the value, especially due to what it's derived from
#This calulates the size of the variables storing loading values, length equal to the penetration range
sizeVar = len(Penetration)
'''

end_main1=datetime.now()
print('Main script part 1 Done in ' + str((end_main1 - start_main1).total_seconds()) + ' seconds')
#Opens study to grab device names
cympy.study.Open(Current_Filename)
start_devices=datetime.now()

#Grabs lists of all devices of the types specified, for grabbing their names, these values are used in each function
#due to modifications changing the order of .list_devices
xfmr = function_study_analysis.list_devices(cympy.enums.DeviceType.Transformer)
xfmr_byphase = function_study_analysis.list_devices(cympy.enums.DeviceType.TransformerByPhase)
xfmr_cable = function_study_analysis.list_devices(cympy.enums.DeviceType.OverheadByPhase)

xfmr_cable_true = function_study_analysis.list_devices(cympy.enums.DeviceType.Underground)
end_devices=datetime.now()
print('Three main list_devices PGE Done in ' + str((end_devices - start_devices).total_seconds()) + ' seconds')

xfmrStorage = []
xfmr_byphaseStorage = []
xfmr_cableStorage = []

cympy.study.Close(False)

OldPen=CurPen
IntVal=0
aplace=0

#StartTime dictates the range of timesteps to use, Maximum time step value 52559, Dec 31st 23:50
# 0=Jan 1st 2018, 00:00, 1=Jan 1st 2018, 00:10, 72=Jan 1st 2018, 12:00, 144=Jan 2nd 2018, 00:00
startTime=int(raw_input('When should this test begin?(1=10 minutes, 6=hour, 144=day):'))
MaxTime=int(raw_input('How many time steps would you like to use?(1=10 minutes, 6=hour, 144=day):'))

print 'checking time steps'
print MaxTime
print type(MaxTime)
DeviceTimeStepPart=DeviceTimeStep[startTime:MaxTime+startTime]

start_full_loop=datetime.now()

if Applied == 1:
    skip=1
LoadTimeXfmrPen = []
LoadTimeByPhasePen = []
LoadTimeTransPen = []
LoadTimeXfmrVoltPen = []
LoadTimeByPhaseVoltPen = []
LoadTimeTransVoltPen = []
LoadTimeByPhaseVoltExtraPen = []
LoadTimeIntByPhasePen = []
LoadTimeIntByPhaseVoltPen = []
LoadTimeByPhaseVoltDropPen = []
LoadTimeTransVoltDropPen = []
LoadTimeXfmrVoltOutPen=[]
HolderPreviousMag=0
whichloop=-1
RevertPreviousChange=[1,1,1,1,1]
#Main tool loop, loops through each penetration level, using LoadGrowth to connect penetration to device year
#Stocastically decides which customer load will recieve an EV
for Pen in Penetration:
    whichloop=whichloop+1
    LoadTimeXfmrMany = []
    LoadTimeByPhaseMany = []
    LoadTimeTransMany = []
    LoadTimeXfmrVoltMany = []
    LoadTimeByPhaseVoltMany = []
    LoadTimeByPhaseVoltExtraMany = []
    LoadTimeTransVoltMany = []
    LoadTimeTransVoltExtraMany = []
    LoadTimeIntByPhaseVoltMany = []
    LoadTimeByPhaseVoltDropMany = []
    LoadTimeTransVoltDropMany = []
    LoadTimeXfmrVoltOutMany=[]
    BrokenStudy=0
    start_loop=datetime.now()
    reset=1

    #Calculating the real penetration, 100-float(oldpen) = Current percentage of Cars with EV spots open
    #As an example, from 95% penetration to 100% penetration, all possible EV's would have to be added, which means
    #100% EV application for Add_EV
    #Another exmaple, 90% to 95%, adding 5% of EV's off of the 10 remaining % wouldn't be 5%, it would be 50%
    if Applied == 1:
        RealPen=float(IntValPen)/(100.0-float(OldPen))*100

    elif Applied == 2:
        RealPen=float(IntValPen)/(100.0-(float(OldPen)-float(CurPen)))*100

    #Storage for the filename in case of a Validity failure later on
    Old_Filename=Current_Filename

    #reset represents wether the system was determined to be valid or not, it starts as 0, and only become 1 after
    #a validity failure in LoadFlowOverload.loadflow
    while reset == 1:
        start_EV=datetime.now()

        #Add_EV takes the study, looks through it for avaliable areas for EV application, and places them
        if skip != 1:
            Current_Filename, CustVehicleStorage, SpotnumOrder, AppliedCars, NamesApplied,LaterStorage,AppliedNames, UnAppliedNames=ModifySpotLoad.Add_EV(Old_Filename,L1_chance,L2_chance,RealPen,model_filename,Pen,CustVehicleStorage,spotlist_through, Type, LaterStorage, L1Store, L2Store,AppliedNames, UnAppliedNames)
        else:
            ModifySpotLoad.open_study(Old_Filename)

        end_EV=datetime.now()
        #print('Add_EV Done in ' + str((end_EV - start_EV).total_seconds()) + ' seconds')
        start_OL=datetime.now()

        #ValidityCheck looks to see if recent additions have invalidated load flow
        reset=LoadFlowOverload.ValidityCheck(xfmr,xfmr_byphase,xfmr_cable, BaseXfmrNull, BaseXfmrByPhaseNull, BaseLineNull)
        '''
        data_overload_percent,reset,xfmrStorage, xfmr_byphaseStorage, xfmr_cableStorage, aplace, IntentionalLoadingStorage, IntappliedStorage, BadStorage = LoadFlowOverload.loadflow(data_overload_precent,Pen,xfmrStorage, xfmr_byphaseStorage,xfmr_cableStorage, aplace, BaseXfmrNull, BaseXfmrByPhaseNull, BaseLineNull,IntentionalName,IntentionalLoadingStorage, IntappliedStorage)
        '''
        end_OL=datetime.now()
        #print('Overloads Done in ' + str((end_OL - start_OL).total_seconds()) + ' seconds')

        #Prints some times signifying validity error
        if reset == 1:
            print 'Well I guess there were big enough problems for an EV re-application'
            BrokenStudy = BrokenStudy + 1


            #If the study fails too many times ends the code, finding it to be an unsolvable problem
            if BrokenStudy == 5:
                print 'There are significant problems, Load Flow can\'t be completed'
                print 'This may be due to intensity of load growth making the system incapable of supplying the loads'
                exit()


    #If the last study wasn't broken
    if reset != 1:
        cympy.study.Close(False)
        ModifySpotLoad.open_study(Current_Filename)
        num=0

        geewhiz=0
        for j in range(startTime, MaxTime+startTime):
            #print 'Pen'
            #print Pen
            #print 'j'
            #print j
            j_int=j-startTime

            start = datetime.now()
            #ReApply applied the current demand profile of EVSE added previously

            RevertPreviousChangeN = ModifySpotLoad.FeederDemand(spotlist_through, SPCUHold, j_int, RevertPreviousChange,Current_Filename)
            #print'revertpreviouschange'
            #print RevertPreviousChange
            #print RevertPreviousChangeN
            RevertPreviousChange = RevertPreviousChangeN

            NameReapply=ModifySpotLoad.ReApply(Current_Filename, CustVehicleStorage, j, L1Store, L2Store, AppliedNames, j_int,PVStore, BatteryDP,SPCUHold,whichloop)



            '''
            if j == startTime:
                print 'NamesApplied, then Reapply'
                print len(NamesApplied)
                print NamesApplied
                print len(NameReapply)
                print NameReapply
                UCVar=-1
                print 'Before Checking Names'
                for name in NameReapply:
                    UCVar=UCVar+1
                    if name != NamesApplied[UCVar]:
                        print 'Customer {one} and Customer {two} did not match'.format(one=name, two=NamesApplied[UCVar])
                print 'After Checking Names'
                exit()
            '''
            end = datetime.now()
            #print('ModifySpotload Done in ' + str((end - start).total_seconds()) + ' seconds')
            start = datetime.now()

            #TimeFlow looks into the overloads that are readable after a load flow simulation
            LoadTimeXfmrSingle,LoadTimeByPhaseSingle,LoadTimeTransSingle,LoadTimeXfmrVoltSingle,LoadTimeByPhaseVoltSingle,LoadTimeTransVoltSingle,num,LoadTimeIntByPhaseSingle ,LoadTimeIntByPhaseVoltSingle, LoadTimeByPhaseVoltExtraSingle,LoadTimeTransVoltExtraSingle,LoadTimeByPhaseVoltDropSingle,LoadTimeTransVoltDropSingle, LoadTimeXfmrVoltOutSingle =LoadFlowOverload.TimeFlow(num,xfmr,xfmr_byphase,xfmr_cable,AppliedNames,UnAppliedNames,Current_Filename,xfmr_cable_true)
            end = datetime.now()
            #print('TimeFlow Done in ' + str((end - start).total_seconds()) + ' seconds')

            #Gathers Loading and Voltage values for each time step
            if LoadTimeXfmrMany == []:

                LoadTimeXfmrMany = [LoadTimeXfmrSingle]
                LoadTimeByPhaseMany = [LoadTimeByPhaseSingle]
                LoadTimeTransMany = [LoadTimeTransSingle]
                LoadTimeXfmrVoltMany = [LoadTimeXfmrVoltSingle]
                LoadTimeByPhaseVoltMany = [LoadTimeByPhaseVoltSingle]
                LoadTimeByPhaseVoltExtraMany = [LoadTimeByPhaseVoltExtraSingle]
                LoadTimeTransVoltMany = [LoadTimeTransVoltSingle]
                LoadTimeTransVoltExtraMany = [LoadTimeTransVoltExtraSingle]
                LoadTimeIntByPhaseMany = [LoadTimeIntByPhaseSingle]
                LoadTimeIntByPhaseVoltMany = [LoadTimeIntByPhaseVoltSingle]
                LoadTimeByPhaseVoltDropMany=[LoadTimeByPhaseVoltDropSingle]
                #LoadTimeTransVoltDropMany=[LoadTimeTransVoltDropSingle]

                LoadTimeXfmrVoltOutMany = [LoadTimeXfmrVoltOutSingle]
            else:

                LoadTimeXfmrMany = LoadTimeXfmrMany+[LoadTimeXfmrSingle]
                LoadTimeByPhaseMany = LoadTimeByPhaseMany+[LoadTimeByPhaseSingle]
                LoadTimeTransMany = LoadTimeTransMany+[LoadTimeTransSingle]
                LoadTimeXfmrVoltMany = LoadTimeXfmrVoltMany+[LoadTimeXfmrVoltSingle]
                LoadTimeByPhaseVoltMany = LoadTimeByPhaseVoltMany+[LoadTimeByPhaseVoltSingle]
                LoadTimeByPhaseVoltExtraMany = LoadTimeByPhaseVoltExtraMany+[LoadTimeByPhaseVoltExtraSingle]
                LoadTimeTransVoltMany = LoadTimeTransVoltMany + [LoadTimeTransVoltSingle]
                LoadTimeTransVoltExtraMany = LoadTimeTransVoltExtraMany + [LoadTimeTransVoltExtraSingle]
                LoadTimeIntByPhaseMany = LoadTimeIntByPhaseMany + [LoadTimeIntByPhaseSingle]
                LoadTimeIntByPhaseVoltMany = LoadTimeIntByPhaseVoltMany + [LoadTimeIntByPhaseVoltSingle]
                LoadTimeByPhaseVoltDropMany=LoadTimeByPhaseVoltDropMany+[LoadTimeByPhaseVoltDropSingle]
                #LoadTimeTransVoltDropMany=LoadTimeTransVoltDropMany+[LoadTimeTransVoltDropSingle]

                LoadTimeXfmrVoltOutMany = LoadTimeXfmrVoltOutMany+[LoadTimeXfmrVoltOutSingle]

        #Each Penetration appends results to per penetration list
        if LoadTimeXfmrPen == []:
            LoadTimeXfmrPen = [[Pen]+[LoadTimeXfmrMany]]
            LoadTimeByPhasePen = [[Pen]+[LoadTimeByPhaseMany]]
            LoadTimeTransPen = [[Pen]+[LoadTimeTransMany]]
            LoadTimeXfmrVoltPen = [[Pen]+[LoadTimeXfmrVoltMany]]
            LoadTimeByPhaseVoltPen = [[Pen]+[LoadTimeByPhaseVoltMany]]
            LoadTimeByPhaseVoltExtraPen = [[Pen] + [LoadTimeByPhaseVoltExtraMany]]
            LoadTimeTransVoltPen = [[Pen]+[LoadTimeTransVoltMany]]
            LoadTimeTransVoltExtraPen = [[Pen] + [LoadTimeTransVoltExtraMany]]
            LoadTimeIntByPhasePen = [[Pen] + [LoadTimeIntByPhaseMany]]
            LoadTimeIntByPhaseVoltPen = [[Pen] + [LoadTimeIntByPhaseVoltMany]]
            LoadTimeByPhaseVoltDropPen = [[Pen]+[LoadTimeByPhaseVoltDropMany]]
            #LoadTimeTransVoltDropPen = [[Pen]+[LoadTimeTransVoltDropMany]]

            LoadTimeXfmrVoltOutPen = [[Pen]+[LoadTimeXfmrVoltOutMany]]
        else:
            LoadTimeXfmrPen = LoadTimeXfmrPen + [[Pen]+[LoadTimeXfmrMany]]
            LoadTimeByPhasePen = LoadTimeByPhasePen+ [[Pen]+[LoadTimeByPhaseMany]]
            LoadTimeTransPen = LoadTimeTransPen+ [[Pen]+[LoadTimeTransMany]]
            LoadTimeXfmrVoltPen = LoadTimeXfmrVoltPen + [[Pen]+[LoadTimeXfmrVoltMany]]
            LoadTimeByPhaseVoltPen = LoadTimeByPhaseVoltPen + [[Pen]+[LoadTimeByPhaseVoltMany]]
            LoadTimeByPhaseVoltExtraPen = LoadTimeByPhaseVoltExtraPen + [[Pen] + [LoadTimeByPhaseVoltExtraMany]]
            LoadTimeTransVoltPen = LoadTimeTransVoltPen + [[Pen]+[LoadTimeTransVoltMany]]
            LoadTimeTransVoltExtraPen = LoadTimeTransVoltExtraPen + [[Pen] + [LoadTimeTransVoltExtraMany]]
            LoadTimeIntByPhasePen = LoadTimeIntByPhasePen + [[Pen] + [LoadTimeIntByPhaseMany]]
            LoadTimeIntByPhaseVoltPen = LoadTimeIntByPhaseVoltPen + [[Pen] + [LoadTimeIntByPhaseVoltMany]]

            LoadTimeByPhaseVoltDropPen = LoadTimeByPhaseVoltDropPen+[[Pen]+[LoadTimeByPhaseVoltDropMany]]
            #LoadTimeTransVoltDropPen = LoadTimeTransVoltDropPen+[[Pen]+[LoadTimeTransVoltDropMany]]
            LoadTimeXfmrVoltOutPen = LoadTimeXfmrVoltOutPen+ [[Pen] + [LoadTimeXfmrVoltOutMany]]


    skip = 0
    OldPen=Pen


    end_loop=datetime.now()
    print('Single Loop Done in ' + str((end_loop - start_loop).total_seconds()) + ' seconds {Pen}'.format(Pen=Pen))
print 'complete without storage?'

print 'loading'
print LoadTimeXfmrPen
print '1'
print LoadTimeXfmrPen[0]
print '2'
print LoadTimeXfmrPen[0][0]
print '3'
print LoadTimeXfmrPen[0][1]
print '4'
print LoadTimeXfmrPen[0][1][0]
print '5'
print LoadTimeXfmrPen[0][1][1]



print LoadTimeByPhasePen[0]
print LoadTimeTransPen[0]

print 'voltage'
print
cympy.study.Close(False)
TimeRange=range(startTime,MaxTime+startTime)
Xfmrvalue,XfmrWorst,XfmrVoltvalue, ByPhasevalue,ByPhaseWorst, ByPhaseVoltvalue,Cablevalue,CableWorst ,CableVoltvalue, XfmrHist,ByPhaseHist,FullVoltage, GraphStorage,IntByPhasevalue,IntByPhaseWorst, IntByPhaseVoltvalue,IntByPhaseHist, VoltageTrendStore, LoadingTrendStore,XfmrExcelHM,XfmrVoltExcelHM,XfmrHistHM,ByPhaseExcelHM,ByPhaseVoltExcelHM,ByPhaseHistHM,IntByPhaseExcelHM,IntByPhaseVoltExcelHM,IntByPhaseHistHM,CableExcelHM,CableVoltExcelHM,CableHistHM,ByPhaseVoltDropvalue,CableVoltDropvalue, XfmrVoltOutExcel =LoadFlowOverload.Processing(LoadTimeXfmrPen, LoadTimeByPhasePen, LoadTimeTransPen, TimeRange,LoadTimeXfmrVoltPen, LoadTimeByPhaseVoltPen, LoadTimeTransVoltPen, LoadTimeIntByPhasePen,LoadTimeIntByPhaseVoltPen, NamesAll, HowMany,LoadTimeByPhaseVoltDropPen,LoadTimeTransVoltDropPen, LoadTimeXfmrVoltOutPen)
print 'ended loop, before sorting'


LoadFlowOverload.CSVOutputs(Penetration,Xfmrvalue,XfmrWorst, ByPhasevalue,ByPhaseWorst, Cablevalue,CableWorst, XfmrVoltvalue,ByPhaseVoltvalue,CableVoltvalue, XfmrHist,ByPhaseHist,FullVoltage,GraphStorage,IntByPhasevalue,IntByPhaseWorst, IntByPhaseVoltvalue,IntByPhaseHist, VoltageTrendStore, LoadingTrendStore, NamesAll, TimeRange,XfmrExcelHM,XfmrVoltExcelHM,XfmrHistHM,ByPhaseExcelHM,ByPhaseVoltExcelHM,ByPhaseHistHM,IntByPhaseExcelHM,IntByPhaseVoltExcelHM,IntByPhaseHistHM,CableExcelHM,CableVoltExcelHM,CableHistHM,DeviceTimeStepPart, ByPhaseVoltDropvalue,CableVoltDropvalue, XfmrVoltOutExcel)



exit()
'''
Xfmrvalue, ByPhasevalue, Cablevalue, LoadTimeXfmrPen, LoadTimeByPhasePen, LoadTimeTransPen, XfmrOver, ByPhaseOver, CableOver=LoadFlowOverload.SortingWorstTime(LoadTimeXfmrPen, LoadTimeByPhasePen, LoadTimeTransPen, TimeRange,LoadTimeXfmrVoltPen, LoadTimeByPhaseVoltPen, LoadTimeTransVoltPen)
print 'ended loop, before sorting'

LoadFlowOverload.CSVOutputsTime(LoadTimeXfmrPen, LoadTimeByPhasePen, LoadTimeTransPen,Xfmrvalue, ByPhasevalue, Cablevalue, MaxTime, Penetration, XfmrOver, ByPhaseOver, CableOver)
'''
#WorstEquipment looks into the device storage to find the worst number of devices you chose, based on loading values
HowMany=5
XfmrVals, ByPhaseVals, CableVals, XfmrNames, ByPhaseNames, CableName=LoadFlowOverload.WorstEquipment(xfmrStorage, xfmr_byphaseStorage, xfmr_cableStorage, HowMany, sizeVar)
print 'types of worst'
print XfmrVals
print type(XfmrVals)
print XfmrNames
print type(XfmrNames)

LoadFlowOverload.CSVOutputs(data_overload_percent, XfmrVals, ByPhaseVals, CableVals, XfmrNames, ByPhaseNames, CableName, Penetration, HowMany,IntentionalLoadingStorage, IntappliedStorage ) #,'List of intentional load names'
print 'Here are transmission lines that look like their implementation is incomplete'
print 'Their loading limit is default, 1A'
print BadStorage

print 'These are the Transformer\'s that don\'t complete load flow already in the base study'
print 'They, cannot complete load flow due to many possible issues, I\'d check phase connections and rating ID\'s'
print XfmrNullName

print 'These are the ByPhase Transformers, usually to residential customers, that fail loadflow'
print XfmrByPhaseNullName

print 'These are the transmission lines that have problems other then incomplete loading limits'
for val in LineNullName:
    Same = 1
    for val2 in BadStorage:
        if val2 == val:
            Same=0
    if Same == 1:
        print val

exit()


    #print xfmrStorage

    #print 'xfmr_byphaseStorage After'
    #print xfmr_byphaseStorage
    #if Pen > 10:
    #    exit()
    #print 'xfmr_cableStorage After'
    #print xfmr_cableStorage



end_full_loop=datetime.now()
print('Entire Loop Done in ' + str((end_full_loop - start_full_loop).total_seconds()) + ' seconds')
exit()
LoadFlowOverload.WorstEquipment(xfmrStorage,xfmr_byphaseStorage,xfmr_cableStorage)

exit()



exit()
array=LoadFlowOverload.ArrayCreation(Current_Filename,data_overload_percent,data_nulls, start_Real)
print array
end_Real = datetime.now()
timescript=end_Real-start_Real
print 'this script took {sec} seconds'.format(sec=timescript)
exit()




if __name__ == "__main__":
    start = datetime.now()
    #Open study and list out devices

    function_study_analysis.open_study(model_filename)


    #a = function_study_analysis.read_cutsheet(temp_cutsheet_store_path, r"X:\Cutsheets\Emergency Switching Sheets\2018 Emergency Cutsheets\Mulino BR1_E_1155.pdf")

    breakers = function_study_analysis.list_devices(cympy.enums.DeviceType.Breaker)
    #print("This is for breakers-------------------------------------------------------------------")
    #print("\n")
    #print(breakers)

    transformers = function_study_analysis.list_devices(cympy.enums.DeviceType.Transformer)

    '''
    spotload = function_study_analysis.list_devices(cympy.enums.DeviceType.SpotLoad)

    devices = spotload
    #devices = function_study_analysis.get_unbalanced_line_Cym(devices)
    #print 'This\'ll play if that doesn\'t error out'
    #print('################First################')
    #print(devices.iloc[1:4,2:4])
    devices = function_study_analysis.get_voltage_Cym(devices)
    #print('################First################')
    #print(devices.iloc[1:4, 4:7])
    devices = function_study_analysis.get_load_Cym(devices)
    print('################First################')
    print(devices.iloc[1:4, 7:10])
    print(devices.iloc[1:4, 10:14])
    #exit()
    #devices = function_study_analysis.get_unbalanced_line_Cym(devices)
    #print('################First################')
    #print(devices.iloc[1:4, 14:17])
    #devices = function_study_analysis.get_distance_Cym(devices)
    #print('################First################')
    #print(devices.iloc[1:4, 17:19])
    #dummy=pandas.ExcelWriter('C:\Users\pwrlab07\Documents\CYMEOutputTesting', engine='xlsxwriter')
    #devices.to_csv(dummy, "SpotLoad Values")
    #devices.to_csv('C:\Users\pwrlab07\PycharmProjects\PGEPython\Testing\CYMEOutputTesting', index=False, header=True)
    #print "Sent to CSV"

    #hmm=cympy.sim.LoadValue(1,2)
    #print(hmm)
    #print(type(hmm))
    #print("This is for spot loads------------------------------------------------------------------")
    #print("\n")
    #print(spotload)
    #print("\n")
    #print(spotload.iloc[:,1:4])
    #print("breaker values")
    #print("\n")
    #print(breakers.iloc[:,1:4])
    '''


    #Create tables that will store ALL loading data for later <-- ALL LOADINGS
    #print("table Creator")
    temp = function_study_analysis.create_tables(breakers, "Breaker")
    #print("temp------------------------------------------------")
    #print("\n")
    #print(temp)
    feeder_summer_table = temp["Summer"]
    feeder_winter_table = temp["Winter"]

    temp = function_study_analysis.create_tables(transformers, "Transformer")
    #print("temp------------------------------------------------")
    #print("\n")
    #print(temp)
    transformer_summer_table = temp["Summer"]
    transformer_winter_table = temp["Winter"]
    '''
    temp = function_study_analysis.create_tables(spotload, "SpotLoad")
    #print("SPOTLOAD------------------------------------------------")
    #print("\n")
    #print(spotload)
    #print("temp SPOTLOAD------------------------------------------------")
    #print("\n")
    #print(temp)
    #spotload_summer_table = temp["Summer"]
    #spotload_winter_table = temp["Winter"]
    #print("Here's Stuff")

    #print(spotload_summer_table)
    #exit()
    '''
    cympy.study.Close(False)

    #Create and format tables that will store MAXIMUM contingency loads <-- CONTINGENCY MAXIMUMS

    feeder_N0_winter = breakers.copy()
    feeder_N0_winter['winter_overload_Total'] = [0] * len(feeder_N0_winter)
    feeder_N0_summer = breakers.copy()
    feeder_N0_summer['summer_overload_Total'] = [0] * len(feeder_N0_summer)
    feeder_N1_feeder_winter = breakers.copy()
    feeder_N1_feeder_winter['winter_overload_Total'] = [0] * len(feeder_N1_feeder_winter)
    feeder_N1_feeder_summer = breakers.copy()
    feeder_N1_feeder_summer['summer_overload_Total'] = [0] * len(feeder_N1_feeder_summer)
    feeder_N1_xfmr_winter = breakers.copy()
    feeder_N1_xfmr_winter['winter_overload_Total'] = [0] * len(feeder_N1_xfmr_winter)
    feeder_N1_xfmr_summer = breakers.copy()
    feeder_N1_xfmr_summer['summer_overload_Total'] = [0] * len(feeder_N1_xfmr_summer)

    feeder_N1_feeder_winter['max_contingency'] = [0] * len(feeder_N1_feeder_winter)
    feeder_N1_feeder_summer['max_contingency'] = [0] * len(feeder_N1_feeder_summer)
    feeder_N1_xfmr_winter['max_contingency'] = [0] * len(feeder_N1_xfmr_winter)
    feeder_N1_xfmr_summer['max_contingency'] = [0] * len(feeder_N1_xfmr_summer)

    transformer_N0_winter = transformers.copy()
    transformer_N0_winter['winter_overload_Total'] = [0] * len(transformer_N0_winter)
    transformer_N0_summer = transformers.copy()
    transformer_N0_summer['summer_overload_Total'] = [0] * len(transformer_N0_summer)
    transformer_N1_feeder_winter = transformers.copy()
    transformer_N1_feeder_winter['winter_overload_Total'] = [0] * len(transformer_N1_feeder_winter)
    transformer_N1_feeder_summer = transformers.copy()
    transformer_N1_feeder_summer['summer_overload_Total'] = [0] * len(transformer_N1_feeder_summer)
    transformer_N1_xfmr_winter = transformers.copy()
    transformer_N1_xfmr_winter['winter_overload_Total'] = [0] * len(transformer_N1_xfmr_winter)
    transformer_N1_xfmr_summer = transformers.copy()
    transformer_N1_xfmr_summer['summer_overload_Total'] = [0] * len(transformer_N1_xfmr_summer)

    transformer_N1_feeder_winter['max_contingency'] = [0] * len(transformer_N1_feeder_winter)
    transformer_N1_feeder_summer['max_contingency'] = [0] * len(transformer_N1_feeder_summer)
    transformer_N1_xfmr_winter['max_contingency'] = [0] * len(transformer_N1_xfmr_winter)
    transformer_N1_xfmr_summer['max_contingency'] = [0] * len(transformer_N1_xfmr_summer)

    #Re-open study and simulate winter loads for N-0

    function_study_analysis.open_study(model_filename)

    temp = function_study_analysis.season_overload_analysis(loadings_simulation_year_winter, "Winter",
                                                            winter_loadings_filename,
                                                            winter_overload_report_filename)

    breaker_overload_winter = temp["Breaker"]
    xfmr_overload_winter = temp["Transformer"]

    #Create base winter values in loading tables

    feeder_winter_table = feeder_winter_table.assign(**{"N-0 KVA": ""})
    for index, row in breaker_overload_winter.iterrows():
        feeder_winter_table.loc[
            cympy.study.GetDevice(row["device_number"], cympy.enums.DeviceType.Breaker).EquipmentID][
            "N-0 KVA"] = int(function_study_analysis.max_current(row.device_number, cympy.enums.DeviceType.Breaker))
    transformer_winter_table = transformer_winter_table.assign(**{"N-0 KVA": ""})
    for index, row in transformers.iterrows():
        transformer_winter_table.loc[row["device_number"]][
            "N-0 KVA"] = int(
            float(cympy.study.QueryInfoDevice("KVATOT", row.device_number, cympy.enums.DeviceType.Transformer)))

    cympy.study.Close(False)

    # Re-open study and simulate summer loads for N-0

    function_study_analysis.open_study(model_filename)

    temp = function_study_analysis.season_overload_analysis(loadings_simulation_year_summer, "Summer",
                                                            summer_loadings_filename,
                                                            summer_overload_report_filename)
    breaker_overload_summer = temp["Breaker"]
    xfmr_overload_summer = temp["Transformer"]

    # Create base summer values in loading tables

    feeder_summer_table = feeder_summer_table.assign(**{"N-0 KVA": ""})
    for index, row in breaker_overload_summer.iterrows():
        feeder_summer_table.loc[
            cympy.study.GetDevice(row["device_number"], cympy.enums.DeviceType.Breaker).EquipmentID][
            "N-0 KVA"] = int(function_study_analysis.max_current(row.device_number, cympy.enums.DeviceType.Breaker))
    transformer_summer_table = transformer_summer_table.assign(**{"N-0 KVA": ""})
    for index, row in transformers.iterrows():
        transformer_summer_table.loc[row["device_number"]][
            "N-0 KVA"] = int(
            float(cympy.study.QueryInfoDevice("KVATOT", row.device_number, cympy.enums.DeviceType.Transformer)))

    cympy.study.Close(False)

    #Input data into contingency tables
    #Accept only greater values to end up with maximum in the end

    for device in breaker_overload_winter.itertuples():
        feeder_N0_winter.loc[device.Index, 'winter_overload_Total'] = max(float(
            breaker_overload_winter.loc[device.Index, 'winter_overload_Total']),
            float(feeder_N0_winter.loc[device.Index, 'winter_overload_Total']))
        feeder_N0_summer.loc[device.Index, 'summer_overload_Total'] = max(float(
            breaker_overload_summer.loc[device.Index, 'summer_overload_Total']), float
        (feeder_N0_summer.loc[device.Index, 'summer_overload_Total']))
    for device in xfmr_overload_winter.itertuples():
        transformer_N0_winter.loc[device.Index, 'winter_overload_Total'] = max(float(
            xfmr_overload_winter.loc[device.Index, 'winter_overload_Total']),
            float(transformer_N0_winter.loc[device.Index, 'winter_overload_Total']))
        transformer_N0_summer.loc[device.Index, 'summer_overload_Total'] = max(float(
            xfmr_overload_summer.loc[device.Index, 'summer_overload_Total']), float
        (transformer_N0_summer.loc[device.Index, 'summer_overload_Total']))

    #Iterate through cutsheets in cutsheets folder

    for filename in os.listdir(cutsheet_filepath):

        cutsheet_filename = cutsheet_filepath + filename
        keyword_found = False
        #Find cutsheets matching defined keywords
        for keyword in cutsheet_keywords:
            if keyword.upper() in cutsheet_filename.upper():
                keyword_found = True
                break
        if not keyword_found:
            continue

        # Re-open study and simulate winter loads for selected cutsheet

        function_study_analysis.open_study(model_filename)

        temp = function_study_analysis.season_overload_analysis(loadings_simulation_year_winter, "Winter",
                                                                winter_loadings_filename,
                                                                winter_overload_report_filename, temp_cutsheet_store_path,
                                                                cutsheet_filename, save_contingency_selfcontained, contingency_selfcontained_store_dir)
        breaker_overload_winter = temp["Breaker"]
        xfmr_overload_winter = temp["Transformer"]

        # Enter winter values into loading tables

        feeder_winter_table = feeder_winter_table.assign(**{filename[:-4] + " KVA": ""})
        for index, row in breaker_overload_winter.iterrows():
            feeder_winter_table.loc[
                cympy.study.GetDevice(row["device_number"], cympy.enums.DeviceType.Breaker).EquipmentID][
                filename[:-4] + " KVA"] = int(
                function_study_analysis.max_current(row.device_number, cympy.enums.DeviceType.Breaker))
        transformer_winter_table = transformer_winter_table.assign(**{filename[:-4] + " KVA": ""})
        for index, row in transformers.iterrows():
            transformer_winter_table.loc[row["device_number"]][
                filename[:-4] + " KVA"] = int(
                float(cympy.study.QueryInfoDevice("KVATOT", row.device_number,
                                                  cympy.enums.DeviceType.Transformer)))

        cympy.study.Close(False)

        # Re-open study and simulate summer loads for selected cutsheet

        function_study_analysis.open_study(model_filename)

        temp = function_study_analysis.season_overload_analysis(loadings_simulation_year_summer, "Summer",
                                                                summer_loadings_filename,
                                                                summer_overload_report_filename, temp_cutsheet_store_path,
                                                                cutsheet_filename, save_contingency_selfcontained, contingency_selfcontained_store_dir)

        breaker_overload_summer = temp["Breaker"]
        xfmr_overload_summer = temp["Transformer"]

        # Enter summer values into loading tables

        feeder_summer_table = feeder_summer_table.assign(**{filename[:-4]+ " KVA": ""})
        for index, row in breaker_overload_summer.iterrows():
            feeder_summer_table.loc[
                cympy.study.GetDevice(row["device_number"], cympy.enums.DeviceType.Breaker).EquipmentID][
                filename[:-4]+ " KVA"] = int(
                function_study_analysis.max_current(row.device_number, cympy.enums.DeviceType.Breaker))
        transformer_summer_table = transformer_summer_table.assign(**{filename[:-4]+ " KVA": ""})
        for index, row in transformers.iterrows():
            transformer_summer_table.loc[row["device_number"]][
                filename[:-4]+ " KVA"] = int(
                float(cympy.study.QueryInfoDevice("KVATOT", row.device_number,
                                                  cympy.enums.DeviceType.Transformer)))

        cympy.study.Close(False)

        # Input data into contingency tables
        # Accept only greater values to end up with maximum in the end

        if re.match("[-\w_ ]+(WR|BR|WK|WJ|BK)\d[-\w_.+ ]+", filename):
            for device in breaker_overload_winter.itertuples():
                if float(breaker_overload_winter.loc[device.Index, 'winter_overload_Total']) > float(
                        feeder_N1_xfmr_winter.loc[device.Index, 'winter_overload_Total']):
                    feeder_N1_xfmr_winter.loc[device.Index, 'winter_overload_Total'] = float(
                        breaker_overload_winter.loc[device.Index, 'winter_overload_Total'])
                    feeder_N1_xfmr_winter.loc[device.Index, 'max_contingency'] = filename[:-4]
                if float(breaker_overload_summer.loc[device.Index, 'summer_overload_Total']) > float(
                        feeder_N1_xfmr_summer.loc[device.Index, 'summer_overload_Total']):
                    feeder_N1_xfmr_summer.loc[device.Index, 'summer_overload_Total'] = float(
                        breaker_overload_summer.loc[device.Index, 'summer_overload_Total'])
                    feeder_N1_xfmr_summer.loc[device.Index, 'max_contingency'] = filename[:-4]
            for device in xfmr_overload_winter.itertuples():
                if float(xfmr_overload_winter.loc[device.Index, 'winter_overload_Total']) > float(
                        transformer_N1_xfmr_winter.loc[device.Index, 'winter_overload_Total']):
                    transformer_N1_xfmr_winter.loc[device.Index, 'winter_overload_Total'] = float(
                        xfmr_overload_winter.loc[device.Index, 'winter_overload_Total'])
                    transformer_N1_xfmr_winter.loc[device.Index, 'max_contingency'] = filename[:-4]
                if float(xfmr_overload_summer.loc[device.Index, 'summer_overload_Total']) > float(
                        transformer_N1_xfmr_summer.loc[device.Index, 'summer_overload_Total']):
                    transformer_N1_xfmr_summer.loc[device.Index, 'summer_overload_Total'] = float(
                        xfmr_overload_summer.loc[device.Index, 'summer_overload_Total'])
                    transformer_N1_xfmr_summer.loc[device.Index, 'max_contingency'] = filename[:-4]
        else:
            for device in breaker_overload_winter.itertuples():
                if float(breaker_overload_winter.loc[device.Index, 'winter_overload_Total']) > float(
                        feeder_N1_feeder_winter.loc[device.Index, 'winter_overload_Total']):
                    feeder_N1_feeder_winter.loc[device.Index, 'winter_overload_Total'] = float(
                        breaker_overload_winter.loc[device.Index, 'winter_overload_Total'])
                    feeder_N1_feeder_winter.loc[device.Index, 'max_contingency'] = filename[:-4]
                if float(breaker_overload_summer.loc[device.Index, 'summer_overload_Total']) > float(
                        feeder_N1_feeder_summer.loc[device.Index, 'summer_overload_Total']):
                    feeder_N1_feeder_summer.loc[device.Index, 'summer_overload_Total'] = float(
                        breaker_overload_summer.loc[device.Index, 'summer_overload_Total'])
                    feeder_N1_feeder_summer.loc[device.Index, 'max_contingency'] = filename[:-4]
            for device in xfmr_overload_winter.itertuples():
                if float(xfmr_overload_winter.loc[device.Index, 'winter_overload_Total']) > float(
                        transformer_N1_feeder_winter.loc[device.Index, 'winter_overload_Total']):
                    transformer_N1_feeder_winter.loc[device.Index, 'winter_overload_Total'] = float(
                        xfmr_overload_winter.loc[device.Index, 'winter_overload_Total'])
                    transformer_N1_feeder_winter.loc[device.Index, 'max_contingency'] = filename[:-4]
                if float(xfmr_overload_summer.loc[device.Index, 'summer_overload_Total']) > float(
                        transformer_N1_feeder_summer.loc[device.Index, 'summer_overload_Total']):
                    transformer_N1_feeder_summer.loc[device.Index, 'summer_overload_Total'] = float(
                        xfmr_overload_summer.loc[device.Index, 'summer_overload_Total'])
                    transformer_N1_feeder_summer.loc[device.Index, 'max_contingency'] = filename[:-4]

    #Filter results to only show breakers that contains "BREAKER_" (bogus breakers)

    feeder_N0_winter = feeder_N0_winter[feeder_N0_winter['device_number'].str.contains("BREAKER_")]
    feeder_N0_summer = feeder_N0_summer[feeder_N0_summer['device_number'].str.contains("BREAKER_")]
    feeder_N1_feeder_winter = feeder_N1_feeder_winter[feeder_N1_feeder_winter['device_number'].str.contains("BREAKER_")]
    feeder_N1_feeder_summer = feeder_N1_feeder_summer[feeder_N1_feeder_summer['device_number'].str.contains("BREAKER_")]
    feeder_N1_xfmr_winter = feeder_N1_xfmr_winter[feeder_N1_xfmr_winter['device_number'].str.contains("BREAKER_")]
    feeder_N1_xfmr_summer = feeder_N1_xfmr_summer[feeder_N1_xfmr_summer['device_number'].str.contains("BREAKER_")]
    transformer_N0_winter = transformer_N0_winter
    transformer_N0_summer = transformer_N0_summer
    transformer_N1_feeder_winter = transformer_N1_feeder_winter
    transformer_N1_feeder_summer = transformer_N1_feeder_summer
    transformer_N1_xfmr_winter = transformer_N1_xfmr_winter
    transformer_N1_xfmr_summer = transformer_N1_xfmr_summer

    #Export loading tables to excel spreadsheets

    function_study_analysis.write_overload_tables(feeder_winter_table,feeder_summer_table,transformer_winter_table,transformer_summer_table,loading_tables_filename)

    function_study_analysis.open_study(model_filename)

    breakers = function_study_analysis.list_devices(cympy.enums.DeviceType.Breaker)

    transformers = function_study_analysis.list_devices(cympy.enums.DeviceType.Transformer)

    #Create graphs based on maximum loading values

    function_study_analysis.plot_overload(feeder_N0_winter, feeder_N0_summer, "Breakers", "Feeder Loading (N-0)",
                                          [[67, "Black", "67% Seasonal Rating", .5],
                                           [100, "Red", "100% Seasonal Rating", 1]],
                                          feeder_normal_overload_plot_filename)
    function_study_analysis.plot_overload(feeder_N1_feeder_winter, feeder_N1_feeder_summer,
                                          "Breakers", "Worst Feeder Contingencies (N-1 Feeders)",
                                          [[67, "Black", "67% Seasonal Rating", .5],
                                           [100, "Red", "100% Seasonal Rating", 1]],
                                          feeder_feeder_overload_plot_filename)
    function_study_analysis.plot_overload(feeder_N1_xfmr_winter, feeder_N1_xfmr_summer,
                                          "Breakers", "Worst Feeder Contingencies (N-1 Transformers)",
                                          [[67, "Black", "67% Seasonal Rating", .5],
                                           [100, "Red", "100% Seasonal Rating", 1]],
                                          feeder_transformer_overload_plot_filename)
    function_study_analysis.plot_overload(transformer_N0_winter, transformer_N0_summer,
                                          "Transformers", "Transformer Loading (N-0)",
                                          [[80, "Black", "80% Seasonal LBNR", .5],
                                           [100, "Red", "100% Seasonal LBNR", 1]],
                                          transformer_normal_overload_plot_filename)
    function_study_analysis.plot_overload(transformer_N1_feeder_winter, transformer_N1_feeder_summer,
                                          "Transformers", "Worst Transformer Contingencies (N-1 Feeders)",
                                          [[80, "Black", "80% Seasonal LBNR", .5],
                                           [100, "Red", "100% Seasonal LBNR", 1]],
                                          transformer_feeder_overload_plot_filename)
    function_study_analysis.plot_overload(transformer_N1_xfmr_winter, transformer_N1_xfmr_summer,
                                          "Transformers", "Worst Transformer Contingencies (N-1 Transformers)",
                                          [[80, "Black", "80% Seasonal LBNR", .5],
                                           [100, "Red", "100% Seasonal LBNR", 1]],
                                          transformer_transformer_overload_plot_filename)

    for index, row in feeder_N1_feeder_summer.iterrows():
        print(row['device_number'] + " Maximum SUMMER Overload N-1 Feeder: " + str(
            row['summer_overload_Total']) + "% (" + str(row['max_contingency']) + ")")
    for index, row in feeder_N1_feeder_winter.iterrows():
        print(row['device_number'] + " Maximum WINTER Overload N-1 Feeder Contingency: " + str(
            row['winter_overload_Total']) + "% (" + str(row['max_contingency']) + ")")
    for index, row in feeder_N1_xfmr_summer.iterrows():
        print(row['device_number'] + " Maximum SUMMER Overload N-1 Transformer Contingency: " + str(
            row['summer_overload_Total']) + "% (" + str(row['max_contingency']) + ")")
    for index, row in feeder_N1_xfmr_winter.iterrows():
        print(row['device_number'] + " Maximum WINTER Overload N-1 Transformer Contingency: " + str(
            row['winter_overload_Total']) + "% (" + str(row['max_contingency']) + ")")
    for index, row in transformer_N1_feeder_summer.iterrows():
        print(row['device_number'] + " Maximum SUMMER Overload N-1 Feeder Contingency: " + str(
            row['summer_overload_Total']) + "% (" + str(row['max_contingency']) + ")")
    for index, row in transformer_N1_feeder_winter.iterrows():
        print(row['device_number'] + " Maximum WINTER Overload N-1 Feeder Contingency: " + str(
            row['winter_overload_Total']) + "% (" + str(row['max_contingency']) + ")")
    for index, row in transformer_N1_xfmr_summer.iterrows():
        print(row['device_number'] + " Maximum SUMMER Overload N-1 Transformer Contingency: " + str(
            row['summer_overload_Total']) + "% (" + str(row['max_contingency']) + ")")
    for index, row in transformer_N1_xfmr_winter.iterrows():
        print(row['device_number'] + " Maximum WINTER Overload N-1 Transformer Contingency: " + str(
            row['winter_overload_Total']) + "% (" + str(row['max_contingency']) + ")")

    print("##################################################")
    print("#               GENERATING REPORTS               #")
    print("##################################################")

    # *********************************************
    # Calculating Loading through each device in the system and uploading to DataFrame
    # *********************************************
    if loading_report_needed == True:
        function_study_analysis.gen_load_analysis_report(breakers, loading_report_filename)
    else:
        print(' ')
        print('Skipping Loadings Report...')

    # *********************************************
    # Calculating Unbalance Phases in the system and uploading to DataFrame
    # *********************************************
    if unbalanced_voltage_report_needed == True:
        function_study_analysis.gen_unbalanced_voltage_report(breakers, unbalanced_voltage_report_filename)
    else:
        print(' ')
        print('Skipping Voltage Report...')

    # *********************************************
    # Calculating Short Circuit in the system and uploading to DataFrame
    # *********************************************
    if short_circuit_report_needed == True:
        function_study_analysis.gen_short_circuit_report(breakers, short_circuit_report_filename)
    else:
        print(' ')
        print('Skipping Short Circuit Report...')

    # *********************************************
    # Saving the actual Self-Contained File in the directory
    # *********************************************
    if saving_selfcontained_needed == True:
        function_study_analysis.save_study()
    else:
        print(' ')
        print('Skipping Saving the Self-Contained File...')
    # *********************************************
    # Creating and Saving CYME Report in directory
    # *********************************************
    if cyme_report_needed == True:
        function_study_analysis.gen_cyme_report(cyme_report_filename)
    else:
        print(' ')
        print('Skipping Creating CYME Report...')

    # *********************************************
    # Completion Statement
    # *********************************************
    print(' ')
    print('******ANALYSIS COMPLETED******')
    end = datetime.now()
    print('Entire STUDY done in ' + str((end - start).total_seconds()) + ' seconds')
    # *********************************************
    # ************ T H E   E N D ******************
    # *********************************************
