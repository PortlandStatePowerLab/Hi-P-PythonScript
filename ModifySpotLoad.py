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
import UserInput
import xlwings as xw

CYMPY_LOCATION = r"C:\Program Files (x86)\CYME\CYME"
sys.path.insert(1, CYMPY_LOCATION)
import cympy
import cympy.rm
import cympy.db
import cympy.study
import cympy.enums
import cympy.utils
cympy.app.ActivateRefresh(False)

#import function_study_analysis
from definitions import *
import random

def open_study(study_file_path):
    # Open specified study and run load flow
    start = datetime.now()

    print('Querying Self-Contained File...')
    cympy.study.Open(study_file_path)
    load_flow = cympy.sim.LoadFlow()
    load_flow.Run()
    end = datetime.now()

def save_study(file_path):
    start = datetime.now()
    #print(' ')
    print('Saving Study...')
    cympy.study.Save(file_path)
    end = datetime.now()
    #print('Done in ' + str((end - start).total_seconds()) + ' seconds')

def list_devices(device_type, verbose=True):
    print(' ')
    print('List of SELECTED Equipments in Database:')
    devices = cympy.study.ListDevices(device_type)
    devices = pandas.DataFrame(devices, columns=['device'])
    devices['device_type_id'] = devices['device'].apply(lambda x: x.DeviceType)
    devices['device_number'] = devices['device'].apply(lambda x: x.DeviceNumber)
    devices['device_type'] = devices['device_type_id'].apply(lambda x: lookup.type_table[x])

    if verbose:
        unique_type = devices['device_type'].unique().tolist()
        for device_type in unique_type:
            print('There are ' + str(devices[devices.device_type == device_type].count()[0]) +
                  ' ' + device_type)
    return devices

def PhaseCheck(phrase,spotload):
    '''
    PhaseCheck loops to see which phase the device is through error exceptions

    There is a better way to do it using more cympy functions, but doesn't lead to a noticable better speed
    '''

    try:
        phasetype = spotload.GetValue(phrase + "CustomerLoadValues.Get(AB).LoadValue.KW")
        isAB = 1
    except cympy.err.CymError:
        isAB = 0

    try:
        phasetype = spotload.GetValue(phrase + "CustomerLoadValues.Get(AC).LoadValue.KW")
        isAC = 1
    except cympy.err.CymError:
        isAC = 0

    try:
        phasetype = spotload.GetValue(phrase + "CustomerLoadValues.Get(BC).LoadValue.KW")
        isBC = 1
    except cympy.err.CymError:
        isBC = 0

    try:
        phasetype = spotload.GetValue(phrase + "CustomerLoadValues.Get(ABC).LoadValue.KW")
        isABC = 1
    except cympy.err.CymError:
        isABC = 0

    try:
        phasetype = spotload.GetValue(phrase + "CustomerLoadValues.Get(A).LoadValue.KW")
        isA = 1
    except cympy.err.CymError:
        isA = 0

    try:
        phasetype = spotload.GetValue(phrase + "CustomerLoadValues.Get(B).LoadValue.KW")
        isB = 1
    except cympy.err.CymError:
        isB = 0

    try:
        phasetype = spotload.GetValue(phrase + "CustomerLoadValues.Get(C).LoadValue.KW")
        isC = 1
    except cympy.err.CymError:
        isC = 0

    if isA == 1:
        SecondPhrase = "CustomerLoadValues.Get(A)."
        kWPhase="KWA"

    elif isB == 1:
        SecondPhrase = "CustomerLoadValues.Get(B)."
        kWPhase = "KWB"

    elif isC == 1:
        SecondPhrase = "CustomerLoadValues.Get(C)."
        kWPhase = "KWC"

    elif isAB == 1:
        SecondPhrase = "CustomerLoadValues.Get(AB)."
        kWPhase = "KWA"

    elif isAC == 1:
        SecondPhrase = "CustomerLoadValues.Get(AC)."
        kWPhase= "KWA"

    elif isBC == 1:
        SecondPhrase = "CustomerLoadValues.Get(BC)."
        kWPhase= "KWB"

    elif isABC == 1:
        SecondPhrase = "CustomerLoadValues.Get(ABC)."
        kWPhase= "KWA"

    else:
        print("Device accessed has invalid Phase")
        SecondPhrase = "CustomerLoadValues.Get(A)."
        kWPhase="KWA"

    return SecondPhrase,kWPhase

def CheckValues(spotnum):
    print 'kWA = {num}'.format(num=cympy.study.QueryInfoDevice("KWA", spotnum, int(14)))
    print 'kWB = {num}'.format(num=cympy.study.QueryInfoDevice("KWB", spotnum, int(14)))
    print 'kWC = {num}'.format(num=cympy.study.QueryInfoDevice("KWC", spotnum, int(14)))
    print 'kW Total = {num}'.format(num=cympy.study.QueryInfoDevice("KWTOT", spotnum, int(14)))
    print 'kVArA = {num}'.format(num=cympy.study.QueryInfoDevice("KVARA", spotnum, int(14)))
    print 'kVArB = {num}'.format(num=cympy.study.QueryInfoDevice("KVARB", spotnum, int(14)))
    print 'kVArC = {num}'.format(num=cympy.study.QueryInfoDevice("KVARC", spotnum, int(14)))
    print 'kVAr Total = {num}'.format(num=cympy.study.QueryInfoDevice("KVARTOT", spotnum, int(14)))

