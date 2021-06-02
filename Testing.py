from __future__ import division
import pandas
import csv
import math
import lookup
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.pyplot import cm
from matplotlib.ticker import FuncFormatter
import pickle
import time
from pytz import timezone
import sys
import os
import difflib
import pandas as pd
import numpy as np
import ModifySpotLoad
import sys
import decimal
import UserInput
import xlwings as xw

print os.getcwd()
CYMPY_LOCATION = r"C:\Program Files (x86)\CYME\CYME"
sys.path.insert(1, CYMPY_LOCATION)
import cympy
import cympy.rm
import cympy.db
import cympy.eq

import function_study_analysis
from definitions import *
import random

ws = xw.Book(r"C:\Users\pwrlab07\Documents\EVSEHourlyDataTemplate2.xlsx").sheets('Scenerio1')
print ws.range("D3").value
# Battery Size
ws.range("D3").value=64.0
print ws.range("D3").value
print ws.range("B5").value
#2 Hour discharge rate
print ws.range("C5").value
#4 hour discharge rate

print ws.range("G3").value
#min battery charge %

print ws.range("G4").value
#Max battery charge %

# L15 = 0:00
# L16 = 0:10
# L51 = 6:00
#57 7
#63 8
#69 9
#75 10
#81 11
# L87 = 12:00
# L123 = 18:00
# L158 = 23:50

print ws.range("O15:O157")
Discharge2Hour= ws.range("O15:O157").value
Charge2Hour= ws.range("R15:R157").value
Discharge4Hour= ws.range("W15:W157").value
Charge4Hour= ws.range("Z15:Z157").value
print type(ws.range("O15:O157"))
print 'hmm'
print Discharge2Hour[4:6]
ws.range("D3").value=32.0
Discharge2Hour= ws.range("O15:O158").value
print Discharge2Hour
exit()
print 'blrg'
if ws.range("G6").value == 2:
    Discharge = ws.range("O15:O158").value
    Charge = ws.range("R15:R158").value
if ws.range("G6").value == 4:
    Discharge= ws.range("W15:W158").value
    Charge= ws.range("Z15:Z158").value
exit()
'''
ModifySpotLoad.open_study('C:\\Users\\pwrlab07\\PycharmProjects\\PGEPython\\INPUT\\Swan_Island_New_Connections.sxst')
spotload = cympy.study.ListDevices(14)
XFMRByPhase = cympy.study.ListDevices(33)
Cables = cympy.study.ListDevices(10)

Spotload_USER_INPUT='OID_1268955'
for abc in range(len(spotload)):
    if spotload[abc].DeviceNumber == Spotload_USER_INPUT:
        # print abc
        spotindex = abc

From1 = UserInput.NodeCheckSpot(spotload[spotindex].DeviceNumber)

From2, To2 = UserInput.NodeCheck(spotload, XFMRByPhase, Cables, From1)

NodeName=UserInput.NodeCheckSpot(spotload[spotindex].DeviceNumber)
CheckingSec = spotload[spotindex].SectionID

NetworkStr = spotload[spotindex].NetworkID

AnotherStep = cympy.study.GetNode(From1)

to_node = cympy.study.Node()
to_node.ID = AnotherStep.ID + '-CHARGE'
to_node.X = AnotherStep.X + 10
to_node.Y = AnotherStep.Y + 10

cympy.study.AddSection(CheckingSec + '-CHARGE', NetworkStr, To2 + '-CHARGE', cympy.enums.DeviceType.Underground, AnotherStep.ID,to_node)
print '2222'
print CheckingSec

cympy.study.AddDevice(Spotload_USER_INPUT + '-CHARGE', 14, CheckingSec+'-CHARGE')
NewLoadCharge = cympy.study.GetLoad(Spotload_USER_INPUT + '-CHARGE', 14)

NewDeviceCharge = cympy.study.GetDevice(Spotload_USER_INPUT + '-CHARGE', 14)
NewLoadCharge.AddCustomerLoad('Anything')
NewDeviceCharge.SetValue('Fixed', 'CustomerLoads.Get({value}).CustomerType'.format(value=Spotload_USER_INPUT +'-CHARGE'))


LoadA = "CustomerLoads.Get({num}).CustomerLoadModels.Get(1).CustomerLoadValues.Get(A).LoadValue.KW".format(num=Spotload_USER_INPUT + '-CHARGE')
LoadB = "CustomerLoads.Get({num}).CustomerLoadModels.Get(1).CustomerLoadValues.Get(B).LoadValue.KW".format(num=Spotload_USER_INPUT + '-CHARGE')
LoadC = "CustomerLoads.Get({num}).CustomerLoadModels.Get(1).CustomerLoadValues.Get(C).LoadValue.KW".format(num=Spotload_USER_INPUT + '-CHARGE')
NewDeviceCharge.SetValue(11.1, LoadA)
NewDeviceCharge.SetValue(22.2, LoadB)
NewDeviceCharge.SetValue(33.3, LoadC)

# model_filename_Tests = 'C:\\Users\\pwrlab07\\PycharmProjects\\PGEPython\\INPUT\\Ceder_Hills_CheckingAdd.sxst'
model_filename_Tests = 'C:\\Users\\pwrlab07\\PycharmProjects\\PGEPython\\INPUT\\Swan_Island_Tests.sxst'

to_node2 = cympy.study.Node()
to_node2.ID = AnotherStep.ID + '-DISCHARGE'
to_node2.X = AnotherStep.X - 10
to_node2.Y = AnotherStep.Y - 10

cympy.study.AddSection(CheckingSec + '-DISCHARGE', NetworkStr, To2 + '-DISCHARGE', cympy.enums.DeviceType.Underground, AnotherStep.ID,to_node2)
cympy.study.AddDevice(Spotload_USER_INPUT + '-DISCHARGE', 28, CheckingSec+'-DISCHARGE')
NewDeviceCharge = cympy.study.GetDevice(Spotload_USER_INPUT + '-Discharge', 28)
genval = float(50.0)
InductionGen = cympy.study.GetDevice(Spotload_USER_INPUT + '-DISCHARGE', 28)
InductionGen.SetValue(genval, "GenerationModels[0].ActiveGeneration")
function_study_analysis.save_study(model_filename_Tests)

InductionGen.SetValue(100.0,"GenerationModels[0].PowerFactor")

print 'blah222'
exit()
'''
'''
name="testingvar"
test=eval(name)
print test

exit()
'''
'''
exec('gg=0')
print gg
exit()
'''
'''
model_filename = "C:\\Users\\pwrlab07\\Downloads\\EVSEHourlyDataTemplate.csv"
IntProfileFull=[]
i=0
cympy.study.Open(model_filename)

xfmr_byphase = function_study_analysis.list_devices(cympy.enums.DeviceType.TransformerByPhase)
Spots = function_study_analysis.list_devices(cympy.enums.DeviceType.SpotLoad)
lf = cympy.sim.LoadFlow()
lf.Run()
for value in Spots['NetworkID']:
    if value == "SWAN ISLAND-BASIN":
        print 'Basin'
    if value == "SWAN ISLAND-DOLPHIN":
        print 'Dolphin'
    if value == "SWAN ISLAND-FREIGHTLINER":
        print 'Freightliner'
    if value == "SWAN ISLAND-GOING":
        print 'Going'
    if value == "SWAN ISLAND-SHIPYARD":
        print 'Shipyard'
exit()
'''
model_filename = "C:\\Users\\pwrlab07\\Downloads\\EVSEHourlyDataTemplate.xlsx"
import subprocess
IntProfileFull=[]

testval=pandas.read_excel(model_filename, sheet_name=0)
h=-1
value=testval.columns[3]
value2=testval.columns[1]
print testval.at[1,value]
print testval.at[3,value2]
testval.at[1,value] = 23.0
model_filename = "C:\\Users\\pwrlab07\\Downloads\\EVSEHourlyDataTemplateTest.xlsx"
testval.to_excel(model_filename)
testval=pandas.read_excel(model_filename, sheet_name=0)
print testval.at[1,value]
print testval.at[3,value2]
exit()

IntProfileAppend=[[],[],[],[],[]]
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
        print value
        print testint
        if value != 'Time':
            if IntProfileAppend[testint] == '':
                IntProfileAppend[testint] = (list(testval0[value]))
            else:
                IntProfileAppend[testint].append(list((testval0[value])))
IntProfileFull.append(IntProfileAppend)
print IntProfileAppend
print '0'
print IntProfileAppend[0]
print '1'
print IntProfileAppend[1]
exit()

if i ==0:
    for value in string1:
        if value != 'Time':
            #value1=exec("")
            if IntProfile0[0] == '':
                IntProfile0[0] = (list(IntProf0[value]))
            else:
                IntProfile0[0].append(list((IntProf0[value])))
    for value in IntProf1:
        if value != 'Time':
            if IntProfile0[1] == '':
                IntProfile0[1] = (list(IntProf1[value]))
            else:
                IntProfile0[1].append(list((IntProf1[value])))
    for value in IntProf2:
        if value != 'Time':
            if IntProfile0[2] == '':
                IntProfile0[2] = (list(IntProf2[value]))
            else:
                IntProfile0[2].append(list((IntProf2[value])))
    for value in IntProf3:
        if value != 'Time':
            if IntProfile0[3] == '':
                IntProfile0[3] = (list(IntProf3[value]))
            else:
                IntProfile0[3].append(list((IntProf3[value])))
    for value in IntProf4:
        if value != 'Time':
            if IntProfile0[4] == '':
                IntProfile0[4] = (list(IntProf4[value]))
            else:
                IntProfile0[4].append(list((IntProf4[value])))
    IntProfile[0]=IntProfile0


#print testval.keys()
print testval.sheet_names
print '1'
print IntProf0

print testval.parse(1, skiprows=1)
print '2'
print IntProf1
print 'uhuh'
print type(testval.parse(1))
print type(IntProf1)
exit()
'''

model_filename = 'C:\\Users\\pwrlab07\\PycharmProjects\\PGEPython\\INPUT\\SwanIslandNew.sxst'
function_study_analysis.open_study(model_filename)

xfmr_byphase = function_study_analysis.list_devices(cympy.enums.DeviceType.TransformerByPhase)
'''
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
time = range(30672,(30672+1011))
for tim in time:
    for value in PVStore:
        print "time"
        print tim
        spot_load_device = cympy.study.GetDevice(value[0], cympy.enums.DeviceType.Photovoltaic)
        Timestepstep = tim % 6
        Timestep = int((tim - Timestepstep) / 6)
        if Timestepstep == 0:
            HoldingFloat = float(value[1][Timestep]) / 1000
            spot_load_device.SetValue(HoldingFloat, "GenerationModels[0].ActiveGeneration")
            if int(HoldingFloat) != 0:
                print 'Zero Remainder Value'
                print HoldingFloat
        else:
            HoldingFloatA = float(value[1][Timestep]) / 1000
            HoldingFloatB = float(value[1][Timestep + 1]) / 1000
            RealHolding = HoldingFloatA + ((HoldingFloatB - HoldingFloatA) / 6) * Timestepstep
            spot_load_device.SetValue(RealHolding, "GenerationModels[0].ActiveGeneration")
            if int(RealHolding) != 0:
                print 'RealHolding Value'
                print RealHolding
                print 'totes done'
                print value[0]
                model_filename = 'C:\\Users\\pwrlab07\\PycharmProjects\\PGEPython\\INPUT\\Swan_Island_SolarChecking.sxst'
                function_study_analysis.save_study(model_filename)
                cympy.study.Close()
                exit()

