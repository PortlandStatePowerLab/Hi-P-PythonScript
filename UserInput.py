#Module for Grabbing Spot Loads and saving study with it
#I wish I didn't have to do this, but it seems that once you've added a customer load the study's values are invalidated
# and attempting to print them via cympy.study.QueryInfoDevice brings back a blank value

from __future__ import division
import pandas
import csv
import math

import function_study_analysis
import lookup
from datetime import datetime

import pickle
import numpy as np
import time
from pytz import timezone
import sys

import difflib


CYMPY_LOCATION = r"C:\Program Files (x86)\CYME\CYME 7.1"
sys.path.insert(1, CYMPY_LOCATION)
import cympy
import cympy.rm
import cympy.db
import cympy.study
import cympy.enums

#import function_study_analysis
from definitions import *
import random
import ModifySpotLoad

def truncate(n, decimals=0):
    '''
    truncate is for rounding values
    '''
    multiplier = 10 ** decimals
    return int(n * multiplier) / multiplier

def CurrentPen(filename,L1_chance,L2_chance,CustCarStorage, spotlist_through, LaterStorage, L1Store, L2Store,AppliedNames, UnAppliedNames):
    '''
    CurPen Asks for the current penetration of the system
    If there is no way of accuretly determining if a spotload customer is a EV customer, need to make adjustment
    Will use the Current penetration to look against residential loads
    i.e. is there are 5000 residental loads in the study, and the CurPen is at 10%, there would be
    5000*(CurPen+1) loads, so 10% penetration extra would add roughly 550 EV's instead of 500
    '''

    start = datetime.now()

    #(int) Asks user for the current study penetration
    CurPen = int(raw_input("What is the current Systems EV Penetration?:"))

    #(int) Asks user if the penetration given is already applied to the study (EVSE are already represented)
    #or if it should be applied
    Applied=int(raw_input('Should this EV penetration be applied to the system(1) or is it already represented(2):'))


    #Need to change type assignment to before IntentionalLoads
    choice = raw_input('Do you use a specific customer type to exclude load growth?(Yes/No):')
    if choice == 'Yes':
        Type=str(raw_input('Please type in one of the excluded customer types (Case Sensitive):'))
    else:
        Type = ''

    #If the user puts a value above 100%, set it too 100%
    if int(CurPen) > 100:
        CurPen=100

    #(int) Asks user for maximum EV penetration they want to study til
    MaxVal = int(raw_input("What is the maximum EV penetration to study for?(Capped at 100%):"))

    #If the user sets the maximum value of penetration above 100%, sets it too 100%
    if int(MaxVal) > 100:
        MaxVal=100
    if MaxVal < CurPen:
        print 'Please don\'t give a current penetration larger then the maximum'
        exit()

    #(int) Asks user for the penetration step size
    IntVal= int(raw_input("What interval do you want to use? (int):"))

    #Add_EV for CurPen, creates a distribution system with the correct EV penetration
    if Applied == 1:
        new_filename,CustCarStorage, placeholder,AppliedCars,Names,LaterStorage,AppliedNames, UnAppliedNames = ModifySpotLoad.Add_EV(filename, L1_chance, L2_chance, CurPen, filename, CurPen, CustCarStorage, spotlist_through, Type, LaterStorage, L1Store, L2Store,AppliedNames, UnAppliedNames)

    elif Applied == 2:
        #If the EVSE penetration is known, this sets up certain output variables while applying no new loads
        new_filename,CustCarStorage, placeholder,AppliedCars,Names,LaterStorage,AppliedNames, UnAppliedNames=ModifySpotLoad.Add_EV(filename, L1_chance, L2_chance, 0, filename, 0, CustCarStorage,spotlist_through, Type, LaterStorage, L1Store, L2Store,AppliedNames, UnAppliedNames)

    else:
        print 'please input 1 or 2 when asking about Penetration application'
        exit()

    cympy.study.Save(new_filename)

    end=datetime.now()
    print('CurrentPen, including one call to Add_EV Done in ' + str((end - start).total_seconds()) + ' seconds')
    return new_filename, CurPen, MaxVal, IntVal, CustCarStorage, Applied, Type, AppliedCars, Names,AppliedNames, UnAppliedNames