def IntentionalLoad(model_filename, IntProfile):
    '''
    This function asks the user if there are Hi-P EVSE they want to add into the study, then calls a function for
    creating the branch of equipment required for large EV loads
    '''
    NameStorage=[]

    NamesAll = []
    UnAppliedNames=[]
    AppliedNames=[]
    IntValue =0

    LaterStorage=[]
    start=datetime.now()
    open_study(model_filename)

    #Python User Input

    '''
    choice = raw_input("Will you be adding large EVSE? (Yes/No):")
    while choice == 'Yes':
        demand_add=0
        amount_add=0
        #(String)   Case Sensitive Spotload index number
        name = raw_input("Enter Spotload Number/Name:")

        #(int)      Size of EVSE
        demand = raw_input("Enter size of EVSE in kW:")
        demand=float(demand)

        #(int)      Number of same kW EVSE at node to add
        amount = raw_input("Enter number of identically sized EVSE at location:")
        amount=int(amount)
        demandAdjust=demand*amount

        #diversityfactor is from PGE transformer ratings
        diversityfactor = DiversityAdjustment(amount)

        #AdjustedDemand represents total realistic EVSE demand
        AdjustedDemand=demandAdjust*diversityfactor

        #(String)   Phase of EVSE
        phase = raw_input("Enter Phase of EVSE (A,B,C,AB,BC,AC,ABC):")

        #(int)   Phase of EVSE
        volt = int(raw_input("Please enter the secondary voltage of the transformer 208, 240, 480:"))

        #(string)   If more EVSE of a different size is going to be added
        another=raw_input('Will you be adding any aditional EVSE to this location? (Yes/No):')

        while another == 'Yes':
            #Collects information on the addition EVSE
            demand_add = raw_input("Enter size of EVSE in kW:")
            demand_add = float(demand_add)

            amount_add = raw_input("Enter number of identically sized EVSE at location:")
            amount_add = int(amount_add)
            demandAdjust_add = demand_add * amount_add

            #Finding the diversityfactor for the current class of EVSE, then adds it to the tot EVSE demand
            diversityfactor = DiversityAdjustment(amount_add)
            AdjustedDemand_add=demandAdjust_add *diversityfactor
            AdjustedDemand=AdjustedDemand+AdjustedDemand_add

            another = raw_input('Will you be adding any aditional EVSE to this location? (Yes/No):')

        if another == 'No':
            #Where intentional EVSE are applied to the distribution study or stored for later application
            now=raw_input('Is this load going to be added right away, or wait until a certain year?(N/W):')

            if now == 'N':
                # IntLoadBranchCreation takes the information given by the user and creates a seperate
                # branch of transformer and spotload to hold the intentional loads
                model_filename=IntLoadBranchCreation(name, AdjustedDemand, phase, volt, IntProfile[IntValue])

                #Adds intentional EVSE name to a list of applied intentional EVSE
                value=[name, IntProfile[IntValue]]
                AppliedNames.append(value)

                #List of all EVSE names applied or stored
                NamesAll.append(value)
            else:
                #Asks for the year at which the EVSE will be applied
                year=int(raw_input('What year will this EVSE be added onto the system?:'))

                #Stores the information needed to use IntLoadBranchCreation on a future system
                store= [year, name, AdjustedDemand, phase, volt, 0, IntProfile[IntValue]]
                LaterStorage.append(store)
                value = [name, IntProfile[IntValue]]
                #Adds intentional EVSE name to a list of unapplied intentional EVSE
                UnAppliedNames.append(value)
                NamesAll.append(value)
            IntValue=IntValue+1
        #If yes then asks user for more intentional load information
        choice=raw_input("Will you be adding additional loads at a different spotload? (Yes/No):")
    '''

    #1
    model_filename = IntLoadBranchCreation('OID_1268955', 900, 'ABC', 480, IntProfile[0])


    # Adds intentional EVSE name to a list of applied intentional EVSE
    value = ['OID_1268955', IntProfile[0]]
    AppliedNames.append(value)

    # List of all EVSE names applied or stored
    NamesAll.append(value)
    #2
    model_filename = IntLoadBranchCreation('OID_1279102', 900, 'ABC', 480, IntProfile[1])

    # Adds intentional EVSE name to a list of applied intentional EVSE
    value = ['OID_1279102', IntProfile[1]]
    AppliedNames.append(value)

    # List of all EVSE names applied or stored
    NamesAll.append(value)
    #3
    model_filename = IntLoadBranchCreation('OID_1268945', 600, 'ABC', 480, IntProfile[2])

    # Adds intentional EVSE name to a list of applied intentional EVSE
    value = ['OID_1268945', IntProfile[2]]
    AppliedNames.append(value)


    # List of all EVSE names applied or stored
    NamesAll.append(value)
    #4
    model_filename = IntLoadBranchCreation('OID_1269093', 150, 'ABC', 480, IntProfile[3])


    # Adds intentional EVSE name to a list of applied intentional EVSE
    value = ['OID_1269093', IntProfile[3]]
    AppliedNames.append(value)

    # List of all EVSE names applied or stored
    NamesAll.append(value)
    #5
    model_filename = IntLoadBranchCreation('OID_1269253', 600, 'ABC', 480, IntProfile[4])

    # Adds intentional EVSE name to a list of applied intentional EVSE
    value = ['OID_1269253', IntProfile[4]]
    AppliedNames.append(value)

    # List of all EVSE names applied or stored
    NamesAll.append(value)
    #6
    model_filename = IntLoadBranchCreation('OID_1269251', 900, 'ABC', 480, IntProfile[5])

    # Adds intentional EVSE name to a list of applied intentional EVSE
    value = ['OID_1269251', IntProfile[5]]
    AppliedNames.append(value)

    # List of all EVSE names applied or stored
    NamesAll.append(value)
    #7
    model_filename = IntLoadBranchCreation('OID_1268926', 150, 'ABC', 480, IntProfile[6])

    # Adds intentional EVSE name to a list of applied intentional EVSE
    value = ['OID_1268926', IntProfile[6]]
    AppliedNames.append(value)

    # List of all EVSE names applied or stored
    NamesAll.append(value)
    '''
    LaterStorage=[]
    AppliedNames=[]
    UnappliedNames=[]
    NamesAll=[]
    '''
    #Creates a new filename, for checking CYME study
    new_filename_template = model_filename.split('.')
    model_filename_changed = new_filename_template[0] + '_Record.' + new_filename_template[1]
    save_study(model_filename_changed)
    cympy.study.Close(False)
    end=datetime.now()

    print('IntentionalLoad Done in ' + str((end - start).total_seconds()) + ' seconds')
    return model_filename_changed,  LaterStorage, AppliedNames, UnAppliedNames, NamesAll