print 'Full Completion of test'
exit()
'''
'''
print (6 % 6) == 0
print 6 % 6 == 0
print 10%4
exit()
'''

xfmr_cable = function_study_analysis.list_devices(cympy.enums.DeviceType.Underground)

xfmr_cable_Other = function_study_analysis.list_devices(cympy.enums.DeviceType.OverheadLine)
'''
for device in xfmr_cable['device_number']:
    deviceID=10
    print device
    print type(device)
    print 'device number'
    spot_load_device = cympy.study.GetDevice(device, deviceID)
    print cympy.study.QueryInfoDevice("LOADINGA", device, deviceID)

    print cympy.study.QueryInfoDevice("LOADINGB", device, deviceID)

    print cympy.study.QueryInfoDevice("LOADINGC", device, deviceID)

    print cympy.study.QueryInfoDevice("VpuAinput", device, deviceID)

    print cympy.study.QueryInfoDevice("VpuBinput", device, deviceID)

    print cympy.study.QueryInfoDevice("VpuCinput", device, deviceID)
    exit()
    break
'''
print 'hmmmm'
print xfmr_cable_Other
for device in xfmr_cable_Other['device_number']:
    deviceID=11
    print device
    print type(device)
    print 'device number 1'

    spot_load_device = cympy.study.GetDevice(device, deviceID)
    print cympy.study.QueryInfoDevice("LOADINGA", device, deviceID)

    print cympy.study.QueryInfoDevice("LOADINGB", device, deviceID)

    print cympy.study.QueryInfoDevice("LOADINGC", device, deviceID)

    print cympy.study.QueryInfoDevice("VpuAinput", device, deviceID)

    print cympy.study.QueryInfoDevice("VpuBinput", device, deviceID)

    print cympy.study.QueryInfoDevice("VpuCinput", device, deviceID)


exit()
'''
#spot_load_device = cympy.study.GetDevice(device, 28)
print spot_load_device
#spot_load_device.SetValue("Connected","ConnectionStatus")
'''
'''
try:
    print spot_load_device.GetValue("DeviceID")
    isAB = 1
except cympy.err.CymError:
    print 'DeviceID is Null'
try:
    print spot_load_device.GetValue("Location")
    isAB = 1
except cympy.err.CymError:
    print 'Location is Null'
try:
    print spot_load_device.GetValue("Phase")
    isAB = 1
except cympy.err.CymError:
    print 'Phase is Null'
try:
    print spot_load_device.GetValue("SymbolSize")
    isAB = 1
except cympy.err.CymError:
    print 'SymbolSize is Null'

try:
    print spot_load_device.GetValue("CTConnection")
    isAB = 1
except cympy.err.CymError:
    print 'CTConnection is Null'
try:
    print spot_load_device.GetValue("GenerationModels[0].ActiveGeneration")
    isAB = 1
except cympy.err.CymError:
    print 'ActiveGeneration is Null'
try:
    print spot_load_device.GetValue("GenerationModels[0].PowerFactor")
    isAB = 1
except cympy.err.CymError:
    print 'PowerFactor is Null'
try:
    print spot_load_device.GetValue("KWSet")
    isAB = 1
except cympy.err.CymError:
    print 'KWSet is Null'
try:
    print spot_load_device.GetValue("PowerFactor")
    isAB = 1
except cympy.err.CymError:
    print 'PowerFactor is Null'
try:
    print spot_load_device.GetValue("NumberOfGenerators")
    isAB = 1
except cympy.err.CymError:
    print 'NumberOfGenerators is Null'

try:
    print spot_load_device.GetValue("FaultContributionUnit")
    isAB = 1
except cympy.err.CymError:
    print 'FaultContributionUnit is Null'
try:
    print spot_load_device.GetValue("FaultContribution")
    isAB = 1
except cympy.err.CymError:
    print 'FaultContribution is Null'
'''
'''

'''
#model_filename = 'C:\\Users\\pwrlab07\\PycharmProjects\\PGEPython\\INPUT\\Swan_Island_Connections.sxst'
model_filename = 'C:\\Users\\pwrlab07\\PycharmProjects\\PGEPython\\INPUT\\Swan_Island_New_Connections.sxst'
function_study_analysis.save_study(model_filename)
cympy.study.Close()
exit()
'''
string='0.125+1.000j'
print string
print type(string)
evald=string.split("-")
'''
"""
try:
    evald=string.split("-")
    isAB=1
except IndexError:
    isAB = 0

try:
    evald=string.split("+")
    isABC=1
except IndexError:
    isABC = 0
"""

print evald
print len(evald)
evald=string.split("+")
print evald
print len(evald)
exit()
evald[1]=evald[1].split("j")
print evald
print type(evald)
exit()

'''
Type=''
LaterStorage=[]
AppliedNames=[]
UnAppliedNames=[]
print UnAppliedNames
UnAppliedNames.append(LaterStorage)
UnAppliedNames.append(AppliedNames)
print UnAppliedNames
exit()
Penetration=range(0,100,1)
for Pen in Penetration:
    ModifySpotLoad.PenetrationVsYears(Pen, Type, LaterStorage, AppliedNames, UnAppliedNames)
exit()
print Penetration
exit()
ModifySpotLoad.PenetrationVsYears(7, Type, LaterStorage, AppliedNames, UnAppliedNames)
blah=['A:25 61631', [72], [], []]
for val in blah:
    print val[0]
exit()
val=[[], [], [1]]
for num in val:
    if num != []:
        for value in num:
            print 'value'
            print value
    print 'num'
    print num