def AskingTime():
    '''
    AskingTime asks the user for the user if they have a specific loadshape for placing accurate EV loads
    Asks the user the time of day looking to be studied, to index a utilization value modifying EV load values
    '''
    loadshape_loadings_filename = "C:\\Users\\pwrlab07\\PycharmProjects\\PGEPython\\INPUT\\LoadShapeExcel.xlsx"

    #(string)  Asks user if they have a loadshape to add
    choice = raw_input("Will you add your own summer and winter EV Loadshapes? (Yes and No Case Sensitive):")
    if choice == 'Yes':

        #(string) Asks user for location of stored load shapes
        loadshape_loadings_filename = raw_input("Where are these loadshapes stored?:")
    LoadShape = pandas.read_excel(loadshape_loadings_filename, index_col=0)


    #(int) Asks for the military time of the study, indexing it too the load shape in 10 minute intervols
    hoursandminutes=int(raw_input("What the time of the study (Military time):"))

    #Ends code if users enters an invalid time
    if hoursandminutes < 0 or hoursandminutes > 2400:
        print 'Please stay within a 24 hour day'
        exit()
    hours = truncate(hoursandminutes, -2) / 100 * 6
    minutes=hoursandminutes % 100
    remainder = minutes % 10
    minutes = truncate(minutes, -1) / 10

    if remainder <= 5:
        extra = 0
    else:
        extra = 1
    print hours
    print minutes
    print extra


    #adjustment for rounding down in the case of values that exceed index values
    if hoursandminutes > 2354:
        TimeStep = hours + minutes + extra
    else:
        TimeStep = hours + minutes + extra + 1
    print TimeStep

    print LoadShape.loc[TimeStep, "L1ChargersSummer"]
    exit()
    return TimeStep, LoadShape

def NodeCheck(spotload2,XFMRByPhase,Cables,CheckingAgainst):
    From=0
    To=0
    for spot1 in spotload2:
        #print spot1.DeviceNumber
        #print cympy.study.QueryInfoDevice("FromNodeId", spot1.DeviceNumber, 14)
        if cympy.study.QueryInfoDevice("FromNodeId", spot1.DeviceNumber, 14) == CheckingAgainst:
            #print 'From this node'
            #print spot1.DeviceNumber
            From=spot1.DeviceNumber
    for spot2 in XFMRByPhase:
        if cympy.study.QueryInfoDevice("FromNodeId", spot2.DeviceNumber, 33) == CheckingAgainst:
            #print 'From this node'
            #print spot2.DeviceNumber
            From = spot2.DeviceNumber
        if cympy.study.QueryInfoDevice("ToNodeId", spot2.DeviceNumber, 33) == CheckingAgainst:
            #print 'To this node'
            #print spot2.DeviceNumber
            To=spot2.DeviceNumber
    for spot3 in Cables:
        if cympy.study.QueryInfoDevice("FromNodeId", spot3.DeviceNumber, 10) == CheckingAgainst:
            #print 'From this node'
            #print spot3.DeviceNumber
            From = spot3.DeviceNumber
        if cympy.study.QueryInfoDevice("ToNodeId", spot3.DeviceNumber, 10) == CheckingAgainst:
            #print 'To this node'
            #print spot3.DeviceNumber
            To = spot3.DeviceNumber
    return From,To

def NodeCheckSpot(DeviceNumber):
    '''
    Specific function for Xfmr branch adding, outputs attached node
    '''
    #print cympy.study.QueryInfoDevice("FromNodeId", DeviceNumber, 14)
    From=cympy.study.QueryInfoDevice("FromNodeId", DeviceNumber, 14)
    return From

def NodeCheckXFMR(DeviceNumber):
    '''
    Specific function for Xfmr branch adding, outputs attached node
    '''
    #print cympy.study.QueryInfoDevice("FromNodeId", DeviceNumber, 33)
    From=cympy.study.QueryInfoDevice("FromNodeId", DeviceNumber, 33)
    return From

def NodeCheckSection(DeviceNumber):
    '''
    Specific function for Xfmr branch adding, outputs attached node
    '''
    #print cympy.study.QueryInfoDevice("FromNodeId", DeviceNumber, 10)
    From=cympy.study.QueryInfoDevice("FromNodeId", DeviceNumber, 10)
    return From

def HowManyWorst():
    '''
    HowManyWorst is a function for asking the user the number of each device they want exported to CSV's
    '''
    HowMany=raw_input('How many of the worst devices in each catagory do you want to output information for?:')
    return int(HowMany)

def ChargerDecisions(L1_chance, L2_chance):
    '''
    ChargerDecisions exits solely to ask the user to provide their own Level 1 to Level 2 EVSE composition
    '''
    Question = raw_input('Do you wish to use the Default L1 and L2 Compositions, or your Own (D/O):')
    if Question == 'O':
        L1_chance = raw_input('What is the percentage of L1 chargers to overall L1 and L2 chargers:')
        L2_chance = raw_input('What is the percentage of L2 chargers to overall L1 and L2 chargers:')

    return L1_chance, L2_chance