def IntLoadBranchCreation(Spotload_USER_INPUT, adjustedDemand, phase, volt,DemandProfile):
    '''
    if randomnumber == 1:
        print 'start of int branch section'
        model_filename = 'C:\\Users\\pwrlab07\\PycharmProjects\\PGEPython\\INPUT\\Cedar Hills IntBranchCheck.sxst'
        function_study_analysis.save_study(model_filename)
        exit()
    '''
    #This function takes the information
    if phase == 'A' or phase == 'B' or phase == 'C':
        TrueDemand = adjustedDemand
    elif phase == 'AB' or phase == 'AC' or phase == 'BC':
        TrueDemand = adjustedDemand/2
    else:
        TrueDemand=adjustedDemand/3
    spotload = cympy.study.ListDevices(14)
    XFMRByPhase = cympy.study.ListDevices(33)
    Cables = cympy.study.ListDevices(10)

    #print 'Branch Function'
    #print adjustedDemand
    #print TrueDemand


    #Spotload_USER_INPUT = '1632838'

    sizelist=[10, 15.0, 25.0, 37.5, 50, 75.0, 100, 150, 166.7, 250, 333.3, 500, 666.7, 833.3]
    for val in sizelist:
        if val >= TrueDemand:
            XfmrStartPhrase='{num}_KVA'.format(num=val)
            break

    #print 'what?'
    if volt == 208:
        XfmrEndPhrase='_1P_120/208V'
    elif volt == 240:
        XfmrEndPhrase = '_1P_120/240V'
    elif volt == 480:
        XfmrEndPhrase = '_1P_277/480V'
    else:
        print 'Invalid secondary voltage on load'

    XfmrIDString=XfmrStartPhrase+XfmrEndPhrase

    for abc in range(len(spotload)):
        if spotload[abc].DeviceNumber == Spotload_USER_INPUT:
            #print abc
            spotindex = abc


    #For testing I used Spotload 1632838, which was index of 1 for all devices
    #print spotload[spotindex].SectionID
    CheckingSec = spotload[spotindex].SectionID
    NetworkStr = spotload[spotindex].NetworkID
    load_flow = cympy.sim.LoadFlow()
    load_flow.Run()

    From1 = UserInput.NodeCheckSpot(spotload[spotindex].DeviceNumber)
    #print 'From Spotload Section'
    #print From1
    From2, To2 = UserInput.NodeCheck(spotload, XFMRByPhase, Cables, From1)

    #print 'From Getting XFMR Section'
    #print From2
    #print 'To Getting XFMR Section'
    #print To2
    From3 = UserInput.NodeCheckXFMR(To2)
    #print'From gathering XFMR Device'
    #print From3
    From4, To4 = UserInput.NodeCheck(spotload, XFMRByPhase, Cables, From3)
    #print 'From Getting Cable Section'
    #print From4
    #print 'To Getting Cable Section'
    #print To4
    From5 = UserInput.NodeCheckSection(To4)
    #print'From cable, should be final node'
    #print From5



    XFMRDevice = cympy.study.GetDevice(To2, 33)

    XFMR_IDA = ''
    XFMR_IDB = ''
    XFMR_IDC = ''
    XFMR_ConnectStatus = XFMRDevice.GetValue('ConnectionStatus')
    CableSection = cympy.study.GetDevice(To4, 10)
    Cable_ID = CableSection.GetValue('CableID')
    Cable_length = CableSection.GetValue('Length')

    # Cable Section CableID, Length
    # XFMR section PhaseTransformerID1,2,3, ConnectionStatus

    AnotherStep = cympy.study.GetNode(From5)
    #print type(AnotherStep)
    #print AnotherStep.ID
    #print AnotherStep.X
    #print AnotherStep.Y

    to_node = cympy.study.Node()
    to_node.ID = AnotherStep.ID + '-2'
    to_node.X = AnotherStep.X + 10
    to_node.Y = AnotherStep.Y + 10
    #print to_node.ID
    #print to_node.X
    #print to_node.Y
    checking = cympy.study.NetworkIterator(From3)
    checking.Next()
    Checkingphase = checking.GetSourcePhase()
    CheckingSection = checking.GetSection()
    # '7711876.041_586887.84'
    #print Checkingphase
    #print CheckingSection


    # placeholdername='A:50 23982|B:25 72834'

    XFMR_IDA,XFMR_IDB, XFMR_IDC = XfmrID(XFMR_IDA,XFMR_IDB, XFMR_IDC, Checkingphase, XfmrIDString)


    cympy.study.AddSection(CheckingSec + '-2', NetworkStr, To4 + '-2', cympy.enums.DeviceType.Underground,AnotherStep.ID, to_node)

    NewCable = cympy.study.GetDevice(To4 + '-2', 10)

    NewCable.SetValue(Cable_ID, 'CableID')
    NewCable.SetValue(Cable_length, 'Length')



    to_node2 = cympy.study.Node()
    to_node2.ID = to_node.ID + '-3'

    to_node2.X = to_node.X + 10
    to_node2.Y = to_node.Y + 10

    cympy.study.AddSection(CheckingSec + '-3', NetworkStr, Spotload_USER_INPUT + '-3', cympy.enums.DeviceType.TransformerByPhase, to_node.ID,
                           to_node2)
    model_filename_Tests = 'C:\\Users\\pwrlab07\\PycharmProjects\\PGEPython\\INPUT\\Ceder_Hills_CheckingAdd.sxst'

    #print To4 + '-3'
    #print 'values'
    #print CheckingSec
    #print To2
    #print To4
    NewXFMR = cympy.study.GetDevice(Spotload_USER_INPUT + '-3', 33)
    NewXFMR.SetValue(XFMR_ConnectStatus, 'ConnectionStatus')
    #print XFMR_IDA
    #print XFMR_IDB
    #print XFMR_IDC
    if XFMR_IDA != '':
        NewXFMR.SetValue(XFMR_IDA, 'PhaseTransformerID1')
    if XFMR_IDB != '':
        NewXFMR.SetValue(XFMR_IDB, 'PhaseTransformerID2')
    if XFMR_IDC != '':
        NewXFMR.SetValue(XFMR_IDC, 'PhaseTransformerID3')

    #print XFMR_IDC

    #print 'Where does the cable come in?'
    #print 'CheckingSec'
    #print CheckingSec
    #print 'To2'
    #print To2
    #print 'To4'
    #print To4
    load_flow.Run()
    to_node3 = cympy.study.Node()
    to_node3.ID = to_node2.ID + '-3'
    to_node3.X = to_node2.X + 10
    to_node3.Y = to_node2.Y + 10

    cympy.study.AddSection(CheckingSec + '-4', NetworkStr, To4 + '-4', cympy.enums.DeviceType.Underground, to_node2.ID,to_node3)

    cympy.study.AddDevice(Spotload_USER_INPUT + '-2', 14, CheckingSec + '-4')
    print 'information'
    print To4 + '-4'
    print CheckingSec + '-4'
    print Spotload_USER_INPUT + '-2'
    #print Spotload_USER_INPUT+'-2'
    #print CheckingSec+'-4'
    NewLoad= cympy.study.GetLoad(Spotload_USER_INPUT + '-2', 14)

    NewLoad.AddCustomerLoad('Anything')
    NewDevice = cympy.study.GetDevice(Spotload_USER_INPUT + '-2', 14)

    NewDevice.SetValue('Fixed', 'CustomerLoads.Get({value}).CustomerType'.format(value=Spotload_USER_INPUT + '-2'))
    #print NewLoad.ListCustomers()

    LoadA="CustomerLoads.Get({num}).CustomerLoadModels.Get(1).CustomerLoadValues.Get(A).LoadValue.KW".format(num=Spotload_USER_INPUT + '-2')
    #print LoadA
    #print 'whaa'
    #print DemandProfile[0][0][0]
    #print 'lll'
    #print DemandProfile[0][0][1]
    #print 'yyy'
    #print DemandProfile[0][0][0]
    LoadB="CustomerLoads.Get({num}).CustomerLoadModels.Get(1).CustomerLoadValues.Get(B).LoadValue.KW".format(num=Spotload_USER_INPUT + '-2')
    LoadC="CustomerLoads.Get({num}).CustomerLoadModels.Get(1).CustomerLoadValues.Get(C).LoadValue.KW".format(num=Spotload_USER_INPUT + '-2')
    NewDevice.SetValue(float(DemandProfile[0][0][0]), LoadA)
    NewDevice.SetValue(float(DemandProfile[0][1][0]), LoadB)
    NewDevice.SetValue(float(DemandProfile[0][2][0]), LoadC)


    #model_filename_Tests = 'C:\\Users\\pwrlab07\\PycharmProjects\\PGEPython\\INPUT\\Ceder_Hills_CheckingAdd.sxst'
    model_filename_Tests = 'C:\\Users\\pwrlab07\\PycharmProjects\\PGEPython\\INPUT\\Swan_Island_base.sxst'
    XfmrName=From2+'-3'

    function_study_analysis.save_study(model_filename_Tests)

    return model_filename_Tests

def XfmrID(XFMR_IDA,XFMR_IDB, XFMR_IDC, Checkingphase, XfmrIDPhrase):
    if Checkingphase == 1:
        XFMR_IDC = XfmrIDPhrase
    elif Checkingphase == 2:
        XFMR_IDB = XfmrIDPhrase
    elif Checkingphase == 3:
        XFMR_IDB = XfmrIDPhrase
        XFMR_IDC = XfmrIDPhrase
    elif Checkingphase == 4:
        XFMR_IDA = XfmrIDPhrase
    elif Checkingphase == 5:
        XFMR_IDA = XfmrIDPhrase
        XFMR_IDC = XfmrIDPhrase
    elif Checkingphase == 6:
        XFMR_IDA = XfmrIDPhrase
        XFMR_IDB = XfmrIDPhrase
    elif Checkingphase == 7:
        XFMR_IDA = XfmrIDPhrase
        XFMR_IDB = XfmrIDPhrase
        XFMR_IDC = XfmrIDPhrase
    else:
        print 'There is no distinct phase?'

    return XFMR_IDA, XFMR_IDB, XFMR_IDC

def DiversityAdjustment(trueamount):
    #PGE standards diversity factor modifier for transformer rating
    if trueamount >=0 and trueamount <= 4:
        diversityfactor=1
    elif trueamount >=5 and trueamount <= 8:
        diversityfactor = 0.9
    elif trueamount >=9 and trueamount <= 14:
        diversityfactor = 0.8
    elif trueamount >=15 and trueamount <= 30:
        diversityfactor = 0.7
    elif trueamount >=31 and trueamount <= 40:
        diversityfactor = 0.6
    else:
        diversityfactor = 0.5
    return diversityfactor