exit()
'''

os.chdir("C:\Users\pwrlab07\Desktop\Sheeran Folder\ChartHold\\")
# Create a Pandas dataframe from some data.
df = pd.DataFrame([9,5,3,2],index=[40,60,80,100])

# Create a Pandas Excel writer using XlsxWriter as the engine.
writer = pd.ExcelWriter('pandas_chart.xlsx', engine='xlsxwriter')

# Convert the dataframe to an XlsxWriter Excel object.
df.to_excel(writer, sheet_name='Sheet1')

# Get the xlsxwriter workbook and worksheet objects.
workbook  = writer.book
worksheet = writer.sheets['Sheet1']


# Create a chart object.
chart = workbook.add_chart({'type': 'column'})

# Configure the series of the chart from the dataframe data.
chart.add_series({'values': '=Sheet1!$B$2:$B$5',
                    'categories':'=Sheet1!$A$2:$A$5',
                  'gap':20
})
#chart.add_series({'values': '=Sheet1!$B$6:$B$9'})

chart.set_title({'name': 'Year End Results'})
chart.set_x_axis({
    'name': 'Length of Overload Events (1 = 10 minutes)',
    'name_font': {'size': 14, 'bold': True},
    'min' : 2,
    'max' : 7,
})
chart.set_y_axis({
    'name': 'Number of times these events happened',
    'name_font': {'size': 14, 'bold': True},
    'major_gridlines': {'visible': True}
})
# Insert the chart into the worksheet.
worksheet.insert_chart('D2', chart)

# Close the Pandas Excel writer and output the Excel file.
writer.save()
exit()
names=[['PRIOH100007', 0], ['PRIOH100606-1', 0], ['PRIOH100606-2', 0], ['PRIOH1006965', 0], ['PRIOH100730-1', 0], ['PRIOH100730-2', 0], ['PRIOH100730-3', 0], ['PRIOH100730-4', 0], ['PRIOH100730-5', 0], ['PRIOH101008', 0], ['PRIOH101019', 0], ['PRIOH101039-1', 0], ['PRIOH101039-2', 0], ['PRIOH101039-3', 0], ['PRIOH101119-1', 0], ['PRIOH101119-2', 0], ['PRIOH101119-3', 0], ['PRIOH101119-4', 0], ['PRIOH101119-5', 0], ['PRIOH101442-1', 0], ['PRIOH101442-2', 0], ['PRIOH1015331', 0], ['PRIOH101560-1', 0], ['PRIOH101560-2', 0], ['PRIOH101583-1', 0], ['PRIOH101583-2', 0], ['PRIOH101594-1', 0], ['PRIOH101594-2', 0], ['PRIOH101675', 0], ['PRIOH101838', 0], ['PRIOH101865', 0], ['PRIOH101989', 0], ['PRIOH102158-1', 0], ['PRIOH102158-2', 0], ['PRIOH102158-3', 0], ['PRIOH102158-4', 0], ['PRIOH102237', 0], ['PRIOH102278-1', 0], ['PRIOH102278-2', 0], ['PRIOH102345', 0], ['PRIOH102360', 0], ['PRIOH102489-1', 0], ['PRIOH102489-2', 0], ['PRIOH103321-1', 0], ['PRIOH103321-2', 0], ['PRIOH103321-3', 0], ['PRIOH103321-4', 0], ['PRIOH103321-5', 0], ['PRIOH103321-6', 0], ['PRIOH103461', 0], ['PRIOH103566-1', 0], ['PRIOH103566-2', 0], ['PRIOH103741-1', 0], ['PRIOH103741-2', 0], ['PRIOH103741-3', 0], ['PRIOH103741-4', 0], ['PRIOH103877', 0], ['PRIOH104185-1', 0], ['PRIOH104185-2', 0], ['PRIOH104258-1', 0], ['PRIOH104258-2', 0], ['PRIOH104465-1', 0], ['PRIOH104465-2', 0], ['PRIOH104465-3', 0], ['PRIOH104497-1', 0], ['PRIOH104497-2', 0], ['PRIOH104647-1', 0], ['PRIOH104647-2', 0], ['PRIOH104652', 0], ['PRIOH104831-1', 0], ['PRIOH104831-2', 0], ['PRIOH104831-3', 0], ['PRIOH104977-1', 0], ['PRIOH104977-2', 0], ['PRIOH105571-1', 0], ['PRIOH105571-2', 0], ['PRIOH105571-3', 0], ['PRIOH105571-4', 0], ['PRIOH105571-5', 0], ['PRIOH105631', 0], ['PRIOH105793', 0], ['PRIOH106002', 0], ['PRIOH106360-1', 0], ['PRIOH106360-2', 0], ['PRIOH106365', 0], ['PRIOH106439-1', 0], ['PRIOH106439-2', 0], ['PRIOH107403', 0], ['PRIOH107465-1', 0], ['PRIOH107465-2', 0], ['PRIOH107465-3', 0], ['PRIOH107465-4', 0], ['PRIOH107552', 0], ['PRIOH107698-1', 0], ['PRIOH107698-2', 0], ['PRIOH107719', 0], ['PRIOH107808-1', 0], ['PRIOH107808-2', 0], ['PRIOH1081505', 0], ['PRIOH108626', 0], ['PRIOH108881', 0], ['PRIOH108906-1', 0], ['PRIOH108906-2', 0], ['PRIOH109137-1', 0], ['PRIOH109137-2', 0], ['PRIOH109821', 0], ['PRIOH109827', 0], ['PRIOH110477-1', 0], ['PRIOH110477-2', 0], ['PRIOH110477-3', 0], ['PRIOH110515-1', 0], ['PRIOH110515-2', 0], ['PRIOH110515-3', 0], ['PRIOH1106162', 0], ['PRIOH110755', 0], ['PRIOH110976-1', 0], ['PRIOH110976-2', 0], ['PRIOH110976-3', 0], ['PRIOH1109985', 0], ['PRIOH111034', 0], ['PRIOH111096-1', 0], ['PRIOH111096-2', 0], ['PRIOH111122', 0], ['PRIOH111550', 0], ['PRIOH111891-1', 0], ['PRIOH111891-2', 0], ['PRIOH112023-1', 0], ['PRIOH112023-2', 0], ['PRIOH112105-1', 0], ['PRIOH112105-2', 0], ['PRIOH112105-3', 0], ['PRIOH112144-1', 0], ['PRIOH112144-2', 0], ['PRIOH112202-1', 0], ['PRIOH112202-2', 0], ['PRIOH112211-1', 0], ['PRIOH112211-2', 0], ['PRIOH112365', 0], ['PRIOH112515-1', 0], ['PRIOH112515-2', 0], ['PRIOH112532', 0], ['PRIOH112538', 0], ['PRIOH112598', 0], ['PRIOH112617-1', 0], ['PRIOH112617-2', 0], ['PRIOH112617-3', 0], ['PRIOH112617-4', 0], ['PRIOH112617-5', 0], ['PRIOH112629', 0], ['PRIOH112823-1', 0], ['PRIOH112823-2', 0], ['PRIOH112823-3', 0], ['PRIOH112902-1', 0], ['PRIOH112902-2', 0], ['PRIOH113051', 0], ['PRIOH115038', 0], ['PRIOH115358', 0], ['PRIOH115789', 0], ['PRIOH115815', 0], ['PRIOH115827', 0], ['PRIOH115833', 0], ['PRIOH116412', 0], ['PRIOH1164385-1', 0], ['PRIOH1164385-2', 0], ['PRIOH1164385-3', 0], ['PRIOH1164386', 0], ['PRIOH116777', 0], ['PRIOH117065-1', 0], ['PRIOH117065-2', 0], ['PRIOH117065-3', 0], ['PRIOH117104-1', 0], ['PRIOH117104-2', 0], ['PRIOH117104-3', 0], ['PRIOH117104-4', 0], ['PRIOH117343-1', 0], ['PRIOH117343-2', 0], ['PRIOH117343-3', 0], ['PRIOH117371', 0], ['PRIOH117421-1', 0], ['PRIOH117421-2', 0], ['PRIOH117544', 0], ['PRIOH117990', 0], ['PRIOH118633-1', 0], ['PRIOH118633-2', 0], ['PRIOH118633-3', 0], ['PRIOH118816', 0], ['PRIOH118831', 0], ['PRIOH118851-1', 0], ['PRIOH118851-2', 0], ['PRIOH119730', 0], ['PRIOH119756-1', 0], ['PRIOH119756-2', 0], ['PRIOH119831', 0], ['PRIOH120174-1', 0], ['PRIOH120174-2', 0], ['PRIOH120174-3', 0], ['PRIOH120262', 0], ['PRIOH120287', 0], ['PRIOH120340-1', 0], ['PRIOH120340-2', 0], ['PRIOH121027', 0], ['PRIOH121073-1', 0], ['PRIOH121073-2', 0], ['PRIOH121149-1', 0], ['PRIOH121149-2', 0], ['PRIOH121149-3', 0], ['PRIOH121278', 0], ['PRIOH121800-1', 0], ['PRIOH121800-2', 0], ['PRIOH122292-1', 0], ['PRIOH122292-2', 0], ['PRIOH122921-1', 0], ['PRIOH122921-2', 0], ['PRIOH123296', 0], ['PRIOH123388', 0], ['PRIOH123455', 0], ['PRIOH123761-1', 0], ['PRIOH123761-2', 0], ['PRIOH123808', 0], ['PRIOH124155', 0], ['PRIOH124637', 0], ['PRIOH124817', 0], ['PRIOH124917-1', 0], ['PRIOH124917-2', 0], ['PRIOH124917-3', 0], ['PRIOH124917-4', 0], ['PRIOH125170', 0], ['PRIOH125193', 0], ['PRIOH125466', 0], ['PRIOH125504-1', 0], ['PRIOH125504-2', 0], ['PRIOH125545-1', 0], ['PRIOH125545-2', 0], ['PRIOH126008', 0], ['PRIOH126089', 0], ['PRIOH126117', 0], ['PRIOH126172-1', 0], ['PRIOH126172-2', 0], ['PRIOH126287-1', 0], ['PRIOH126287-2', 0], ['PRIOH126287-3', 0], ['PRIOH126287-4', 0], ['PRIOH126287-5', 0], ['PRIOH1263905', 0], ['PRIOH1263925', 0], ['PRIOH126470-1', 0], ['PRIOH126470-2', 0], ['PRIOH126470-3', 0], ['PRIOH126500-1', 0], ['PRIOH126500-2', 0], ['PRIOH126709-1', 0], ['PRIOH126709-2', 0], ['PRIOH127035-1', 0], ['PRIOH127035-2', 0], ['PRIOH127084', 0], ['PRIOH127163', 0], ['PRIOH127163-1', 0], ['PRIOH127428', 0], ['PRIOH127613-1', 0], ['PRIOH127613-2', 0], ['PRIOH128164', 0], ['PRIOH128257-1', 0], ['PRIOH128257-2', 0], ['PRIOH128257-3', 0], ['PRIOH128388-1', 0], ['PRIOH128388-2', 0], ['PRIOH128416', 0], ['PRIOH128871', 0], ['PRIOH1288865', 0], ['PRIOH1288866', 0], ['PRIOH128968', 0], ['PRIOH129087-1', 0], ['PRIOH129087-2', 0], ['PRIOH129087-3', 0], ['PRIOH129087-4', 0], ['PRIOH129158', 0], ['PRIOH129414-1', 0], ['PRIOH129414-2', 0], ['PRIOH129414-3', 0], ['PRIOH129414-4', 0], ['PRIOH129414-5', 0], ['PRIOH129414-6', 0], ['PRIOH129414-7', 0], ['PRIOH129466', 0], ['PRIOH129625', 0], ['PRIOH129652', 0], ['PRIOH129695-1', 0], ['PRIOH129695-2', 0], ['PRIOH130403-1', 0], ['PRIOH130403-2', 0], ['PRIOH130525', 0], ['PRIOH130581', 0], ['PRIOH130760', 0], ['PRIOH130914-1', 0], ['PRIOH130914-2', 0], ['PRIOH131379', 0], ['PRIOH132307-1', 0], ['PRIOH132307-2', 0], ['PRIOH132511', 0], ['PRIOH132511-1', 0], ['PRIOH132640-1', 0], ['PRIOH132640-2', 0], ['PRIOH132968', 0], ['PRIOH133224', 0], ['PRIOH133288', 0], ['PRIOH134013', 0], ['PRIOH134058-1', 0], ['PRIOH134058-2', 0], ['PRIOH134487', 0], ['PRIOH134518-1', 0], ['PRIOH134518-2', 0], ['PRIOH134518-3', 0], ['PRIOH134518-4', 0], ['PRIOH134994-1', 0], ['PRIOH134994-2', 0], ['PRIOH135283-1', 0], ['PRIOH135283-2', 0], ['PRIOH136108-1', 0], ['PRIOH136108-2', 0], ['PRIOH136188-1', 0], ['PRIOH136188-2', 0], ['PRIOH136290', 0], ['PRIOH136671', 0], ['PRIOH136699-1', 0], ['PRIOH136699-2', 0], ['PRIOH137011-1', 0], ['PRIOH137011-2', 0], ['PRIOH137061', 0], ['PRIOH137260-1', 0], ['PRIOH137260-2', 0], ['PRIOH137380-1', 0], ['PRIOH137380-2', 0], ['PRIOH137552', 0], ['PRIOH137862', 0], ['PRIOH138097', 0], ['PRIOH138224', 0], ['PRIOH138498', 0], ['PRIOH138550-1', 0], ['PRIOH138550-2', 0], ['PRIOH138713', 0], ['PRIOH138842', 0], ['PRIOH138901-1', 0], ['PRIOH138901-2', 0], ['PRIOH138925', 0], ['PRIOH139274', 0], ['PRIOH139299', 0], ['PRIOH139792-1', 0], ['PRIOH139792-2', 0], ['PRIOH140584-1', 0], ['PRIOH140584-2', 0], ['PRIOH140584-3', 0], ['PRIOH140584-4', 0], ['PRIOH140584-5', 0], ['PRIOH140690-1', 0], ['PRIOH140690-2', 0], ['PRIOH140757-1', 0], ['PRIOH140757-2', 0], ['PRIOH140799', 0], ['PRIOH141158', 0], ['PRIOH141286', 0], ['PRIOH141287', 0], ['PRIOH141357', 0], ['PRIOH141358-1', 0], ['PRIOH141358-2', 0], ['PRIOH141407', 0], ['PRIOH141612-1', 0], ['PRIOH141612-2', 0], ['PRIOH141612-3', 0], ['PRIOH141853-1', 0], ['PRIOH141853-2', 0], ['PRIOH141853-3', 0], ['PRIOH141959-1', 0], ['PRIOH141959-2', 0], ['PRIOH142091', 0], ['PRIOH142206', 0], ['PRIOH142597', 0], ['PRIOH142802', 0], ['PRIOH143047-1', 0], ['PRIOH143047-2', 0], ['PRIOH143060-1', 0], ['PRIOH143060-2', 0], ['PRIOH143266', 0], ['PRIOH143545', 0], ['PRIOH143787', 0], ['PRIOH143802', 0], ['PRIOH144247-1', 0], ['PRIOH144247-2', 0], ['PRIOH144247-3', 0], ['PRIOH144944-1', 0], ['PRIOH144944-2', 0], ['PRIOH145381', 0], ['PRIOH145500', 0], ['PRIOH145603', 0], ['PRIOH145607-1', 0], ['PRIOH145607-2', 0], ['PRIOH145607-3', 0], ['PRIOH145607-4', 0], ['PRIOH145607-5', 0], ['PRIOH145878-1', 0], ['PRIOH145878-2', 0], ['PRIOH145881', 0], ['PRIOH146163-1', 0], ['PRIOH146163-2', 0], ['PRIOH146163-3', 0], ['PRIOH146163-4', 0], ['PRIOH146163-5', 0], ['PRIOH146406', 0], ['PRIOH147130-1', 0], ['PRIOH147130-2', 0], ['PRIOH147130-3', 0], ['PRIOH147130-4', 0], ['PRIOH147182', 0], ['PRIOH147503-1', 0], ['PRIOH147503-2', 0], ['PRIOH147503-3', 0], ['PRIOH147526', 0], ['PRIOH147986-1', 0], ['PRIOH147986-2', 0], ['PRIOH148116-1', 0], ['PRIOH148116-2', 0], ['PRIOH148160-1', 0], ['PRIOH148160-2', 0], ['PRIOH148252-1', 0], ['PRIOH148252-2', 0], ['PRIOH148494-1', 0], ['PRIOH148494-2', 0], ['PRIOH148745-1', 0], ['PRIOH148745-2', 0], ['PRIOH148829', 0], ['PRIOH149202', 0], ['PRIOH149323', 0], ['PRIOH149340-1', 0], ['PRIOH149340-2', 0], ['PRIOH149454-1', 0], ['PRIOH149454-2', 0], ['PRIOH149460', 0], ['PRIOH149544-1', 0], ['PRIOH149544-2', 0], ['PRIOH149739-1', 0], ['PRIOH149739-2', 0], ['PRIOH149874-1', 0], ['PRIOH149874-2', 0], ['PRIOH149874-3', 0], ['PRIOH149921', 0], ['PRIOH150520-1', 0], ['PRIOH150520-2', 0], ['PRIOH150520-3', 0], ['PRIOH150726', 0], ['PRIOH151413', 0], ['PRIOH151575', 0], ['PRIOH151647', 0], ['PRIOH152115-1', 0], ['PRIOH152115-2', 0], ['PRIOH153231-1', 0], ['PRIOH153231-2', 0], ['PRIOH153233-1', 0], ['PRIOH153233-2', 0], ['PRIOH153233-3', 0], ['PRIOH153502', 0], ['PRIOH153542', 0], ['PRIOH153649', 0], ['PRIOH153654-1', 0], ['PRIOH153654-2', 0], ['PRIOH153742-1', 0], ['PRIOH153742-2', 0], ['PRIOH153742-3', 0], ['PRIOH153742-4', 0], ['PRIOH153936', 0], ['PRIOH154240-1', 0], ['PRIOH154240-2', 0], ['PRIOH154464', 0], ['PRIOH154616', 0], ['PRIOH154643', 0], ['PRIOH154651', 0], ['PRIOH154943', 0], ['PRIOH155176-1', 0], ['PRIOH155176-2', 0], ['PRIOH155407-1', 0], ['PRIOH155407-2', 0], ['PRIOH155425-1', 0], ['PRIOH155425-2', 0], ['PRIOH156226', 0], ['PRIOH156455-1', 0], ['PRIOH156455-2', 0], ['PRIOH156563-1', 0], ['PRIOH156563-2', 0], ['PRIOH156563-3', 0], ['PRIOH156649-1', 0], ['PRIOH156649-2', 0], ['PRIOH156687-1', 0], ['PRIOH156687-2', 0], ['PRIOH156941', 0], ['PRIOH157357', 0], ['PRIOH157560-1', 0], ['PRIOH157560-2', 0], ['PRIOH157596-1', 0], ['PRIOH157596-2', 0], ['PRIOH157747', 0], ['PRIOH158173', 0], ['PRIOH158563', 0], ['PRIOH158812', 0], ['PRIOH158821', 0], ['PRIOH158984-1', 0], ['PRIOH158984-2', 0], ['PRIOH159331', 0], ['PRIOH159513', 0], ['PRIOH159940', 0], ['PRIOH160668', 0], ['PRIOH161627', 0], ['PRIOH161783', 0], ['PRIOH161865', 0], ['PRIOH161869', 0], ['PRIOH162006', 0], ['PRIOH162271-1', 0], ['PRIOH162271-2', 0], ['PRIOH162271-3', 0], ['PRIOH162622-1', 0], ['PRIOH162622-2', 0], ['PRIOH162622-3', 0], ['PRIOH163297-1', 0], ['PRIOH163297-2', 0], ['PRIOH163821', 0], ['PRIOH164266', 0], ['PRIOH164279', 0], ['PRIOH164319-1', 0], ['PRIOH164319-2', 0], ['PRIOH164932-1', 0], ['PRIOH164932-2', 0], ['PRIOH164958-1', 0], ['PRIOH164958-2', 0], ['PRIOH166491', 0], ['PRIOH166627', 0], ['PRIOH166738', 0], ['PRIOH166914-1', 0], ['PRIOH166914-2', 0], ['PRIOH167372', 0], ['PRIOH167384-1', 0], ['PRIOH167384-2', 0], ['PRIOH167891-1', 0], ['PRIOH167891-2', 0], ['PRIOH167937', 0], ['PRIOH167937-3', 0], ['PRIOH168041', 0], ['PRIOH169297', 0], ['PRIOH169641', 0], ['PRIOH169950', 0], ['PRIOH170221', 0], ['PRIOH170352-1', 0], ['PRIOH170352-2', 0], ['PRIOH170568', 0], ['PRIOH170670', 0], ['PRIOH170800', 0], ['PRIOH171020', 0], ['PRIOH171281-1', 0], ['PRIOH171281-2', 0], ['PRIOH172400', 0], ['PRIOH172447-1', 0], ['PRIOH172447-2', 0], ['PRIOH172447-3', 0], ['PRIOH173589', 0], ['PRIOH173630-1', 0], ['PRIOH173630-2', 0], ['PRIOH173775-1', 0], ['PRIOH173775-2', 0], ['PRIOH173819', 0], ['PRIOH174179', 0], ['PRIOH174404', 0], ['PRIOH174829-1', 0], ['PRIOH174829-2', 0], ['PRIOH174898', 0], ['PRIOH174943', 0], ['PRIOH175164', 0], ['PRIOH175505-1', 0], ['PRIOH175505-2', 0], ['PRIOH175959', 0], ['PRIOH176605', 0], ['PRIOH176848-1', 0], ['PRIOH176848-2', 0], ['PRIOH177194-1', 0], ['PRIOH177194-2', 0], ['PRIOH177429-1', 0], ['PRIOH177429-2', 0], ['PRIOH177582-1', 0], ['PRIOH177582-2', 0], ['PRIOH178061', 0], ['PRIOH178681', 0], ['PRIOH179769-1', 0], ['PRIOH179769-2', 0], ['PRIOH180696', 0], ['PRIOH181758-1', 0], ['PRIOH181758-2', 0], ['PRIOH181758-3', 0], ['PRIOH182182', 0], ['PRIOH182183-1', 0], ['PRIOH182183-2', 0], ['PRIOH182289-1', 0], ['PRIOH182289-2', 0], ['PRIOH182569', 0], ['PRIOH182583', 0], ['PRIOH182729', 0], ['PRIOH182767', 0], ['PRIOH183383', 0], ['PRIOH184508', 0], ['PRIOH184666', 0], ['PRIOH185714', 0], ['PRIOH185739', 0], ['PRIOH185835', 0], ['PRIOH186036', 0], ['PRIOH186562-1', 0], ['PRIOH186562-2', 0], ['PRIOH187086', 0], ['PRIOH187390-1', 0], ['PRIOH187390-2', 0], ['PRIOH187755', 0], ['PRIOH189476', 0], ['PRIOH189720-1', 0], ['PRIOH189720-2', 0], ['PRIOH190451', 0], ['PRIOH191495-1', 0], ['PRIOH191495-2', 0], ['PRIOH191510-1', 0], ['PRIOH191510-2', 0], ['PRIOH192408', 0], ['PRIOH192798', 0], ['PRIOH192798-3', 0], ['PRIOH192808', 0], ['PRIOH192875-1', 0], ['PRIOH192875-2', 0], ['PRIOH193571', 0], ['PRIOH194196-1', 0], ['PRIOH194196-2', 0], ['PRIOH194462', 0], ['PRIOH195077', 0], ['PRIOH195923-1', 0], ['PRIOH195923-2', 0], ['PRIOH196247', 0], ['PRIOH196321', 0], ['PRIOH197265', 0], ['PRIOH197565-1', 0], ['PRIOH197565-2', 0], ['PRIOH197642-1', 0], ['PRIOH197642-2', 0], ['PRIOH197642-3', 0], ['PRIOH198558', 0], ['PRIOH198834-1', 0], ['PRIOH198834-2', 0], ['PRIOH199326', 0], ['PRIOH199388', 0], ['PRIOH199707-1', 0], ['PRIOH199707-2', 0], ['PRIOH199745', 0], ['PRIOH200146', 0], ['PRIOH201002', 0], ['PRIOH202154', 0], ['PRIOH203425', 0], ['PRIOH203666-1', 0], ['PRIOH203666-2', 0], ['PRIOH203682', 0], ['PRIOH203682-2', 0], ['PRIOH203682-3', 0], ['PRIOH203727', 0], ['PRIOH204560-1', 0], ['PRIOH204927-1', 0], ['PRIOH204927-2', 0], ['PRIOH205061', 0], ['PRIOH205771', 0], ['PRIOH205950', 0], ['PRIOH206108', 0], ['PRIOH206193', 0], ['PRIOH206360', 0], ['PRIOH206786', 0], ['PRIOH207090', 0], ['PRIOH208217', 0], ['PRIOH208257', 0], ['PRIOH210262', 0], ['PRIOH210758', 0], ['PRIOH210977-1', 0], ['PRIOH210977-2', 0], ['PRIOH211258', 0], ['PRIOH211333-1', 0], ['PRIOH211333-2', 0], ['PRIOH211333-3', 0], ['PRIOH211399', 0], ['PRIOH211950', 0], ['PRIOH212784', 0], ['PRIOH213059', 0], ['PRIOH213413', 0], ['PRIOH214462', 0], ['PRIOH214883', 0], ['PRIOH215292-1', 0], ['PRIOH215292-2', 0], ['PRIOH215292-3', 0], ['PRIOH215292-4', 0], ['PRIOH216447', 0], ['PRIOH216631-1', 0], ['PRIOH216631-2', 0], ['PRIOH216921', 0], ['PRIOH217237', 0], ['PRIOH217399', 0], ['PRIOH217464', 0], ['PRIOH218712', 0], ['PRIOH218876', 0], ['PRIOH219116', 0], ['PRIOH219582', 0], ['PRIOH220390', 0], ['PRIOH220812-1', 0], ['PRIOH220812-2', 0], ['PRIOH221184', 0], ['PRIOH221385', 0], ['PRIOH221679', 0], ['PRIOH222139', 0], ['PRIOH223439', 0], ['PRIOH224021-1', 0], ['PRIOH224021-2', 0], ['PRIOH224021-3', 0], ['PRIOH225089', 0], ['PRIOH225119', 0], ['PRIOH225524', 0], ['PRIOH225526', 0], ['PRIOH225794-1', 0], ['PRIOH225794-2', 0], ['PRIOH226536', 0], ['PRIOH226955-1', 0], ['PRIOH226955-2', 0], ['PRIOH227236', 0], ['PRIOH227375-1', 0], ['PRIOH227375-2', 0], ['PRIOH227413', 0], ['PRIOH227464', 0], ['PRIOH227575-1', 0], ['PRIOH227575-2', 0], ['PRIOH229066', 0], ['PRIOH229186', 0], ['PRIOH229254', 0], ['PRIOH229874', 0], ['PRIOH230726-1', 0], ['PRIOH230726-2', 0], ['PRIOH230805', 0], ['PRIOH231109', 0], ['PRIOH231237-1', 0], ['PRIOH231237-2', 0], ['PRIOH231559-1', 0], ['PRIOH231559-2', 0], ['PRIOH231711', 0], ['PRIOH232146', 0], ['PRIOH233115', 0], ['PRIOH233201', 0], ['PRIOH233227-1', 0], ['PRIOH233227-2', 0], ['PRIOH233841', 0], ['PRIOH233887', 0], ['PRIOH234585', 0], ['PRIOH234606-1', 0], ['PRIOH234606-2', 0], ['PRIOH234925', 0], ['PRIOH234971', 0], ['PRIOH235330', 0], ['PRIOH235365', 0], ['PRIOH236125', 0], ['PRIOH236164', 0], ['PRIOH236190', 0], ['PRIOH236573-1', 0], ['PRIOH236573-2', 0], ['PRIOH237006', 0], ['PRIOH237333', 0], ['PRIOH237387-1', 0], ['PRIOH237387-2', 0], ['PRIOH237735', 0], ['PRIOH238533', 0], ['PRIOH239107-1', 0], ['PRIOH239107-2', 0], ['PRIOH239107-3', 0], ['PRIOH239832', 0], ['PRIOH240278', 0], ['PRIOH240457', 0], ['PRIOH243418', 0], ['PRIOH243707', 0], ['PRIOH244158-1', 0], ['PRIOH244158-2', 0], ['PRIOH244162', 0], ['PRIOH244376', 0], ['PRIOH244900-1', 0], ['PRIOH244900-2', 0], ['PRIOH245618-1', 0], ['PRIOH245618-2', 0], ['PRIOH245936', 0], ['PRIOH246237', 0], ['PRIOH246347-1', 0], ['PRIOH246347-2', 0], ['PRIOH246933', 0], ['PRIOH247150', 0], ['PRIOH247714', 0], ['PRIOH247722', 0], ['PRIOH248185', 0], ['PRIOH248255', 0], ['PRIOH248331', 0], ['PRIOH248923', 0], ['PRIOH249521', 0], ['PRIOH249611', 0], ['PRIOH250097-1', 0], ['PRIOH250097-2', 0], ['PRIOH250173', 0], ['PRIOH250962', 0], ['PRIOH251005', 0], ['PRIOH251489', 0], ['PRIOH251595', 0], ['PRIOH251688', 0], ['PRIOH252173-1', 0], ['PRIOH252173-2', 0], ['PRIOH252239-1', 0], ['PRIOH252239-2', 0], ['PRIOH252999', 0], ['PRIOH254333-1', 0], ['PRIOH254333-2', 0], ['PRIOH254387-1', 0], ['PRIOH254387-2', 0], ['PRIOH255002', 0], ['PRIOH255557', 0], ['PRIOH255764', 0], ['PRIOH257302', 0], ['PRIOH257692', 0], ['PRIOH257718', 0], ['PRIOH258020', 0], ['PRIOH258520', 0], ['PRIOH258915', 0], ['PRIOH259164', 0], ['PRIOH259490-1', 0], ['PRIOH259490-2', 0], ['PRIOH259553', 0], ['PRIOH259991', 0], ['PRIOH260045', 0], ['PRIOH260112', 0], ['PRIOH260270', 0], ['PRIOH260622', 0], ['PRIOH260988', 0], ['PRIOH261390-1', 0], ['PRIOH261390-2', 0], ['PRIOH261834', 0], ['PRIOH262594', 0], ['PRIOH263250', 0], ['PRIOH263316-1', 0], ['PRIOH263316-2', 0], ['PRIOH26369', 0], ['PRIOH26370', 0], ['PRIOH26371', 0], ['PRIOH26372', 0], ['PRIOH26373', 0], ['PRIOH26374', 0], ['PRIOH26375', 0], ['PRIOH26376', 0], ['PRIOH26377', 0], ['PRIOH26378', 0], ['PRIOH26379', 0], ['PRIOH26380', 0], ['PRIOH26381', 0], ['PRIOH26382', 0], ['PRIOH26383', 0], ['PRIOH264331', 0], ['PRIOH264545', 0], ['PRIOH264810', 0], ['PRIOH265448', 0], ['PRIOH26591', 0], ['PRIOH2674801', 0], ['PRIOH267646', 0], ['PRIOH268001', 0], ['PRIOH268122', 0], ['PRIOH268527-1', 0], ['PRIOH268527-2', 0], ['PRIOH268949', 0], ['PRIOH269194', 0], ['PRIOH269662', 0], ['PRIOH269762', 0], ['PRIOH269872', 0], ['PRIOH270697', 0], ['PRIOH2708433', 0], ['PRIOH272846', 0], ['PRIOH273047', 0], ['PRIOH273159', 0], ['PRIOH273938', 0], ['PRIOH273958-1', 0], ['PRIOH273958-2', 0], ['PRIOH273958-3', 0], ['PRIOH274378-1', 0], ['PRIOH274378-2', 0], ['PRIOH274625', 0], ['PRIOH27478', 0], ['PRIOH27493', 0], ['PRIOH274954', 0], ['PRIOH27497', 0], ['PRIOH27498', 0], ['PRIOH27499', 0], ['PRIOH27500', 0], ['PRIOH27501', 0], ['PRIOH27502', 0], ['PRIOH27503', 0], ['PRIOH275033', 0], ['PRIOH275907', 0], ['PRIOH276357', 0], ['PRIOH276483-1', 0], ['PRIOH276483-2', 0], ['PRIOH276679', 0], ['PRIOH279757', 0], ['PRIOH280273', 0], ['PRIOH281090', 0], ['PRIOH281782', 0], ['PRIOH282730', 0], ['PRIOH283204', 0], ['PRIOH283336', 0], ['PRIOH284353', 0], ['PRIOH284353-1', 0], ['PRIOH284466', 0], ['PRIOH28539', 0], ['PRIOH28540', 0], ['PRIOH286346', 0], ['PRIOH286612', 0], ['PRIOH286695', 0], ['PRIOH286936', 0], ['PRIOH28770', 0], ['PRIOH28771', 0], ['PRIOH28772', 0], ['PRIOH28774', 0], ['PRIOH287936', 0], ['PRIOH287960', 0], ['PRIOH288557', 0], ['PRIOH288664', 0], ['PRIOH288749', 0], ['PRIOH28921', 0], ['PRIOH28924', 0], ['PRIOH28928', 0], ['PRIOH28930', 0], ['PRIOH28932', 0], ['PRIOH28934', 0], ['PRIOH28936', 0], ['PRIOH28937', 0], ['PRIOH28938', 0], ['PRIOH28939', 0], ['PRIOH28940', 0], ['PRIOH28941', 0], ['PRIOH28942', 0], ['PRIOH28943', 0], ['PRIOH28944', 0], ['PRIOH28945', 0], ['PRIOH28946', 0], ['PRIOH28947', 0], ['PRIOH28948', 0], ['PRIOH289722', 0], ['PRIOH289845', 0], ['PRIOH290030', 0], ['PRIOH290284', 0], ['PRIOH290490', 0], ['PRIOH290907', 0], ['PRIOH291339', 0], ['PRIOH29166', 0], ['PRIOH29168', 0], ['PRIOH29171', 0], ['PRIOH29173', 0], ['PRIOH29175', 0], ['PRIOH29177', 0], ['PRIOH29178', 0], ['PRIOH29179', 0], ['PRIOH29180', 0], ['PRIOH29181', 0], ['PRIOH29182', 0], ['PRIOH29183', 0], ['PRIOH29184', 0], ['PRIOH29185', 0], ['PRIOH29186', 0], ['PRIOH292059', 0], ['PRIOH292140', 0], ['PRIOH292194-1', 0], ['PRIOH292194-2', 0], ['PRIOH292277', 0], ['PRIOH293247', 0], ['PRIOH2934002', 0], ['PRIOH293555', 0], ['PRIOH293639', 0], ['PRIOH29366', 0], ['PRIOH29368', 0], ['PRIOH29370', 0], ['PRIOH29372', 0], ['PRIOH29374', 0], ['PRIOH29376', 0], ['PRIOH29377', 0], ['PRIOH29379', 0], ['PRIOH29381', 0], ['PRIOH29383', 0], ['PRIOH29385', 0], ['PRIOH29386', 0], ['PRIOH29388', 0], ['PRIOH29390', 0], ['PRIOH29392', 0], ['PRIOH29394', 0], ['PRIOH29396', 0], ['PRIOH29398', 0], ['PRIOH29400', 0], ['PRIOH29402', 0], ['PRIOH29404', 0], ['PRIOH29406', 0], ['PRIOH29408', 0], ['PRIOH29410', 0], ['PRIOH29412', 0], ['PRIOH29414', 0], ['PRIOH29416', 0], ['PRIOH29420', 0], ['PRIOH294578', 0], ['PRIOH294623', 0], ['PRIOH294883', 0], ['PRIOH294992', 0], ['PRIOH295043', 0], ['PRIOH295707', 0], ['PRIOH29580', 0], ['PRIOH29581', 0], ['PRIOH29583', 0], ['PRIOH296073', 0], ['PRIOH296405', 0], ['PRIOH296448', 0], ['PRIOH296643', 0], ['PRIOH297935', 0], ['PRIOH298341', 0], ['PRIOH299515-1', 0], ['PRIOH299515-2', 0], ['PRIOH300741', 0], ['PRIOH300998', 0], ['PRIOH301316', 0], ['PRIOH302785', 0], ['PRIOH302982', 0], ['PRIOH303178', 0], ['PRIOH303665', 0], ['PRIOH304417', 0], ['PRIOH304509', 0], ['PRIOH304605', 0], ['PRIOH304669', 0], ['PRIOH305381', 0], ['PRIOH306605', 0], ['PRIOH308511', 0], ['PRIOH308886', 0], ['PRIOH309567', 0], ['PRIOH310162', 0], ['PRIOH310326', 0], ['PRIOH311704', 0], ['PRIOH312559', 0], ['PRIOH313053', 0], ['PRIOH313859', 0], ['PRIOH314164', 0], ['PRIOH315829', 0], ['PRIOH315996', 0], ['PRIOH316353', 0], ['PRIOH316448', 0], ['PRIOH317083', 0], ['PRIOH317084', 0], ['PRIOH317225', 0], ['PRIOH317776', 0], ['PRIOH317780', 0], ['PRIOH319171', 0], ['PRIOH31933', 0], ['PRIOH31934', 0], ['PRIOH31935', 0], ['PRIOH31936', 0], ['PRIOH31937', 0], ['PRIOH319424', 0], ['PRIOH31944', 0], ['PRIOH31949', 0], ['PRIOH31951', 0], ['PRIOH31952', 0], ['PRIOH31953', 0], ['PRIOH319601', 0], ['PRIOH320365', 0], ['PRIOH320753', 0], ['PRIOH320905', 0], ['PRIOH322474', 0], ['PRIOH322901-1', 0], ['PRIOH322901-2', 0], ['PRIOH323384', 0], ['PRIOH323917', 0], ['PRIOH324381', 0], ['PRIOH326078', 0], ['PRIOH326639', 0], ['PRIOH326654', 0], ['PRIOH327072', 0], ['PRIOH327630', 0], ['PRIOH328502', 0], ['PRIOH3313204-1', 0], ['PRIOH3313204-2', 0], ['PRIOH3313205', 0], ['PRIOH3313206', 0], ['PRIOH331403', 0], ['PRIOH331512', 0], ['PRIOH331881', 0], ['PRIOH332657', 0], ['PRIOH333269', 0], ['PRIOH343196', 0], ['PRIOH343197', 0], ['PRIOH343198', 0], ['PRIOH343199', 0], ['PRIOH343200', 0], ['PRIOH343206', 0], ['PRIOH343208', 0], ['PRIOH343209', 0], ['PRIOH343211', 0], ['PRIOH343212', 0], ['PRIOH343213', 0], ['PRIOH343214', 0], ['PRIOH343216', 0], ['PRIOH343217', 0], ['PRIOH343218', 0], ['PRIOH343219', 0], ['PRIOH343223', 0], ['PRIOH343227', 0], ['PRIOH343228', 0], ['PRIOH3433201', 0], ['PRIOH343611', 0], ['PRIOH343612', 0], ['PRIOH343613', 0], ['PRIOH343614', 0], ['PRIOH343618', 0], ['PRIOH343619', 0], ['PRIOH343620', 0], ['PRIOH343621', 0], ['PRIOH343622', 0], ['PRIOH343623', 0], ['PRIOH343633', 0], ['PRIOH343648', 0], ['PRIOH343651', 0], ['PRIOH343652', 0], ['PRIOH343655', 0], ['PRIOH343656', 0], ['PRIOH343658', 0], ['PRIOH343659', 0], ['PRIOH343660', 0], ['PRIOH343661', 0], ['PRIOH343662', 0], ['PRIOH343663', 0], ['PRIOH343664', 0], ['PRIOH343665', 0], ['PRIOH343666', 0], ['PRIOH343667', 0], ['PRIOH343668', 0], ['PRIOH343669', 0], ['PRIOH343670', 0], ['PRIOH343671', 0], ['PRIOH343672', 0], ['PRIOH343673', 0], ['PRIOH343674', 0], ['PRIOH343675', 0], ['PRIOH343676', 0], ['PRIOH343677', 0], ['PRIOH343678', 0], ['PRIOH343679', 0], ['PRIOH343680', 0], ['PRIOH343681', 0], ['PRIOH343682', 0], ['PRIOH343683', 0], ['PRIOH343684', 0], ['PRIOH343685', 0], ['PRIOH343686', 0], ['PRIOH343687', 0], ['PRIOH343689', 0], ['PRIOH343690', 0], ['PRIOH343691', 0], ['PRIOH343692', 0], ['PRIOH343693', 0], ['PRIOH343694', 0], ['PRIOH343695', 0], ['PRIOH343696', 0], ['PRIOH343697', 0], ['PRIOH343698', 0], ['PRIOH343699', 0], ['PRIOH343700', 0], ['PRIOH343701', 0], ['PRIOH344056', 0], ['PRIOH344058', 0], ['PRIOH344059', 0], ['PRIOH344060', 0], ['PRIOH344061', 0], ['PRIOH344062', 0], ['PRIOH344067', 0], ['PRIOH344068', 0], ['PRIOH344069', 0], ['PRIOH344070', 0], ['PRIOH344071', 0], ['PRIOH344072', 0], ['PRIOH344073', 0], ['PRIOH344074', 0], ['PRIOH344076', 0], ['PRIOH344077', 0], ['PRIOH344078', 0], ['PRIOH344079', 0], ['PRIOH344080', 0], ['PRIOH344085', 0], ['PRIOH344086', 0], ['PRIOH344087', 0], ['PRIOH344095', 0], ['PRIOH344096', 0], ['PRIOH344099', 0], ['PRIOH344100', 0], ['PRIOH344106', 0], ['PRIOH353417', 0], ['PRIOH353630', 0], ['PRIOH354050', 0], ['PRIOH354263', 0], ['PRIOH377585', 0], ['PRIOH391521', 0], ['PRIOH455633', 0], ['PRIOH455634', 0], ['PRIOH455635', 0], ['PRIOH455636', 0], ['PRIOH45735', 0], ['PRIOH45736', 0], ['PRIOH45737', 0], ['PRIOH45745', 0], ['PRIOH45747', 0], ['PRIOH45854', 0], ['PRIOH45855', 0], ['PRIOH45856', 0], ['PRIOH45857', 0], ['PRIOH45858', 0], ['PRIOH45859', 0], ['PRIOH45860', 0], ['PRIOH45861', 0], ['PRIOH45862', 0], ['PRIOH45863', 0], ['PRIOH45864', 0], ['PRIOH45865', 0], ['PRIOH45866', 0], ['PRIOH45867', 0], ['PRIOH45868', 0], ['PRIOH45869', 0], ['PRIOH45870', 0], ['PRIOH45871', 0], ['PRIOH45979', 0], ['PRIOH45980', 0], ['PRIOH45981', 0], ['PRIOH45982', 0], ['PRIOH45983', 0], ['PRIOH45984', 0], ['PRIOH45985', 0], ['PRIOH45986', 0], ['PRIOH45987', 0], ['PRIOH45988', 0], ['PRIOH45989', 0], ['PRIOH45990', 0], ['PRIOH45991', 0], ['PRIOH45992', 0], ['PRIOH45993', 0], ['PRIOH45994', 0], ['PRIOH45995', 0], ['PRIOH45996', 0], ['PRIOH45997', 0], ['PRIOH45998', 0], ['PRIOH45999', 0], ['PRIOH46000', 0], ['PRIOH46001', 0], ['PRIOH46002', 0], ['PRIOH46003', 0], ['PRIOH46207', 0], ['PRIOH46208', 0], ['PRIOH46209', 0], ['PRIOH46210', 0], ['PRIOH46211', 0], ['PRIOH46212', 0], ['PRIOH46213', 0], ['PRIOH46214', 0], ['PRIOH46215', 0], ['PRIOH46216', 0], ['PRIOH46217', 0], ['PRIOH46218', 0], ['PRIOH46219', 0], ['PRIOH46220', 0], ['PRIOH46221', 0], ['PRIOH46222', 0], ['PRIOH46223', 0], ['PRIOH46224', 0], ['PRIOH46225', 0], ['PRIOH46226', 0], ['PRIOH46227', 0], ['PRIOH46228', 0], ['PRIOH46229', 0], ['PRIOH46230', 0], ['PRIOH46231', 0], ['PRIOH46232', 0], ['PRIOH46233', 0], ['PRIOH46234', 0], ['PRIOH46235', 0], ['PRIOH46236', 0], ['PRIOH46237', 0], ['PRIOH46238', 0], ['PRIOH46239', 0], ['PRIOH46240', 0], ['PRIOH46241', 0], ['PRIOH46242', 0], ['PRIOH46243', 0], ['PRIOH46244', 0], ['PRIOH46245', 0], ['PRIOH46246', 0], ['PRIOH46247', 0], ['PRIOH46248', 0], ['PRIOH46660', 0], ['PRIOH46661', 0], ['PRIOH46662', 0], ['PRIOH46664', 0], ['PRIOH46665', 0], ['PRIOH46666', 0], ['PRIOH46667', 0], ['PRIOH46668', 0], ['PRIOH46669', 0], ['PRIOH46670', 0], ['PRIOH46671', 0], ['PRIOH46672', 0], ['PRIOH46673', 0], ['PRIOH46674', 0], ['PRIOH46675', 0], ['PRIOH46676', 0], ['PRIOH46866', 0], ['PRIOH46867', 0], ['PRIOH46868', 0], ['PRIOH46870', 0], ['PRIOH46877', 0], ['PRIOH46878', 0], ['PRIOH46879', 0], ['PRIOH46880', 0], ['PRIOH46881', 0], ['PRIOH46882', 0], ['PRIOH46894', 0], ['PRIOH46902', 0], ['PRIOH47160', 0], ['PRIOH47161', 0], ['PRIOH47162', 0], ['PRIOH47165', 0], ['PRIOH47184', 0], ['PRIOH47185', 0], ['PRIOH47186', 0], ['PRIOH47440', 0], ['PRIOH47441', 0], ['PRIOH47442', 0], ['PRIOH47443', 0], ['PRIOH47444', 0], ['PRIOH47445', 0], ['PRIOH47446', 0], ['PRIOH47447', 0], ['PRIOH47448', 0], ['PRIOH47449', 0], ['PRIOH47450', 0], ['PRIOH47451', 0], ['PRIOH47452', 0], ['PRIOH47453', 0], ['PRIOH47454', 0], ['PRIOH47455', 0], ['PRIOH47456', 0], ['PRIOH47457', 0], ['PRIOH47458', 0], ['PRIOH47459', 0], ['PRIOH47460', 0], ['PRIOH47461', 0], ['PRIOH47462', 0], ['PRIOH47463', 0], ['PRIOH47464', 0], ['PRIOH47465', 0], ['PRIOH47466', 0], ['PRIOH47467', 0], ['PRIOH47468', 0], ['PRIOH47469', 0], ['PRIOH47470', 0], ['PRIOH47471', 0], ['PRIOH47472', 0], ['PRIOH47474', 0], ['PRIOH47475', 0], ['PRIOH47476', 0], ['PRIOH47477', 0], ['PRIOH47479', 0], ['PRIOH47480', 0], ['PRIOH47484', 0], ['PRIOH47485', 0], ['PRIOH47486', 0], ['PRIOH47487', 0], ['PRIOH47491', 0], ['PRIOH47492', 0], ['PRIOH47493', 0], ['PRIOH47494', 0], ['PRIOH47495', 0], ['PRIOH47500', 0], ['PRIOH47501', 0], ['PRIOH47502', 0], ['PRIOH47503', 0], ['PRIOH47504', 0], ['PRIOH47506', 0], ['PRIOH47507', 0], ['PRIOH47508', 0], ['PRIOH47509', 0], ['PRIOH47773', 0], ['PRIOH47774', 0], ['PRIOH47775', 0], ['PRIOH47776', 0], ['PRIOH47777', 0], ['PRIOH47778', 0], ['PRIOH47779', 0], ['PRIOH47780', 0], ['PRIOH47781', 0], ['PRIOH47782', 0], ['PRIOH47783', 0], ['PRIOH47784', 0], ['PRIOH47785', 0], ['PRIOH47786', 0], ['PRIOH47787', 0], ['PRIOH47788', 0], ['PRIOH47789', 0], ['PRIOH47790', 0], ['PRIOH47791', 0], ['PRIOH47792', 0], ['PRIOH47927', 0], ['PRIOH47934', 0], ['PRIOH47936', 0], ['PRIOH47937', 0], ['PRIOH47938', 0], ['PRIOH47939', 0], ['PRIOH47940', 0], ['PRIOH47941', 0], ['PRIOH47942', 0], ['PRIOH47943', 0], ['PRIOH47945', 0], ['PRIOH47946', 0], ['PRIOH47947', 0], ['PRIOH47948', 0], ['PRIOH47949', 0], ['PRIOH47950', 0], ['PRIOH47951', 0], ['PRIOH47952', 0], ['PRIOH47953', 0], ['PRIOH47954', 0], ['PRIOH47955', 0], ['PRIOH47956', 0], ['PRIOH48132', 0], ['PRIOH48133', 0], ['PRIOH48135', 0], ['PRIOH48136', 0], ['PRIOH48137', 0], ['PRIOH48138', 0], ['PRIOH48139', 0], ['PRIOH48140', 0], ['PRIOH48141', 0], ['PRIOH48166', 0], ['PRIOH48169', 0], ['PRIOH48171', 0], ['PRIOH48173', 0], ['PRIOH48175', 0], ['PRIOH48177', 0], ['PRIOH48179', 0], ['PRIOH48181', 0], ['PRIOH48183', 0], ['PRIOH48185', 0], ['PRIOH48187', 0], ['PRIOH48189', 0], ['PRIOH48191', 0], ['PRIOH48193', 0], ['PRIOH48195', 0], ['PRIOH48197', 0], ['PRIOH48199', 0], ['PRIOH48201', 0], ['PRIOH48203', 0], ['PRIOH48205', 0], ['PRIOH48207', 0], ['PRIOH48209', 0], ['PRIOH48211', 0], ['PRIOH48213', 0], ['PRIOH48215', 0], ['PRIOH48375', 0], ['PRIOH48377', 0], ['PRIOH48379', 0], ['PRIOH48381', 0], ['PRIOH48382', 0], ['PRIOH48393', 0], ['PRIOH48432', 0], ['PRIOH48433', 0], ['PRIOH48434', 0], ['PRIOH48435', 0], ['PRIOH48436', 0], ['PRIOH48437', 0], ['PRIOH48438', 0], ['PRIOH48439', 0], ['PRIOH48440', 0], ['PRIOH48441', 0], ['PRIOH48442', 0], ['PRIOH48443', 0], ['PRIOH48483', 0], ['PRIOH48484', 0], ['PRIOH48485', 0], ['PRIOH48486', 0], ['PRIOH48487', 0], ['PRIOH48488', 0], ['PRIOH48489', 0], ['PRIOH48490', 0], ['PRIOH48491', 0], ['PRIOH48492', 0], ['PRIOH48493', 0], ['PRIOH48494', 0], ['PRIOH48495', 0], ['PRIOH48496', 0], ['PRIOH48497', 0], ['PRIOH48498', 0], ['PRIOH48499', 0], ['PRIOH48500', 0], ['PRIOH48502', 0], ['PRIOH48503', 0], ['PRIOH48596', 0], ['PRIOH48597', 0], ['PRIOH48598', 0], ['PRIOH48599', 0], ['PRIOH48600', 0], ['PRIOH48601', 0], ['PRIOH48749', 0], ['PRIOH48750', 0], ['PRIOH48751', 0], ['PRIOH48752', 0], ['PRIOH48754', 0], ['PRIOH48755', 0], ['PRIOH48757', 0], ['PRIOH48758', 0], ['PRIOH48759', 0], ['PRIOH48764', 0], ['PRIOH48847', 0], ['PRIOH48848', 0], ['PRIOH48849', 0], ['PRIOH48850', 0], ['PRIOH48851', 0], ['PRIOH48852', 0], ['PRIOH48853', 0], ['PRIOH48854', 0], ['PRIOH48855', 0], ['PRIOH48856', 0], ['PRIOH48857', 0], ['PRIOH48858', 0], ['PRIOH48859', 0], ['PRIOH48860', 0], ['PRIOH48861', 0], ['PRIOH48862', 0], ['PRIOH48863', 0], ['PRIOH48864', 0], ['PRIOH48865', 0], ['PRIOH48866', 0], ['PRIOH48867', 0], ['PRIOH48868', 0], ['PRIOH49025', 0], ['PRIOH49034', 0], ['PRIOH49035', 0], ['PRIOH49039', 0], ['PRIOH49040', 0], ['PRIOH49041', 0], ['PRIOH49042', 0], ['PRIOH49043', 0], ['PRIOH49044', 0], ['PRIOH49045', 0], ['PRIOH49047', 0], ['PRIOH49048', 0], ['PRIOH49049', 0], ['PRIOH49050', 0], ['PRIOH49051', 0], ['PRIOH49052', 0], ['PRIOH49053', 0], ['PRIOH49054', 0], ['PRIOH49055', 0], ['PRIOH49056', 0], ['PRIOH49057', 0], ['PRIOH49058', 0], ['PRIOH49059', 0], ['PRIOH49060', 0], ['PRIOH49061', 0], ['PRIOH49062', 0], ['PRIOH49063', 0], ['PRIOH49064', 0], ['PRIOH49065', 0], ['PRIOH49066', 0], ['PRIOH49067', 0], ['PRIOH49068', 0], ['PRIOH49069', 0], ['PRIOH49070', 0], ['PRIOH49071', 0], ['PRIOH49072', 0], ['PRIOH49073', 0], ['PRIOH49074', 0], ['PRIOH49076', 0], ['PRIOH49077', 0], ['PRIOH49078', 0], ['PRIOH49079', 0], ['PRIOH49080', 0], ['PRIOH49081', 0], ['PRIOH49082', 0], ['PRIOH49083', 0], ['PRIOH49084', 0], ['PRIOH49085', 0], ['PRIOH49086', 0], ['PRIOH49087', 0], ['PRIOH49088', 0], ['PRIOH49089', 0], ['PRIOH49090', 0], ['PRIOH49091', 0], ['PRIOH49200', 0], ['PRIOH49201', 0], ['PRIOH49202', 0], ['PRIOH49203', 0], ['PRIOH49204', 0], ['PRIOH49205', 0], ['PRIOH49206', 0], ['PRIOH49933', 0], ['PRIOH49934', 0], ['PRIOH49935', 0], ['PRIOH49936', 0], ['PRIOH49937', 0], ['PRIOH49938', 0], ['PRIOH49939', 0], ['PRIOH49940', 0], ['PRIOH49941', 0], ['PRIOH49943', 0], ['PRIOH49944', 0], ['PRIOH49945', 0], ['PRIOH49951', 0], ['PRIOH49958', 0], ['PRIOH49959', 0], ['PRIOH49960', 0], ['PRIOH49961', 0], ['PRIOH50143', 0], ['PRIOH50144', 0], ['PRIOH50145', 0], ['PRIOH50146', 0], ['PRIOH50147', 0], ['PRIOH50148', 0], ['PRIOH50149', 0], ['PRIOH50150', 0], ['PRIOH50151', 0], ['PRIOH50152', 0], ['PRIOH50153', 0], ['PRIOH50154', 0], ['PRIOH50158', 0], ['PRIOH50159', 0], ['PRIOH50162', 0], ['PRIOH50164', 0], ['PRIOH50166', 0], ['PRIOH50182', 0], ['PRIOH50189', 0], ['PRIOH50190', 0], ['PRIOH50191', 0], ['PRIOH50192', 0], ['PRIOH50193', 0], ['PRIOH50194', 0], ['PRIOH50195', 0], ['PRIOH50196', 0], ['PRIOH50197', 0], ['PRIOH50198', 0], ['PRIOH50199', 0], ['PRIOH50200', 0], ['PRIOH50201', 0], ['PRIOH50202', 0], ['PRIOH50203', 0], ['PRIOH50204', 0], ['PRIOH50205', 0], ['PRIOH50209', 0], ['PRIOH50210', 0], ['PRIOH50211', 0], ['PRIOH50212', 0], ['PRIOH50213', 0], ['PRIOH50214', 0], ['PRIOH50215', 0], ['PRIOH50216', 0], ['PRIOH50217', 0], ['PRIOH50218', 0], ['PRIOH50220', 0], ['PRIOH50221', 0], ['PRIOH50223', 0], ['PRIOH50471', 0], ['PRIOH50472', 0], ['PRIOH50473', 0], ['PRIOH50474', 0], ['PRIOH50475', 0], ['PRIOH50476', 0], ['PRIOH646449', 0], ['PRIOH646450', 0], ['PRIOH649649', 0], ['PRIOH703649', 0], ['PRIOH703650', 0], ['PRIOH786529', 0], ['PRIOH813089', 0], ['PRIOH83855', 0], ['PRIOH84640', 0], ['PRIOH84645', 0], ['PRIOH84646', 0], ['PRIOH84647', 0], ['PRIOH84648', 0], ['PRIOH84649', 0], ['PRIOH84650', 0], ['PRIOH84651', 0], ['PRIOH84652', 0], ['PRIOH84776', 0], ['PRIOH84779', 0], ['PRIOH84790', 0], ['PRIOH84793', 0], ['PRIOH84914', 0], ['PRIOH84915', 0], ['PRIOH85042', 0], ['PRIOH85043', 0], ['PRIOH85044', 0], ['PRIOH85045', 0], ['PRIOH85046', 0], ['PRIOH85113', 0], ['PRIOH85115', 0], ['PRIOH85229', 0], ['PRIOH85398', 0], ['PRIOH85617', 0], ['PRIOH85960', 0], ['PRIOH85979', 0], ['PRIOH86135', 0], ['PRIOH86143', 0], ['PRIOH86221', 0], ['PRIOH86222', 0], ['PRIOH86240', 0], ['PRIOH86329', 0], ['PRIOH86356', 0], ['PRIOH86376', 0], ['PRIOH86420', 0], ['PRIOH86875', 0], ['PRIOH87071', 0], ['PRIOH87128', 0], ['PRIOH87591', 0], ['PRIOH87868', 0], ['PRIOH87983', 0], ['PRIOH87990', 0], ['PRIOH87991', 0], ['PRIOH88072', 0], ['PRIOH88132', 0], ['PRIOH88225', 0], ['PRIOH88273', 0], ['PRIOH88471', 0], ['PRIOH88698', 0], ['PRIOH88702', 0], ['PRIOH88861', 0], ['PRIOH88862', 0], ['PRIOH88897', 0], ['PRIOH89129', 0], ['PRIOH89698', 0], ['PRIOH89863', 0], ['PRIOH89881', 0], ['PRIOH89956', 0], ['PRIOH90165', 0], ['PRIOH90557', 0], ['PRIOH90558', 0], ['PRIOH90559', 0], ['PRIOH90560', 0], ['PRIOH90667', 0], ['PRIOH90699', 0], ['PRIOH90979', 0], ['PRIOH91000', 0], ['PRIOH91279', 0], ['PRIOH91296', 0], ['PRIOH91330', 0], ['PRIOH91387', 0], ['PRIOH91650', 0], ['PRIOH91705', 0], ['PRIOH91757', 0], ['PRIOH91770', 0], ['PRIOH91946', 0], ['PRIOH92354-1', 0], ['PRIOH92354-2', 0], ['PRIOH92503-1', 0], ['PRIOH92503-2', 0], ['PRIOH92788-1', 0], ['PRIOH92788-2', 0], ['PRIOH92788-3', 0], ['PRIOH92827', 0], ['PRIOH92924', 0], ['PRIOH93039', 0], ['PRIOH93043-1', 0], ['PRIOH93043-2', 0], ['PRIOH93043-3', 0], ['PRIOH93043-4', 0], ['PRIOH93091-1', 0], ['PRIOH93091-2', 0], ['PRIOH93091-3', 0], ['PRIOH93091-4', 0], ['PRIOH93193', 0], ['PRIOH93393', 0], ['PRIOH93443', 0], ['PRIOH93732-1', 0], ['PRIOH93732-2', 0], ['PRIOH93732-3', 0], ['PRIOH93732-4', 0], ['PRIOH93732-5', 0], ['PRIOH93769', 0], ['PRIOH93809-1', 0], ['PRIOH93809-2', 0], ['PRIOH93809-3', 0], ['PRIOH93879', 0], ['PRIOH93901-1', 0], ['PRIOH93901-2', 0], ['PRIOH93980', 0], ['PRIOH94082-1', 0], ['PRIOH94082-2', 0], ['PRIOH94353-1', 0], ['PRIOH94353-2', 0], ['PRIOH94353-3', 0], ['PRIOH94353-4', 0], ['PRIOH94353-5', 0], ['PRIOH94353-6', 0], ['PRIOH94353-7', 0], ['PRIOH94353-8', 0], ['PRIOH94542-1', 0], ['PRIOH94542-2', 0], ['PRIOH94542-3', 0], ['PRIOH94692-1', 0], ['PRIOH94692-2', 0], ['PRIOH94740-1', 0], ['PRIOH94740-2', 0], ['PRIOH94878-1', 0], ['PRIOH94878-2', 0], ['PRIOH95120-1', 0], ['PRIOH95120-2', 0], ['PRIOH95120-3', 0], ['PRIOH95120-4', 0], ['PRIOH951809', 0], ['PRIOH95370', 0], ['PRIOH95847', 0], ['PRIOH966081', 0], ['PRIOH96783', 0], ['PRIOH96815-1', 0], ['PRIOH96815-2', 0], ['PRIOH96815-3', 0], ['PRIOH97087-1', 0], ['PRIOH97087-2', 0], ['PRIOH97116-1', 0], ['PRIOH97116-2', 0], ['PRIOH97116-3', 0], ['PRIOH97170', 0], ['PRIOH97266-1', 0], ['PRIOH97266-2', 0], ['PRIOH97273-1', 0], ['PRIOH97273-2', 0], ['PRIOH973233', 0], ['PRIOH973234', 0], ['PRIOH97478-1', 0], ['PRIOH97478-2', 0], ['PRIOH97524-1', 0], ['PRIOH97524-2', 0], ['PRIOH97738-1', 0], ['PRIOH97738-2', 0], ['PRIOH97738-3', 0], ['PRIOH97746-1', 0], ['PRIOH97746-2', 0], ['PRIOH97746-3', 0], ['PRIOH97746-4', 0], ['PRIOH978339-1', 0], ['PRIOH978339-2', 0], ['PRIOH978622', 0], ['PRIOH98330-1', 0], ['PRIOH98330-2', 0], ['PRIOH98330-3', 0], ['PRIOH98330-4', 0], ['PRIOH98330-5', 0], ['PRIOH98330-6', 0], ['PRIOH98393-1', 0], ['PRIOH98393-2', 0], ['PRIOH98471', 0], ['PRIOH98486', 0], ['PRIOH98956', 0], ['PRIOH99003', 0], ['PRIOH99187-1', 0], ['PRIOH99187-2', 0], ['PRIOH99187-3', 0], ['PRIOH99187-4', 0], ['PRIOH99292', 0], ['PRIOH99328', 0], ['PRIOH99590', 0], ['PRIOH99736-1', 0], ['PRIOH99736-2', 0]]
space=[]
space.append(names)
print space
print len(space)
space.append(names)
print space
print len(space)
space.append(names)
print space
print len(space)
print names[0]
print type(names)
exit()

print '1'
exec('X=4+3')
print X
exit()

Xfmrvalue=[['CEDA_WR1', 0], ['CEDA_WR2', 0]]
print Xfmrvalue
print Xfmrvalue[0]
print Xfmrvalue[0][1]
exit()

print range(10,0,-1)
exit()

X=[('CEDA_WR1', 53.029), ('CEDA_WR2', 72.785)]
Y=[1]+X
print Y
exit()

test=[]
test.append([1,2,3,4,5])
test.append([1,2,3,4,5])
test.append([1,2,3,4,5])
test.append([1,2,3,4,5])
test[0][2]=999
print test
print test[0]
print test[0][0]
exit()

def SortingWorst(xfmrStorage, xfmr_byphaseStorage, xfmr_cableStorage):

'''
#SortingWorse is a small function for sorting the loadings by magnitude, seperate storage for ByPhase phase loading storage
'''
#HowMany represents the number of devices examines, 5=values of top 5 worst, 10=values of the top 10 worst
HowMany=5

for val in xfmrStorage:
    #print val
    val.sort(key=takeThird, reverse=True)

if len(xfmrStorage[0]) >= HowMany:
    XfmrStorageTop = [[]] * HowMany
    XfmrNameTop = [[]] * HowMany
    XfmrThingsTop = [[]] * HowMany
else:
    XfmrStorageTop = [[]] * len(xfmrStorage[0])
    XfmrNameTop = [[]] * len(xfmrStorage[0])
    XfmrThingsTop = [[]] * len(xfmrStorage[0])

for i in range(len(XfmrStorageTop)):
    XfmrStorageTop[i]=0

for i in range(len(XfmrStorageTop)):
    for j in range(len(xfmrStorage)):
        XfmrStorageTop[i] = XfmrStorageTop[i] + float(xfmrStorage[j][i][2])
        XfmrNameTop[i]=xfmrStorage[j][i][1]
print(XfmrStorageTop)
print(XfmrNameTop)

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
print(CableStorageTop)
print(CableNameTop)


xfmr_byphaseAStorage=xfmr_byphaseStorage

for val in xfmr_byphaseAStorage:
    #print val
    val.sort(key=takeThird, reverse=True)

PhaseAStorage=[[]]*HowMany
PhaseAName=[[]]*HowMany
for i in range(len(PhaseAStorage)):
    PhaseAStorage[i]=0

for i in range(len(xfmr_byphaseAStorage)+1):
    for j in range(len(xfmr_byphaseAStorage)):

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

for i in range(len(xfmr_byphaseBStorage)+1):
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

for i in range(len(xfmr_byphaseCStorage)+1):
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
print(TopByPhaseStorage)
print(TopByPhaseNames)




return XfmrNameTop,TopByPhaseNames,CableNameTop


def whichVal(val):
    output=0
    print val
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
            print 'lah'
            output = [float(val[4])]
            print output


    return output


print 'what?'
#xfmrStorage, xfmr_byphaseStorage, xfmr_cableStorage=WorstTesting()
XfmrNameTop,TopByPhaseNames,CableNameTop = SortingWorst(xfmrStorage, xfmr_byphaseStorage, xfmr_cableStorage)#, HowMany)
print(XfmrNameTop)
print(CableNameTop)
print(TopByPhaseNames)




one=0
two=0
three=0
four=0
five=0
six=0
seven=0
eight=0
nine=0
ten=0
Total_xfmr=[]
HowMany=3
for i in range(len(xfmrStorage)):
    anotherInt=0
    print 'i'
    print i
    for name in XfmrNameTop:
        for j in range(len(xfmrStorage[i])):
            if xfmrStorage[i][j][1] == name:
                if anotherInt == 0:
                    if one == 0:
                        one = [[float(xfmrStorage[i][j][2])]]
                    else:
                        one.append([float(xfmrStorage[i][j][2])])
                    anotherInt=anotherInt+1
                elif anotherInt == 1 and HowMany >=2:
                    if two == 0:
                        two = [[float(xfmrStorage[i][j][2])]]
                    else:
                        two.append([float(xfmrStorage[i][j][2])])
                    anotherInt = anotherInt + 1
                elif anotherInt == 2 and HowMany >=3:
                    if three == 0:
                        three = [[float(xfmrStorage[i][j][2])]]
                    else:
                        three.append([float(xfmrStorage[i][j][2])])
                    anotherInt = anotherInt + 1
                elif anotherInt == 3 and HowMany >=4:
                    if four == 0:
                        four = [[float(xfmrStorage[i][j][2])]]
                    else:
                        four.append([float(xfmrStorage[i][j][2])])
                    anotherInt=anotherInt+1
                elif anotherInt == 4 and HowMany >=5:
                    if five == 0:
                        five = [[float(xfmrStorage[i][j][2])]]
                    else:
                        five.append([float(xfmrStorage[i][j][2])])
                    anotherInt = anotherInt + 1
                elif anotherInt == 5  and HowMany >=6:
                    if six == 0:
                        six = [[float(xfmrStorage[i][j][2])]]
                    else:
                        six.append([float(xfmrStorage[i][j][2])])
                    anotherInt = anotherInt + 1
                if anotherInt == 6 and HowMany >=7:
                    if seven == 0:
                        seven = [[float(xfmrStorage[i][j][2])]]
                    else:
                        seven.append([float(xfmrStorage[i][j][2])])
                    anotherInt=anotherInt+1
                elif anotherInt == 7 and HowMany >=8:
                    if eight== 0:
                        eight = [[float(xfmrStorage[i][j][2])]]
                    else:
                        eight.append([float(xfmrStorage[i][j][2])])
                    anotherInt = anotherInt + 1
                elif anotherInt == 8 and HowMany >=9:
                    if nine == 0:
                        nine = [[float(xfmrStorage[i][j][2])]]
                    else:
                        nine.append([float(xfmrStorage[i][j][2])])
                    anotherInt = anotherInt + 1
                elif anotherInt == 9 and HowMany >=10:
                    if ten == 0:
                        ten = [[float(xfmrStorage[i][j][2])]]
                    else:
                        ten.append([float(xfmrStorage[i][j][2])])
                    anotherInt = anotherInt + 1
print 'starter 1'
print one
print two
print three
print Total_xfmr
print HowMany
if HowMany >= 1:
    Total_xfmr.append(one)
if HowMany >= 2:
    Total_xfmr.append(two)
if HowMany >= 3:
    Total_xfmr.append(three)
if HowMany >= 4:
    Total_xfmr.append(four)
if HowMany >= 5:
    Total_xfmr.append(five)
if HowMany >= 6:
    Total_xfmr.append(six)
if HowMany >= 7:
    Total_xfmr.append(seven)
if HowMany >= 8:
    Total_xfmr.append(eight)
if HowMany >= 9:
    Total_xfmr.append(nine)
if HowMany >= 10:
    Total_xfmr.append(ten)
print Total_xfmr

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
HowMany = 5

for i in range(len(xfmr_byphaseStorage)):
    anotherInt=0
    print 'i'
    print i
    for name in TopByPhaseNames:
        for j in range(len(xfmr_byphaseStorage[i])):
            if xfmr_byphaseStorage[i][j][1] == name:
                if anotherInt == 0:
                    if one == 0:
                        one = whichVal(xfmr_byphaseStorage[i][j])
                    else:
                        one.append(whichVal(xfmr_byphaseStorage[i][j]))
                    anotherInt = anotherInt + 1

                elif anotherInt == 1 and HowMany >= 2:
                    if two == 0:
                        two = whichVal(xfmr_byphaseStorage[i][j])
                    else:
                        two.append(whichVal(xfmr_byphaseStorage[i][j]))
                    anotherInt = anotherInt + 1
                elif anotherInt == 2 and HowMany >= 3:
                    if three == 0:
                        three = whichVal(xfmr_byphaseStorage[i][j])
                    else:
                        three.append(whichVal(xfmr_byphaseStorage[i][j]))
                    anotherInt = anotherInt + 1
                elif anotherInt == 3 and HowMany >= 4:
                    if four == 0:
                        four = whichVal(xfmr_byphaseStorage[i][j])
                    else:
                        four.append(whichVal(xfmr_byphaseStorage[i][j]))
                    anotherInt = anotherInt + 1
                elif anotherInt == 4 and HowMany >= 5:
                    if five == 0:
                        five = whichVal(xfmr_byphaseStorage[i][j])
                    else:
                        five.append(whichVal(xfmr_byphaseStorage[i][j]))
                    anotherInt = anotherInt + 1
                elif anotherInt == 5 and HowMany >= 6:
                    if six == 0:
                        six = whichVal(xfmr_byphaseStorage[i][j])
                    else:
                        six.append(whichVal(xfmr_byphaseStorage[i][j]))
                    anotherInt = anotherInt + 1
                if anotherInt == 6 and HowMany >= 7:
                    if seven == 0:
                        seven = whichVal(xfmr_byphaseStorage[i][j])
                    else:
                        seven.append(whichVal(xfmr_byphaseStorage[i][j]))
                    anotherInt = anotherInt + 1
                elif anotherInt == 7 and HowMany >= 8:
                    if eight == 0:
                        eight = whichVal(xfmr_byphaseStorage[i][j])
                    else:
                        eight.append(whichVal(xfmr_byphaseStorage[i][j]))
                    anotherInt = anotherInt + 1
                elif anotherInt == 8 and HowMany >= 9:
                    if nine == 0:
                        nine = whichVal(xfmr_byphaseStorage[i][j])
                    else:
                        nine.append(whichVal(xfmr_byphaseStorage[i][j]))
                    anotherInt = anotherInt + 1
                elif anotherInt == 9 and HowMany >= 10:
                    if ten == 0:
                        ten = whichVal(xfmr_byphaseStorage[i][j])
                    else:
                        ten.append(whichVal(xfmr_byphaseStorage[i][j]))
                    anotherInt = anotherInt + 1

print 'starter 2'
print one
print two
print three
print Total_ByPhase

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

one=0
two=0
three=0
four=0
five=0
six=0
seven=0
eight=0
nine=0
ten=0
Total_Cable=[]
HowMany=5
for i in range(len(xfmr_cableStorage)):
    anotherInt=0
    print 'i'
    print i
    for name in CableNameTop:
        for j in range(len(xfmr_cableStorage[i])):
            if xfmr_cableStorage[i][j][1] == name:
                if anotherInt == 0:
                    if one == 0:
                        one = [[float(xfmr_cableStorage[i][j][2])]]
                    else:
                        one.append([float(xfmr_cableStorage[i][j][2])])
                    anotherInt=anotherInt+1
                elif anotherInt == 1 and HowMany >=2:
                    if two == 0:
                        two = [[float(xfmr_cableStorage[i][j][2])]]
                    else:
                        two.append([float(xfmr_cableStorage[i][j][2])])
                    anotherInt = anotherInt + 1
                elif anotherInt == 2 and HowMany >=3:
                    if three == 0:
                        three = [[float(xfmr_cableStorage[i][j][2])]]
                    else:
                        three.append([float(xfmr_cableStorage[i][j][2])])
                    anotherInt = anotherInt + 1
                elif anotherInt == 3 and HowMany >=4:
                    if four == 0:
                        four = [[float(xfmr_cableStorage[i][j][2])]]
                    else:
                        four.append([float(xfmr_cableStorage[i][j][2])])
                    anotherInt=anotherInt+1
                elif anotherInt == 4 and HowMany >=5:
                    if five == 0:
                        five = [[float(xfmr_cableStorage[i][j][2])]]
                    else:
                        five.append([float(xfmr_cableStorage[i][j][2])])
                    anotherInt = anotherInt + 1
                elif anotherInt == 5  and HowMany >=6:
                    if six == 0:
                        six = [[float(xfmr_cableStorage[i][j][2])]]
                    else:
                        six.append([float(xfmr_cableStorage[i][j][2])])
                    anotherInt = anotherInt + 1
                if anotherInt == 6 and HowMany >=7:
                    if seven == 0:
                        seven = [[float(xfmr_cableStorage[i][j][2])]]
                    else:
                        seven.append([float(xfmr_cableStorage[i][j][2])])
                    anotherInt=anotherInt+1
                elif anotherInt == 7 and HowMany >=8:
                    if eight== 0:
                        eight = [[float(xfmr_cableStorage[i][j][2])]]
                    else:
                        eight.append([float(xfmr_cableStorage[i][j][2])])
                    anotherInt = anotherInt + 1
                elif anotherInt == 8 and HowMany >=9:
                    if nine == 0:
                        nine = [[float(xfmr_cableStorage[i][j][2])]]
                    else:
                        nine.append([float(xfmr_cableStorage[i][j][2])])
                    anotherInt = anotherInt + 1
                elif anotherInt == 9 and HowMany >=10:
                    if ten == 0:
                        ten = [[float(xfmr_cableStorage[i][j][2])]]
                    else:
                        ten.append([float(xfmr_cableStorage[i][j][2])])
                    anotherInt = anotherInt + 1


print 'starter 3'
print one
print two
print three
print Total_Cable

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

print Total_xfmr
print Total_ByPhase
print Total_Cable
exit()

xfmrStorage = [[(0, 'MULI_BR1', 64.906), (0, 'LLND_BR1', 77.658), (0, 'LIBRL_BR1', 74.596)],
               [(5, 'MULI_BR1', 66.396), (5, 'LLND_BR1', 80.605), (5, 'LIBRL_BR1', 76.088)],
               [(10, 'MULI_BR1', 68.398), (10, 'LLND_BR1', 83.228), (10, 'LIBRL_BR1', 76.953)],
               [(15, 'MULI_BR1', 70.19), (15, 'LLND_BR1', 86.701), (15, 'LIBRL_BR1', 77.739)]]
'''