def Add_EV(model_filename,L1,L2,Penetration,through_filename, PEN, CustCarStorage,spotload, Type, LaterStorage, L1Store, L2Store, AppliedNames, UnAppliedNames):
    #Add_EV is responsible for getting together all thr phrases and values related to changing relevent Spotload
    #Customers
    '''
    Currently this only adds a single EV load onto each household, more work could be put into use catigorizing the
    houses as different sizes by EV load, and adding the possibility of more EV's on a single customer load
    '''
    open_study(model_filename)

    #Calls PenetrationVsYears to apply load growth
    LaterStorage, AppliedNames, UnAppliedNames=PenetrationVsYears(PEN, Type, LaterStorage, AppliedNames, UnAppliedNames)
    #print Penetration
    print len(spotload)
    print Penetration
    place=0
    order = -1
    CustOrder=-1
    again=1
    Change=0
    #print 'CustCar Before'
    #print CustCarStorage
    CarsApplied=0



    #arbitrary sized storage variables, will work unless there are more then 3 times as many residental customers then
    #there are total spotloads
    LoadValueMatrix = [[]]*len(spotload)*3
    u=0
    NamesApplied=[]
    #Sets LoadValueMa
    for val in LoadValueMatrix:
        LoadValueMatrix[u]=0.0
        u=u+1
    PhraseMaterix = [[]]*len(spotload)*3
    CurrentSpotNum = [[]]*len(spotload)*3
    Placeholder = [[]] * len(spotload) * 3
    CustNumholder = [[]] * len(spotload) * 3

    #While for looping through entire spotload list
    while place < len(spotload):
        addedalready = 0
        #print 'the place is {val}'.format(val=place)

        spotnum=spotload['device_number'][place]
        CustLoad = cympy.study.GetLoad(spotnum, 14)
        CustList = CustLoad.ListCustomers()
        #print 'first loop'
        #print CustList
        spot_load_device = cympy.study.GetDevice(spotnum, cympy.enums.DeviceType.SpotLoad)
        if Change == 1:
            order=order+1
            Change = 0
        #print 'SpotLoad name'
        #print spotnum
        OriValue=0

        #Loops through each of the customers inside the spotload
        for j in range(0, len(CustList)):
            CustOrder = CustOrder + 1
            #print 'order and custnum, and custcarstorage'
            #print CustOrder
            #print CustList[j]
            #print CustCarStorage[CustOrder][0][0]
            #if CustOrder <30:
            #    print 'CustOrder'
            #    print CustOrder

            ApplyValue=0
            #Check to make sure customer isn't an EV only placement customer
            if CustList[j] != spotnum:
                customer_load_prop = "CustomerLoads.Get({value}).".format(value=CustList[j])
                CustType = spot_load_device.GetValue(customer_load_prop + "CustomerType")

                #again = number of EV cars possible
                value=0
                if CustType == "Residential":
                    again = CustCarStorage[CustOrder][1][0]
                    realplace=spotnum
                    PlaceInCust=-1
                    for val in CustCarStorage[CustOrder][3]:
                        PlaceInCust=PlaceInCust+1

                        #Pen is a random value from 0 to 100, checking too see if EV's are added or not
                        Pen=random.uniform(0, 100)
                        if val != 0 and CustCarStorage[CustOrder][4][PlaceInCust] == 1:
                            OriValue = OriValue + L1Store[CustCarStorage[CustOrder][2][PlaceInCust]][0]
                        if val != 0 and CustCarStorage[CustOrder][4][PlaceInCust] == 2:
                            OriValue = OriValue + L2Store[CustCarStorage[CustOrder][2][PlaceInCust]][0]
                        #if the random Pen is larger then the % of added EV's this time, then add the EV load
                        if float(Pen) <= float(Penetration) and val == 0:
                            CarsApplied=CarsApplied+1
                            ApplyValue=ApplyValue+1


                            FirstPhrase = "CustomerLoads.Get({num}).CustomerLoadModels.Get(1).".format(num=realplace)
                            SecondPhrase, kWPhase = PhaseCheck(FirstPhrase, spot_load_device)

                            #Checks too see if val is between 0 and the % ratio of L1 to L2
                            if CustCarStorage[CustOrder][4][PlaceInCust]==1:

                                OriValue =OriValue+L1Store[CustCarStorage[CustOrder][2][PlaceInCust]][0]/1000

                                CustCarStorage[CustOrder][3][PlaceInCust]=1

                                LoadValueMatrix[order] = OriValue

                                CurrentSpotNum[order] = spotnum
                                PhraseMaterix[order] = FirstPhrase + SecondPhrase + "LoadValue.KW"
                                Placeholder[order]=place
                                CustNumholder[order]=CustList[j]
                                Change=1


                                #Each time an EV is added, remove it from CustCarStorage
                                CustCarStorage[CustOrder][1][1] = CustCarStorage[CustOrder][1][1] - 1
                                value=value+1


                            #Checks too see if the random val is larger then L1's %, and less then or equal to the
                            #combined L1 and L2 percentages
                            elif CustCarStorage[CustOrder][4][PlaceInCust]==2:

                                #print OriValue

                                OriValue = OriValue + L2Store[CustCarStorage[CustOrder][2][PlaceInCust]][0]/1000
                                CustCarStorage[CustOrder][3][PlaceInCust] = 2

                                LoadValueMatrix[order] = OriValue
                                #print 'Where Current Spotnum is placed'
                                #print order
                                #print spotnum
                                CurrentSpotNum[order] = spotnum
                                PhraseMaterix[order] = FirstPhrase + SecondPhrase + "LoadValue.KW"
                                Placeholder[order] = place
                                CustNumholder[order] = CustList[j]
                                Change=1


                                #print 'huh'
                                #print CustCarStorage[CustOrder][1]
                                CustCarStorage[CustOrder][1][1] = CustCarStorage[CustOrder][1][1] - 1
                                #print 'huh pt. 2'
                                #print CustCarStorage[CustOrder][1]
                                #exit()
                                value=value+1
            if ApplyValue != 0:
                NamesApplied.append(CustList[j])

        place=place+1


    #print 'CustCar After'
    #print CustCarStorage

    '''    
    for i in range(4000):
        if LoadValueMatrix[i] > 7.0:
            print PhraseMaterix[i]
            print LoadValueMatrix[i]
            print CurrentSpotNum[i]
    '''
    #ChangeLoad takes the collected customer load manipulation phrases and applies them to the EV load
    model_filename_EV = ChangeLoad(LoadValueMatrix, PhraseMaterix, order, CurrentSpotNum, through_filename,PEN, Type)

    NamesApplied.sort(key=takeFirst, reverse=True)

    return model_filename_EV, CustCarStorage, CurrentSpotNum, CarsApplied, NamesApplied, LaterStorage, AppliedNames, UnAppliedNames

def ChangeLoad(val,phrase,order,spotnum,model_filename,ActualPen, Type):

    #ChangeLoad takes the phrases and values found in Add_EV and applied them to their loads
    UseType='Fixed'
    if Type != '':
        UseType == Type

    val_total=0
    CarsApplied=0
    #Loops through each of the spotload's accessed
    for i in range(0,order):
        spot_load_device = cympy.study.GetDevice(spotnum[i], 14)

        NextVal=float(spot_load_device.GetValue(phrase[i]))+val[i]

        spot_load_device.SetValue(NextVal, phrase[i])
        spot_load_device.SetValue(UseType,'CustomerLoads.Get({value}).CustomerType'.format(value=spotnum[i]))

        val_total=val_total+val[i]

    ActualPen=int(ActualPen)




    filename_template = model_filename.split('.')

    filename_changed = filename_template[0] + '_Peneration_{Pen}.'.format(Pen=ActualPen)+ filename_template[1]

    save_study(filename_changed)

    print 'There were {num} Residental EV Loads added for a total of {kW} kW\'s of load'.format(num=order,kW=val_total)

    return filename_changed

def FeederDemand(spotload, SPCUHold, time, RevertPreviousChange,Current_Filename):
    print 'FeederDemand Started'
    save_study(Current_Filename + '22')
    load_flow = cympy.sim.LoadFlow()
    load_flow.Run()
    place=0
    order = -1
    CustOrder=-1
    again=1
    Change=0
    RevertPreviousChangeNew=[1,1,1,1,1]
    HolderFull=[]
    bbb=0
    while place < len(spotload):

        bbb=bbb+1
        addedalready = 0

        # print 'the place is {val}'.format(val=place)

        spotnum = spotload['device_number'][place]
        NetworkIDStep=spotload['NetworkID'][place]
        place=place+1
        if NetworkIDStep == "SWAN ISLAND-DOLPHIN":
            NetworkID = 0
        elif NetworkIDStep == "SWAN ISLAND-FREIGHTLINER":
            NetworkID = 1
        elif NetworkIDStep == "SWAN ISLAND-SHIPYARD":
            NetworkID = 2
        elif NetworkIDStep == "SWAN ISLAND-BASIN":
            NetworkID = 3
        elif NetworkIDStep == "SWAN ISLAND-GOING":
            NetworkID = 4

        CustLoad = cympy.study.GetLoad(spotnum, 14)
        CustList = CustLoad.ListCustomers()
        spot_load_device = cympy.study.GetDevice(spotnum, cympy.enums.DeviceType.SpotLoad)
        if Change == 1:
            order = order + 1
            Change = 0
        # print 'SpotLoad name'
        # print spotnum
        OriValue = 0

        # Loops through each of the customers inside the spotload
        for j in range(0, len(CustList)):
            CustOrder = CustOrder + 1
            # Check to make sure customer isn't an EV only placement customer
            if CustList[j] != spotnum:
                customer_load_prop = "CustomerLoads.Get({value}).".format(value=CustList[j])
                CustType = spot_load_device.GetValue(customer_load_prop + "CustomerType")
                if CustType != 'Fixed':
                    # again = number of EV cars possible
                    value = 0
                    realplace = spotnum

                    LoadA = "CustomerLoads.Get({num}).CustomerLoadModels.Get(1).CustomerLoadValues.Get(A).LoadValue.KW".format(num=CustList[j])
                    LoadB = "CustomerLoads.Get({num}).CustomerLoadModels.Get(1).CustomerLoadValues.Get(B).LoadValue.KW".format(num=CustList[j])
                    LoadC = "CustomerLoads.Get({num}).CustomerLoadModels.Get(1).CustomerLoadValues.Get(C).LoadValue.KW".format(num=CustList[j])

                    V1Val=0
                    V2Val=0
                    V3Val=0
                    try:
                        ValueA=float(spot_load_device.GetValue(LoadA))
                    except cympy.err.CymError:
                        ValueA=0.0

                    try:
                        ValueB=float(spot_load_device.GetValue(LoadB))
                    except cympy.err.CymError:
                        ValueB=0.0
                    try:
                        ValueC=float(spot_load_device.GetValue(LoadC))
                    except cympy.err.CymError:
                        ValueC=0.0

                    DummyValue=float(SPCUHold[NetworkID][time])

                    if ValueA > 0.0:
                        TrueValueA=ValueA *float(RevertPreviousChange[NetworkID])
                        V1Val = TrueValueA * DummyValue
                        RevertPreviousChangeNew[NetworkID] = 1 / DummyValue
                        if int(V1Val * RevertPreviousChangeNew[NetworkID]) != int(TrueValueA):
                            print 'huhA'
                            print TrueValueA
                            print V1Val
                            print RevertPreviousChangeNew[NetworkID]
                            print DummyValue
                        spot_load_device.SetValue(V1Val, LoadA)
                    if ValueB > 0.0:
                        TrueValueB=ValueB *float(RevertPreviousChange[NetworkID])
                        V2Val = TrueValueB * DummyValue
                        RevertPreviousChangeNew[NetworkID]=1/DummyValue
                        if int(V2Val * RevertPreviousChangeNew[NetworkID]) != int(TrueValueB):
                            print 'huhB'
                            print TrueValueB
                            print V2Val
                            print RevertPreviousChangeNew[NetworkID]
                            print DummyValue
                        spot_load_device.SetValue(V2Val, LoadB)
                    if ValueC > 0.0:
                        TrueValueC=ValueC *float(RevertPreviousChange[NetworkID])
                        V3Val = TrueValueC * DummyValue
                        RevertPreviousChangeNew[NetworkID]=1/DummyValue
                        if int(V3Val * RevertPreviousChangeNew[NetworkID]) != int(TrueValueC):
                            print 'huhC'
                            print TrueValueC
                            print V3Val
                            print RevertPreviousChangeNew[NetworkID]
                            print DummyValue
                        spot_load_device.SetValue(V3Val, LoadC)


    save_study(Current_Filename+'33')
    return RevertPreviousChangeNew

def HouseholdVehicles(model_filename, L1_chance, L2_chance):
    '''
    HouseholdCars is designed to assign a certain value related to household load, representing multiple cars for multi
    -family households, currently an not arbitraty value
    '''

    path = "C:\\Users\\pwrlab07\\Downloads\\CarsFromLoad.csv"
    df = pandas.read_csv(path)
    OneLoadMember = df['ONE 1']
    TwoLoadMember = df['TWO 1']
    ThreeLoadMember = df['THREE 1']
    FourLoadMember = df['FOUR 1']
    OneMemberCar = df['ONE 2']
    TwoMemberCar = df['TWO 2']
    ThreeMemberCar = df['THREE 2']
    FourMemberCar = df['FOUR 2']


    start2=datetime.now()
    cympy.study.Open(model_filename)


    spotload_pre = function_study_analysis.list_devices(14)

    CustStorage = []
    CustValStorage = []
    OutputStorage=[]
    NameStorage=[]

    #Loops through spotload numbers, each loop name is equal to one of the spotload device numbers
    for name in spotload_pre['device_number']:
        CustLoad = cympy.study.GetLoad(name, 14)
        CustList = CustLoad.ListCustomers()
        NewCustAdded=0

        #Loops through each customer index on the specific spotload of name
        for j in range(0, len(CustList)):
            spot_load_device = cympy.study.GetDevice(name, cympy.enums.DeviceType.SpotLoad)
            customer_load_prop = "CustomerLoads.Get({value}).".format(value=CustList[j])
            CustType = spot_load_device.GetValue(customer_load_prop + "CustomerType")

            #Looks to see if the customer being accessed is a residental type, which would mean an applicable EV house
            #Adds a seperate load for storing EV's
            if NewCustAdded ==0:

                #AddCustomerLoad is a broken cympy function, the customer number should be the string input, but is
                #instead the spotload ID
                CustLoad.AddCustomerLoad("blah")
                NewCustAdded = 1

    spotload_pre = function_study_analysis.list_devices(14)

    for name in spotload_pre['device_number']:

        CustLoad = cympy.study.GetLoad(name, 14)
        CustList = CustLoad.ListCustomers()


        for j in range(0, len(CustList)):
            spot_load_device = cympy.study.GetDevice(name, cympy.enums.DeviceType.SpotLoad)
            customer_load_prop = "CustomerLoads.Get({value}).".format(value=CustList[j])
            CustType = spot_load_device.GetValue(customer_load_prop + "CustomerType")

            FirstPhrase = "CustomerLoads.Get({num}).CustomerLoadModels.Get(1).".format(num=CustList[j])

            #Gathering the phrase for calling on customer loads
            SecondPhrase, kWPhase = PhaseCheck(FirstPhrase, spot_load_device)


            inter_step = [CustList[j]]

            if CustType == "Residential":
                inter_step2 = [float(spot_load_device.GetValue(FirstPhrase + SecondPhrase + "LoadValue.KW"))]

            else:
                inter_step2=[0.0]

            #Each loop appends the found values to the storage variables
            CustStorage.append(inter_step)
            CustValStorage.append(inter_step2)
            NameStorage.append(name)


    OneLoadMember = df['ONE 1']
    TwoLoadMember = df['TWO 1']
    ThreeLoadMember = df['THREE 1']
    FourLoadMember = df['FOUR 1']
    OneMemberCar = df['ONE 2']
    TwoMemberCar = df['TWO 2']
    ThreeMemberCar = df['THREE 2']
    FourMemberCar = df['FOUR 2']
    CarAll=0
    i=0
    ChanceStorage=[]
    for value in CustValStorage:
        value = float(value[0])

        if value >= 0.0:

            if value < 0.1:
                value = 0
            else:
                value = (UserInput.truncate(value, 1)*10)-1

            value=int(value)
            Pen=random.uniform(0, 100)

            if value <= 74:
                if Pen > 0 and Pen <= OneLoadMember[value]:
                    Members=1

                elif Pen > OneLoadMember[value] and Pen <= (OneLoadMember[value]+TwoLoadMember[value]):
                    Members = 2

                elif Pen > (OneLoadMember[value] + TwoLoadMember[value]) and Pen <= (OneLoadMember[value] + TwoLoadMember[value]+ ThreeLoadMember[value]):
                    Members = 3

                elif Pen > (OneLoadMember[value] + TwoLoadMember[value]+ ThreeLoadMember[value]):
                    Members = 4
            Modify=0
            if value > 74:
                Pen=random.uniform(0, 100)
                if Pen < 15:
                    Members=3
                else:
                    Members=4
                value = 74
                Modify=1
            Pen2 = random.uniform(0, 100)
            Cars=0
            if Members == 1:

                if Pen2 > 0 and Pen2 <= OneMemberCar[0]:
                    Cars=0

                elif Pen2 > OneMemberCar[0] and Pen2 <= (OneMemberCar[0]+OneMemberCar[1]):
                    Cars=1

                elif Pen2 > (OneMemberCar[0] + OneMemberCar[1]) and Pen2 <= (OneMemberCar[0] + OneMemberCar[1]+ OneMemberCar[2]):
                    Cars=2

                elif Pen2 > (OneMemberCar[0] + OneMemberCar[1]+ OneMemberCar[2]) and Pen2 <= (OneMemberCar[0] + OneMemberCar[1] + OneMemberCar[2]+ OneMemberCar[3]):
                    Cars = 3
                elif Pen2 > (OneMemberCar[0] + OneMemberCar[1] + OneMemberCar[2]+ OneMemberCar[3]):
                    Cars = 4
            if Members == 2:
                if Pen2 > 0 and Pen2 <= TwoMemberCar[0]:
                    Cars=0

                elif Pen2 > TwoMemberCar[0] and Pen2 <= (TwoMemberCar[0]+TwoMemberCar[1]):
                    Cars=1

                elif Pen2 > (TwoMemberCar[0] + TwoMemberCar[1]) and Pen2 <= (TwoMemberCar[0] + TwoMemberCar[1]+ TwoMemberCar[2]):
                    Cars=2

                elif Pen2 > (TwoMemberCar[0] + TwoMemberCar[1]+ TwoMemberCar[2]) and Pen2 <= (TwoMemberCar[0] + TwoMemberCar[1] + TwoMemberCar[2]+ TwoMemberCar[3]):
                    Cars = 3
                elif Pen2 > (TwoMemberCar[0] + TwoMemberCar[1] + TwoMemberCar[2]+ TwoMemberCar[3]):
                    Cars = 4
            if Members == 3:
                if Pen2 > 0 and Pen2 <= ThreeMemberCar[0]:
                    Cars=0

                elif Pen2 > ThreeMemberCar[0] and Pen2 <= (ThreeMemberCar[0]+ThreeMemberCar[1]):
                    Cars=1

                elif Pen2 > (ThreeMemberCar[0] + ThreeMemberCar[1]) and Pen2 <= (ThreeMemberCar[0] + ThreeMemberCar[1]+ ThreeMemberCar[2]):
                    Cars=2

                elif Pen2 > (ThreeMemberCar[0] + ThreeMemberCar[1]+ ThreeMemberCar[2]) and Pen2 <= (ThreeMemberCar[0] + ThreeMemberCar[1] + ThreeMemberCar[2]+ ThreeMemberCar[3]):
                    Cars = 3
                elif Pen2 > (ThreeMemberCar[0] + ThreeMemberCar[1] + ThreeMemberCar[2]+ ThreeMemberCar[3]):
                    Cars = 4
            if Members == 4:
                if Pen2 > 0 and Pen2 <= FourMemberCar[0]:
                    Cars=0

                elif Pen2 > FourMemberCar[0] and Pen2 <= (FourMemberCar[0]+FourMemberCar[1]):
                    Cars=1

                elif Pen2 > (FourMemberCar[0] + FourMemberCar[1]) and Pen2 <= (FourMemberCar[0] + FourMemberCar[1]+ FourMemberCar[2]):
                    Cars=2

                elif Pen2 > (FourMemberCar[0] + FourMemberCar[1]+ FourMemberCar[2]) and Pen2 <= (FourMemberCar[0] + FourMemberCar[1] + FourMemberCar[2]+ FourMemberCar[3]):
                    Cars = 3
                elif Pen2 > (FourMemberCar[0] + FourMemberCar[1] + FourMemberCar[2]+ FourMemberCar[3]):
                    Cars = 4

            MemberVals=[OneLoadMember[value], OneLoadMember[value] + TwoLoadMember[value], OneLoadMember[value] + TwoLoadMember[value] + ThreeLoadMember[value]]

            if Members == 1:
                CarVals=[OneMemberCar[0],OneMemberCar[0] + OneMemberCar[1] ,OneMemberCar[0] + OneMemberCar[1] + OneMemberCar[2],OneMemberCar[0] + OneMemberCar[1] + OneMemberCar[2]+ OneMemberCar[3]]
            elif Members == 2:
                CarVals=[TwoMemberCar[0],TwoMemberCar[0] + TwoMemberCar[1] ,TwoMemberCar[0] + TwoMemberCar[1] + TwoMemberCar[2],TwoMemberCar[0] + TwoMemberCar[1] + TwoMemberCar[2]+ TwoMemberCar[3]]
            elif Members == 3:
                CarVals=[ThreeMemberCar[0],ThreeMemberCar[0] + ThreeMemberCar[1] ,ThreeMemberCar[0] + ThreeMemberCar[1] + ThreeMemberCar[2],ThreeMemberCar[0] + ThreeMemberCar[1] + ThreeMemberCar[2]+ ThreeMemberCar[3]]
            elif Members == 4:
                CarVals=[FourMemberCar[0],FourMemberCar[0] + FourMemberCar[1] ,FourMemberCar[0] + FourMemberCar[1] + FourMemberCar[2],FourMemberCar[0] + FourMemberCar[1] + FourMemberCar[2]+ FourMemberCar[3]]

            #value
            CarAll=CarAll+Cars
            appendval=[CustStorage[i],value,Pen,Modify,MemberVals,Members,Pen2,CarVals,Cars]
            ChanceStorage.append(appendval)

        CarDemandStep= range(0,Cars)
        CarEVNum=[]
        CarEVNumPlaced = []
        CarEVSELevel=[]
        for j in CarDemandStep:
            val = random.uniform(1,348)
            val=int(UserInput.truncate(val,0))
            CarEVNum.append(val)
            rand= random.uniform(0,100)

            if rand >= 0 and rand <= L1_chance:
                Level=1
            elif rand > L1_chance and rand <= (L1_chance + L2_chance):
                Level=2
            CarEVSELevel.append(Level)
        for g in range(len(CarEVNum)):
            Num=0
            CarEVNumPlaced.append(Num)
        OutStore = [CustStorage[i], [Cars,Cars], CarEVNum, CarEVNumPlaced, CarEVSELevel, NameStorage[i]]
        OutputStorage.append(OutStore)


        i = i + 1

    #These two lines allow the study name to be changes, allows the base study to remain undisturbed
    filename_template = model_filename.split('.')
    filename_changed = filename_template[0] + '_EV_Holding_Created.'+ filename_template[1]
    #for HouseholdCars Use Case
    '''
    print 'EndGathering'
    for val in ChanceStorage:
        print val
    exit()
    '''

    cympy.study.Save(filename_changed)
    cympy.study.Close(False)
    end2 = datetime.now()
    print('HouseHold Cars Done in ' + str((end2 - start2).total_seconds()) + ' seconds')

    return OutputStorage, filename_changed, spotload_pre, CarAll

def PenetrationVsYears(Pen, Type, LaterStorage, AppliedNames, UnAppliedNames):
    '''
    PenetrationVsYears reads a csv the lists an estimated EV penetration value next too the year when it's expected
    to happen with two columns, one for the year, the other penetration

    This is used for determining the years to apply Load Growth at each penetration
    '''
    print 'penetrationvsyears'
    UseType='Fixed'
    if Type != '':
        UseType=Type
    path = "C:\\Users\\pwrlab07\\Downloads\\PenetrationVsYear.csv"
    df = pandas.read_csv(path)
    Years_df = df['Year']
    Penetration_df = df['Penetration']
    Pen=int(Pen)

    i=0
    ActualYear=0
    PreviousYear=0
    set = 0
    for val in Penetration_df:
        val=int(val)
        if set == 0:

            if val == Pen:
                ActualYear = int(Years_df[i])
                set=1


            elif (val - Pen) > 0 and i == 0:
                ActualYear = int(Years_df[0])
                set=1


            if i < len(Penetration_df - 1) and set == 0:
                if Pen > Penetration_df[i] and Pen < Penetration_df[i+1]:
                    #print 'yes'
                    year_dif=Years_df[i+1]-Years_df[i]
                    pen_dif=Penetration_df[i+1]-Penetration_df[i]
                    val=Pen-Penetration_df[i]
                    ActualYear=val*year_dif/pen_dif + Years_df[i]
                    set=1

        i=i+1

    if LaterStorage != []:
        for i in range(len(LaterStorage)):
            if LaterStorage[i][0] <= ActualYear and LaterStorage[i][5]==0:
                print 'application'
                print LaterStorage[i]

                IntLoadBranchCreation(LaterStorage[i][1],LaterStorage[i][2],LaterStorage[i][3],LaterStorage[i][4],LaterStorage[i][6])
                appendval=[LaterStorage[i][1], LaterStorage[i][6]]
                AppliedNames.append(appendval)
                integer=-1
                for name in UnAppliedNames:
                    integer = integer+1
                    if name[0] == LaterStorage[i][1]:
                        UnAppliedNames.pop(integer)


                print 'Section Applied'
                LaterStorage[i][5]=1

    CustTypes = cympy.study.ListCustomerTypes()

    CustTypes.remove(UseType)
    Networks = cympy.study.ListNetworks()
    #load_growth = cympy.study.LoadGrowth()
    #load_growth.GrowthPercent = 1.5
    #load_growth.SetIncludeCustormerType(UseType, False)

    ActualYear=int(math.floor(ActualYear))
    #Check to see if the current year of devices is the same as the year from the imported file
    #If it isn't the same year, apply load growth

    #if ActualYear != load_growth.GetActualGrowthYears(Networks, CustTypes)[0]:

    #load_growth.Apply(Networks, ActualYear)

    load_flow = cympy.sim.LoadFlow()
    load_flow.Run()

    print Pen
    return LaterStorage,AppliedNames, UnAppliedNames

def ReApply(model_filename, CustCarStorage, time, L1Store, L2Store, AppliedIntNames, time_int, PVDemandProfiles, BatteryDP,SPCUHold,whichloop):
    '''
    This function exists solely to reapplying different loads at different time steps
    '''
    load_flow = cympy.sim.LoadFlow()
    load_flow.Run()
    NamesApplied=[]
    place=0
    TotalApplied=0
    secondstep = 0
    for cust in CustCarStorage:

        OriValue=0
        if secondstep==1:
            if cust[5] == OldCust:
                OriValue=LastAdd
        valuePlace=-1
        CheckPlaced=-1
        for value in cust[3]:
            valuePlace=valuePlace+1
            if value==1:
                CheckPlaced=1
                OriValue=OriValue+L1Store[cust[2][valuePlace]][time]/1000
            if value==2:
                CheckPlaced = 2
                OriValue=OriValue+L2Store[cust[2][valuePlace]][time]/1000
            LastAdd=OriValue
            OldCust=cust[5]
            secondstep=1


        spot_load_device = cympy.study.GetDevice(cust[5], cympy.enums.DeviceType.SpotLoad)
        place=place+1
        if CheckPlaced != -1:
            NamesApplied.append(cust[0][0])
        FirstPhrase = "CustomerLoads.Get({num}).CustomerLoadModels.Get(1).".format(num=cust[5])
        SecondPhrase, kWPhase = PhaseCheck(FirstPhrase, spot_load_device)
        phrase=FirstPhrase + SecondPhrase + "LoadValue.KW"

        spot_load_device.SetValue(float(OriValue), phrase)
        TotalApplied=TotalApplied+int(OriValue)
    print 'Total Applied'
    print TotalApplied

    randvar=-1
    print 'Checking Application Loop {val} {val2}'.format(val=whichloop, val2=time)

    for value in AppliedIntNames:

        randvar=randvar+1
        print randvar
        print value[0]
        intspotload=value[0]+'-2'

        spot_load_device = cympy.study.GetDevice(intspotload, cympy.enums.DeviceType.SpotLoad)

        FirstPhrase = "CustomerLoads.Get({num}).CustomerLoadModels.Get(1).".format(num=cust[5])

        LoadA = "CustomerLoads.Get({num}).CustomerLoadModels.Get(1).CustomerLoadValues.Get(A).LoadValue.KW".format(num=intspotload)
        LoadB = "CustomerLoads.Get({num}).CustomerLoadModels.Get(1).CustomerLoadValues.Get(B).LoadValue.KW".format(num=intspotload)
        LoadC = "CustomerLoads.Get({num}).CustomerLoadModels.Get(1).CustomerLoadValues.Get(C).LoadValue.KW".format(num=intspotload)
        print value[1][whichloop][0][time]
        '''
        print 'values'
        print value[1]
        print'2'
        print value[1][0]
        print'3'
        print value[1][1]
        print'4'
        print value[1][1][0]
        print'5'
        print value[1][1][1]
        print'6'
        print value[1][1][0][0]
        print'7'
        print value[1][1][1][0]
        print spot_load_device
        print type(spot_load_device)
        '''
        spot_load_device.SetValue(float(value[1][whichloop][0][time]), LoadA)
        spot_load_device.SetValue(float(value[1][whichloop][1][time]), LoadB)
        spot_load_device.SetValue(float(value[1][whichloop][2][time]), LoadC)


    for value in PVDemandProfiles:

        spot_load_device = cympy.study.GetDevice(value[0], cympy.enums.DeviceType.Photovoltaic)
        Timestepstep= time%6
        Timestep=int((time-Timestepstep)/6)
        if Timestepstep == 0:
            HoldingFloat=float(value[1][Timestep])/1000
            spot_load_device.SetValue(HoldingFloat, "GenerationModels[0].ActiveGeneration")
        else:
            HoldingFloatA = float(value[1][Timestep]) / 1000
            HoldingFloatB = float(value[1][Timestep+1]) / 1000
            RealHolding= HoldingFloatA+((HoldingFloatB-HoldingFloatA)/6)*Timestepstep
            spot_load_device.SetValue(RealHolding, "GenerationModels[0].ActiveGeneration")
    '''
    print 'after a bit'
    print time
    print time_int
    print Timestep
    print float(value[1][Timestep])
    '''


    #Battery Controlling Code Below:
    randomint=0
    customername='BattLoad'
    Gencheck=0
    Loadcheck=0
    #First object in BatteryDP is
    for value in BatteryDP:
        randomint=randomint+1

        #InductionGen = cympy.study.GetDevice(InductionGeneratorName, 28)
        #Spotload = cympy.study.GetDevice(SpotloadName, 14)

        DisValue=str(value[0])+'-DISCHARGE'
        #print value[0]
        #print type(value[0])
        #print DisValue
        #print type(DisValue)
        InductionGen = cympy.study.GetDevice(DisValue, 28)

        #InductionGen.SetValue(DemandValue, "GenerationModels[0].ActiveGeneration")
        genval=float(value[2][time_int])
        InductionGen.SetValue(genval,"GenerationModels[0].ActiveGeneration")
        #InductionGen.SetValue("PF if you wanna set it","GenerationModels[0].PowerFactor")

        ChargeValue=str(value[0])+'-CHARGE'
        #print ChargeValue
        Spotload = cympy.study.GetDevice(ChargeValue, 14)
        customername = ChargeValue
        LoadA = "CustomerLoads.Get({num}).CustomerLoadModels.Get(1).CustomerLoadValues.Get(A).LoadValue.KW".format(num=customername)
        LoadB = "CustomerLoads.Get({num}).CustomerLoadModels.Get(1).CustomerLoadValues.Get(B).LoadValue.KW".format(num=customername)
        LoadC = "CustomerLoads.Get({num}).CustomerLoadModels.Get(1).CustomerLoadValues.Get(C).LoadValue.KW".format(num=customername)

        #Spotload.SetValue(ChargingValue/3, LoadA)
        loadval=float(value[1][time_int]/3)
        Spotload.SetValue((loadval), LoadA)
        Spotload.SetValue((loadval), LoadB)
        Spotload.SetValue((loadval), LoadC)

        model_filename_gen = 'C:\\Users\\pwrlab07\\PycharmProjects\\PGEPython\\INPUT\\GenertaionCheck.sxst'
        cympy.study.Save(model_filename_gen)
        Gencheck = 1
        cympy.study.Close(False)

        cympy.study.Open(model_filename)





    NamesApplied.sort(key=takeFirst, reverse=True)
    return NamesApplied

def takeFirst(elem):
    return elem[0]

def BESCreation(BESProfile, model_filename):
    randvar=0
    for SingleProfile in BESProfile:
        if randvar ==0:
            open_study(model_filename)
        else:
            open_study(model_filename2)
        spotload = cympy.study.ListDevices(14)
        XFMRByPhase = cympy.study.ListDevices(33)
        Cables = cympy.study.ListDevices(10)

        Spotload_USER_INPUT = str(SingleProfile[0])
        for abc in range(len(spotload)):
            # print abc
            #print type(spotload[abc].DeviceNumber)
            #print spotload[abc].DeviceNumber
            if spotload[abc].DeviceNumber == Spotload_USER_INPUT:

                spotindex = abc
        #print Spotload_USER_INPUT
        From1 = UserInput.NodeCheckSpot(spotload[spotindex].DeviceNumber)

        From2, To2 = UserInput.NodeCheck(spotload, XFMRByPhase, Cables, From1)

        NodeName = UserInput.NodeCheckSpot(spotload[spotindex].DeviceNumber)
        CheckingSec = spotload[spotindex].SectionID

        NetworkStr = spotload[spotindex].NetworkID

        AnotherStep = cympy.study.GetNode(From1)

        to_node = cympy.study.Node()
        to_node.ID = AnotherStep.ID + '-CHARGE'
        to_node.X = AnotherStep.X + 10
        to_node.Y = AnotherStep.Y + 10

        cympy.study.AddSection(CheckingSec + '-CHARGE', NetworkStr, To2 + '-CHARGE', cympy.enums.DeviceType.Underground,
                               AnotherStep.ID, to_node)
        #print '2222'
        #print CheckingSec

        cympy.study.AddDevice(Spotload_USER_INPUT + '-CHARGE', 14, CheckingSec + '-CHARGE')
        NewLoadCharge = cympy.study.GetLoad(Spotload_USER_INPUT + '-CHARGE', 14)

        NewDeviceCharge = cympy.study.GetDevice(Spotload_USER_INPUT + '-CHARGE', 14)
        NewLoadCharge.AddCustomerLoad('Anything')
        NewDeviceCharge.SetValue('Fixed',
                                 'CustomerLoads.Get({value}).CustomerType'.format(value=Spotload_USER_INPUT + '-CHARGE'))

        LoadA = "CustomerLoads.Get({num}).CustomerLoadModels.Get(1).CustomerLoadValues.Get(A).LoadValue.KW".format(
            num=Spotload_USER_INPUT + '-CHARGE')
        LoadB = "CustomerLoads.Get({num}).CustomerLoadModels.Get(1).CustomerLoadValues.Get(B).LoadValue.KW".format(
            num=Spotload_USER_INPUT + '-CHARGE')
        LoadC = "CustomerLoads.Get({num}).CustomerLoadModels.Get(1).CustomerLoadValues.Get(C).LoadValue.KW".format(
            num=Spotload_USER_INPUT + '-CHARGE')
        NewDeviceCharge.SetValue(0.0, LoadA)
        NewDeviceCharge.SetValue(0.0, LoadB)
        NewDeviceCharge.SetValue(0.0, LoadC)

        # model_filename_Tests = 'C:\\Users\\pwrlab07\\PycharmProjects\\PGEPython\\INPUT\\Ceder_Hills_CheckingAdd.sxst'
        model_filename_Tests = 'C:\\Users\\pwrlab07\\PycharmProjects\\PGEPython\\INPUT\\Swan_Island_Tests.sxst'

        to_node2 = cympy.study.Node()
        to_node2.ID = AnotherStep.ID + '-DISCHARGE'
        to_node2.X = AnotherStep.X - 10
        to_node2.Y = AnotherStep.Y - 10

        cympy.study.AddSection(CheckingSec + '-DISCHARGE', NetworkStr, To2 + '-DISCHARGE',
                               cympy.enums.DeviceType.Underground, AnotherStep.ID, to_node2)
        cympy.study.AddDevice(Spotload_USER_INPUT + '-DISCHARGE', 28, CheckingSec + '-DISCHARGE')
        InductionGen = cympy.study.GetDevice(Spotload_USER_INPUT + '-DISCHARGE', 28)
        InductionGen.SetValue(0.0, "GenerationModels[0].ActiveGeneration")
        InductionGen.SetValue(100.0, "GenerationModels[0].PowerFactor")
        model_filename2='C:\\Users\\pwrlab07\\PycharmProjects\\PGEPython\\INPUT\\Swan_Island_BESCreation.sxst'
        save_study(model_filename2)
        cympy.study.Close(False)
        randvar=randvar+1

    return model_filename2

def BESProfPull(ws, BatterySize, TimeCharge, TimeDischarge, LengthChoice):
    ws.range("D3").value = float(BatterySize)
    testrange=range(15,159)
    for value in testrange:
        stringReset = "L{value0}".format(value0=value)
        ws.range(stringReset).value = 0
    string="L{value1}".format(value1=TimeCharge)
    #print 'tests'
    #print ws.range(string).value
    #print string
    ws.range(string).value = 1
    #print 'tests'
    #print ws.range(string).value
    #print string
    string2 = "L{value2}".format(value2=TimeDischarge)
    ws.range(string2).value=-1
    if LengthChoice == 2:
        Discharge = ws.range("O15:O158").value
        Charge = ws.range("R15:R158").value
    if LengthChoice == 4:
        Discharge = ws.range("W15:W158").value
        Charge = ws.range("Z15:Z158").value

    return Charge,Discharge






