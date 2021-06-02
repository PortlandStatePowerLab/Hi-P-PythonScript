## -*- coding: utf-8 -*-
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
# 8888888888 888     888 888b    888  .d8888b. 88888888888 8888888 .d88888b.  888b    888  .d8888b.
# 888        888     888 8888b   888 d88P  Y88b    888       888  d88P" "Y88b 8888b   888 d88P  Y88b
# 888        888     888 88888b  888 888    888    888       888  888     888 88888b  888 Y88b.
# 8888888    888     888 888Y88b 888 888           888       888  888     888 888Y88b 888  "Y888b.
# 888        888     888 888 Y88b888 888           888       888  888     888 888 Y88b888     "Y88b.
# 888        888     888 888  Y88888 888    888    888       888  888     888 888  Y88888       "888
# 888        Y88b. .d88P 888   Y8888 Y88b  d88P    888       888  Y88b. .d88P 888   Y8888 Y88b  d88P
# 888         "Y88888P"  888    Y888  "Y8888P"     888     8888888 "Y88888P"  888    Y888  "Y8888P"
#
# *********************************************
# Importing needed Libraries from Python
# *********************************************
from __future__ import division
import pandas
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
import ModifySpotLoad

CYMPY_LOCATION = r"C:\Program Files (x86)\CYME\CYME"
sys.path.insert(1, CYMPY_LOCATION)
import cympy
import cympy.rm
import cympy.db
import cympy.study
import cympy.enums

# *********************************************
# Functions created for each capability
# *********************************************

def open_study(study_file_path):
    # Open specified study and run load flow
    start = datetime.now()
    print(' ')
    print('Querying Self-Contained File...')
    cympy.study.Open(study_file_path)
    load_flow = cympy.sim.LoadFlow()
    load_flow.Run()



    end = datetime.now()
    print('Done in ' + str((end - start).total_seconds()) + ' seconds')


def run_load_flow():

    #Run CYME load flow

    start = datetime.now()
    try:
        print(' ')
        print('Simulating Load Flow Analysis...')
        load_flow = cympy.sim.LoadFlow()
        load_flow.Run()
    except cympy.err.CymError as error_flow_message:
        print(error_flow_message.GetMessage())
        print("CYME Errors: " + str(cympy.GetMessages(2)))
    end = datetime.now()
    print('Done in ' + str((end - start).total_seconds()) + ' seconds')

def run_short_circuit():
    start = datetime.now()
    try:
        print(' ')
        print('Simulating Short Circuit Analysis...')
        short_circuit = cympy.sim.ShortCircuit()
        short_circuit.SetValue('SC', 'ParametersConfigurations[0].Domain')
        short_circuit.Run()
    except cympy.err.CymError as error_sc_message:
        print(error_sc_message.GetMessage())
        print("CYME Errors: " + str(cympy.GetMessages(2)))
    end = datetime.now()
    print('Done in ' + str((end - start).total_seconds()) + ' seconds')

def list_devices(device_type, verbose=True):
    #start=datetime.now()
    #print(' ')
    #print('List of SELECTED Equipments in Database:')
    devices = cympy.study.ListDevices(device_type)
    devices = pandas.DataFrame(devices, columns=['device'])
    devices['device_type_id'] = devices['device'].apply(lambda x: x.DeviceType)

    devices['NetworkID'] = devices['device'].apply(lambda x: x.NetworkID)
    devices['device_number'] = devices['device'].apply(lambda x: x.DeviceNumber)
    devices['device_type'] = devices['device_type_id'].apply(lambda x: lookup.type_table[x])

    if verbose:
        unique_type = devices['device_type'].unique().tolist()
        for device_type in unique_type:
            hello=0
            #print('There are ' + str(devices[devices.device_type == device_type].count()[0]) +
            #      ' ' + device_type)
    #end=datetime.now()
    #print('list_devices PGE Done in ' + str((end - start).total_seconds()) + ' seconds')

    return devices

def gen_overload_report(season, devices, device_type, file_path):
    start = datetime.now()
    if season == "Winter":
        print(' ')
        print('Calculating Winter Overloads in the selected networks...')
        overload = devices.copy()
        overload_analysis = file_path
        overload['current_A'] = [0] * len(overload)
        overload['current_B'] = [0] * len(overload)
        overload['current_C'] = [0] * len(overload)
        overload['winter_overload_A'] = [0] * len(overload)
        overload['winter_overload_B'] = [0] * len(overload)
        overload['winter_overload_C'] = [0] * len(overload)
        overload['winter_overload_Total'] = [0] * len(overload)

        for device in devices.itertuples():
            overload.loc[device.Index, 'current_A'] = cympy.study.QueryInfoDevice(
                "IA", device.device_number, int(device.device_type_id))
            overload.loc[device.Index, 'current_B'] = cympy.study.QueryInfoDevice(
                "IB", device.device_number, int(device.device_type_id))
            overload.loc[device.Index, 'current_C'] = cympy.study.QueryInfoDevice(
                "IC", device.device_number, int(device.device_type_id))
            overload.loc[device.Index, 'winter_overload_A'] = cympy.study.QueryInfoDevice(
                "LoadingEqRating2A", device.device_number, int(device.device_type_id))
            overload.loc[device.Index, 'winter_overload_B'] = cympy.study.QueryInfoDevice(
                "LoadingEqRating2B", device.device_number, int(device.device_type_id))
            overload.loc[device.Index, 'winter_overload_C'] = cympy.study.QueryInfoDevice(
                "LoadingEqRating2C", device.device_number, int(device.device_type_id))
            overload.loc[device.Index, 'winter_overload_Total'] = cympy.study.QueryInfoDevice(
                "LoadingEqRating2", device.device_number, int(device.device_type_id))

        for column in ['current_A','current_B', 'current_C', 'winter_overload_A', 'winter_overload_B', 'winter_overload_C',
                       'winter_overload_Total']:
            overload[column] = overload[column].apply(lambda x: None if x is '' else float(x))

        if device_type == "Breakers":
            overload_2 = overload[overload['device_number'].str.contains("BREAKER_")]
            overload_2.to_csv(overload_analysis, index=False, header=True)
            end = datetime.now()
            print('Done in ' + str((end - start).total_seconds()) + ' seconds')
            return overload_2
        elif device_type == "Transformers":
            overload_4 = overload
            overload_4.to_csv(overload_analysis, index=False, header=True)
            end = datetime.now()
            print('Done in ' + str((end - start).total_seconds()) + ' seconds')
            return overload_4
        else:
            overload.to_csv(overload_analysis, index=False, header=True)
            end = datetime.now()
            print('Done in ' + str((end - start).total_seconds()) + ' seconds')
            return overload
    elif season == "Summer":
        print(' ')
        print('Calculating Summer Overloads in the selected networks...')
        overload = devices.copy()
        overload_analysis = file_path
        overload['summer_overload_A'] = [0] * len(overload)
        overload['summer_overload_B'] = [0] * len(overload)
        overload['summer_overload_C'] = [0] * len(overload)
        overload['summer_overload_Total'] = [0] * len(overload)
        overload['current_A'] = [0] * len(overload)
        overload['current_B'] = [0] * len(overload)
        overload['current_C'] = [0] * len(overload)

        for device in devices.itertuples():
            overload.loc[device.Index, 'summer_overload_A'] = cympy.study.QueryInfoDevice(
                "LoadingEqRating1A", device.device_number, int(device.device_type_id))
            overload.loc[device.Index, 'summer_overload_B'] = cympy.study.QueryInfoDevice(
                "LoadingEqRating1B", device.device_number, int(device.device_type_id))
            overload.loc[device.Index, 'summer_overload_C'] = cympy.study.QueryInfoDevice(
                "LoadingEqRating1C", device.device_number, int(device.device_type_id))
            overload.loc[device.Index, 'summer_overload_Total'] = cympy.study.QueryInfoDevice(
                "LoadingEqRating1", device.device_number, int(device.device_type_id))
            overload.loc[device.Index, 'current_A'] = cympy.study.QueryInfoDevice(
                "IA", device.device_number, int(device.device_type_id))
            overload.loc[device.Index, 'current_B'] = cympy.study.QueryInfoDevice(
                "IB", device.device_number, int(device.device_type_id))
            overload.loc[device.Index, 'current_C'] = cympy.study.QueryInfoDevice(
                "IC", device.device_number, int(device.device_type_id))

        for column in ['summer_overload_A', 'summer_overload_B', 'summer_overload_C', 'summer_overload_Total',
                       'current_A',
                       'current_B', 'current_C']:
            overload[column] = overload[column].apply(lambda x: None if x is '' else float(x))

        if device_type == "Breakers":
            overload_2 = overload[overload['device_number'].str.contains("BREAKER")]
            #print("#########################")
            #print("Didn't think I'd need to do this again, silly me")
            #print(overload_analysis)
            #print(type(overload_analysis))
            #print(overload_2)
            #print(type(overload_2))
            overload_2.to_csv(overload_analysis, index=False, header=True)
            end = datetime.now()
            print('Done in ' + str((end - start).total_seconds()) + ' seconds')
            return overload_2
        elif device_type == "Transformers":
            overload_4 = overload
            overload_4.to_csv(overload_analysis, index=False, header=True)
            end = datetime.now()
            print('Done in ' + str((end - start).total_seconds()) + ' seconds')
            return overload_4
        else:
            overload.to_csv(overload_analysis, index=False, header=True)
            end = datetime.now()
            print('Done in ' + str((end - start).total_seconds()) + ' seconds')
            return overload
    else:
        print("Season must be Winter/Summer!")
        return

def gen_load_analysis_report(devices, file_path):
    start = datetime.now()
    print(' ')
    print('Calculating Loading (MW, MVAR, & MVA) at ALL Devices...')
    load = devices.copy()
    load['MWA'] = [0] * len(load)
    load['MWB'] = [0] * len(load)
    load['MWC'] = [0] * len(load)
    load['MWTOT'] = [0] * len(load)
    load['MVARA'] = [0] * len(load)
    load['MVARB'] = [0] * len(load)
    load['MVARC'] = [0] * len(load)
    load['MVARTOT'] = [0] * len(load)
    load['MVAA'] = [0] * len(load)
    load['MVAB'] = [0] * len(load)
    load['MVAC'] = [0] * len(load)
    load['MVATOT'] = [0] * len(load)

    for device in devices.itertuples():
        load.loc[device.Index, 'MWA'] = cympy.study.QueryInfoDevice(
            "MWA", device.device_number, int(device.device_type_id))
        load.loc[device.Index, 'MWB'] = cympy.study.QueryInfoDevice(
            "MWB", device.device_number, int(device.device_type_id))
        load.loc[device.Index, 'MWC'] = cympy.study.QueryInfoDevice(
            "MWC", device.device_number, int(device.device_type_id))
        load.loc[device.Index, 'MWTOT'] = cympy.study.QueryInfoDevice(
            "MWTOT", device.device_number, int(device.device_type_id))
        load.loc[device.Index, 'MVARA'] = cympy.study.QueryInfoDevice(
            "MVARA", device.device_number, int(device.device_type_id))
        load.loc[device.Index, 'MVARB'] = cympy.study.QueryInfoDevice(
            "MVARB", device.device_number, int(device.device_type_id))
        load.loc[device.Index, 'MVARC'] = cympy.study.QueryInfoDevice(
            "MVARC", device.device_number, int(device.device_type_id))
        load.loc[device.Index, 'MVARTOT'] = cympy.study.QueryInfoDevice(
            "MVARTOT", device.device_number, int(device.device_type_id))
        load.loc[device.Index, 'MVAA'] = cympy.study.QueryInfoDevice(
            "MVAA", device.device_number, int(device.device_type_id))
        load.loc[device.Index, 'MVAB'] = cympy.study.QueryInfoDevice(
            "MVAB", device.device_number, int(device.device_type_id))
        load.loc[device.Index, 'MVAC'] = cympy.study.QueryInfoDevice(
            "MVAC", device.device_number, int(device.device_type_id))
        load.loc[device.Index, 'MVATOT'] = cympy.study.QueryInfoDevice(
            "MVATOT", device.device_number, int(device.device_type_id))

    for column in ['MWA', 'MWB', 'MWC', 'MWTOT', 'MVARA', 'MVARB', 'MVARC', 'MVARTOT', 'MVAA', 'MVAB', 'MVAC',
                   'MVATOT']:
        load[column] = load[column].apply(lambda x: None if x is '' else float(x))

    load_2 = load[load['device_number'].str.contains("BREAKER")]
    load_2.to_csv(file_path, index=False, header=True)

    end = datetime.now()
    print('Done in ' + str((end - start).total_seconds()) + ' seconds')

def gen_unbalanced_voltage_report(devices, file_path):
    start = datetime.now()
    print(' ')
    print('Calculating unbalance Voltages...')
    voltage = devices.copy()
    voltage['voltage_A'] = [0] * len(voltage)
    voltage['voltage_B'] = [0] * len(voltage)
    voltage['voltage_C'] = [0] * len(voltage)

    for device in devices.itertuples():
        voltage.loc[device.Index, 'voltage_A'] = cympy.study.QueryInfoDevice(
            "VBaseA", device.device_number, int(device.device_type_id))
        voltage.loc[device.Index, 'voltage_B'] = cympy.study.QueryInfoDevice(
            "VBaseB", device.device_number, int(device.device_type_id))
        voltage.loc[device.Index, 'voltage_C'] = cympy.study.QueryInfoDevice(
            "VBaseC", device.device_number, int(device.device_type_id))


    # Get the mean voltage across phase
    # voltage['mean_voltage_ABC'] = voltage[['voltage_A', 'voltage_B', 'voltage_C']].mean(axis=1)

    # *********************************************
    # Voltage Unbalace Function
    # *********************************************
    def _diff(value):
        diff = []
        for phase in ['voltage_A', 'voltage_B', 'voltage_C']:
            diff.append(abs(float(value[phase]) - value['mean_voltage_ABC']) * 100 / value['mean_voltage_ABC'])
        return max(diff)


    # Get the max difference of the three phase voltage with the mean
    # voltage['diff_with_mean'] = voltage[['mean_voltage_ABC', 'voltage_A', 'voltage_B', 'voltage_C']].apply(_diff, axis=1)
    for column in ['voltage_A', 'voltage_B', 'voltage_C']:
        voltage[column] = voltage[column].apply(lambda x: None if x is '' else float(x))

    voltage_2 = voltage[voltage['device_number'].str.contains("BREAKER")]
    voltage_2.to_csv(file_path, index=False, header=True)

    end = datetime.now()
    print('Done in ' + str((end - start).total_seconds()) + ' seconds')

def gen_short_circuit_report(devices, file_path):
    start = datetime.now()
    print(' ')
    print('Calculating Short Circuit in the selected networks...')
    sc = devices.copy()
    sc['LLLampKmin'] = [0] * len(sc)
    sc['LLLampKmax'] = [0] * len(sc)
    sc['LGampKmin'] = [0] * len(sc)
    sc['LGampKmax'] = [0] * len(sc)

    for device in devices.itertuples():
        sc.loc[device.Index, 'LLLampKmin'] = cympy.study.QueryInfoDevice(
            "LLLampKmin", device.device_number, int(device.device_type_id))
        sc.loc[device.Index, 'LLLampKmax'] = cympy.study.QueryInfoDevice(
            "LLLampKmax", device.device_number, int(device.device_type_id))
        sc.loc[device.Index, 'LGampKmin'] = cympy.study.QueryInfoDevice(
            "LGampKmin", device.device_number, int(device.device_type_id))
        sc.loc[device.Index, 'LGampKmax'] = cympy.study.QueryInfoDevice(
            "LGampKmax", device.device_number, int(device.device_type_id))

    for column in ['LLLampKmin', 'LLLampKmax', 'LGampKmin', 'LGampKmax']:
        sc[column] = sc[column].apply(lambda x: None if x is '' else float(x))

    sc_2 = sc[sc['device_number'].str.contains("BREAKER")]
    sc_2.to_csv(file_path, index=False, header=True)

    end = datetime.now()
    print('Done in ' + str((end - start).total_seconds()) + ' seconds')

def gen_cyme_report(file_path):
    start = datetime.now()
    print(' ')
    print('Creating/Saving Report File...')
    report_name = "Feeder and Transformer Loading"
    networks = cympy.study.ListNetworks()
    cympy.rm.Save(report_name, networks, cympy.enums.ReportModeType.MSExcel, file_path)
    end = datetime.now()
    print('Done in ' + str((end - start).total_seconds()) + ' seconds')

def save_study(file_path):
    start = datetime.now()
    print(' ')
    print('Saving Study...')
    cympy.study.Save(file_path)
    end = datetime.now()
    print('Done in ' + str((end - start).total_seconds()) + ' seconds')

def season_overload_analysis(year, season, loading_file_path, overload_file_path, temp_cutsheet_store_path =None,cutsheet_file_path=None, save_contingency_selfcontained = None, contingency_selfcontained_store_dir = None):
    if season == "Winter" or season == "Summer":
        print("##################################################")
        print("# STARTING SEASONAL OVERLOAD ANALYSIS FOR " + season.upper() + " #")
        print("##################################################")
    else:
        print("Season not valid for seasonal overload analysis!")
        return

    # *********************************************
    # Load Allocation For Self Contained File
    # *********************************************
    run_load_allocation(year,loading_file_path)

    list_source_nodes()

    # *********************************************
    # Emergency Switch Operation
    # *********************************************
    if cutsheet_file_path:
        print(1)
        print(temp_cutsheet_store_path)
        print(cutsheet_file_path)
        print(2)
        run_cutsheet(temp_cutsheet_store_path, cutsheet_file_path)
    else:
        print('')
        print('No Emergency Cutsheet Simulated')
        print cutsheet_file_path

    # *********************************************
    # Load Flow Analysis for Self Contained File
    # *********************************************
    run_load_flow()
    run_short_circuit()

    # *********************************************
    # Creating list of devices from the Self Contained File
    # *********************************************
    # *********************************************
    # Devices Database
    # *********************************************
    breakers = list_devices(cympy.enums.DeviceType.Breaker)
    transformers = list_devices(cympy.enums.DeviceType.Transformer)

    # *********************************************
    # Calculating Overloads in the system and uploading to DataFrame
    # *********************************************
    overload_dict = {}
    overload_dict["Breaker"] =  gen_overload_report(season, breakers,"Breakers",overload_file_path)
    overload_dict["Transformer"] = gen_overload_report(season, transformers,"Transformers", overload_file_path)
    if cutsheet_file_path and save_contingency_selfcontained:
        save_study(contingency_selfcontained_store_dir+cutsheet_file_path.split("\\")[-1][:-4] + "_" + season + ".sxst")
    return overload_dict


def fmu_wrapper_Cym(model_filename, input_values, input_names,
                output_names, output_device_names, write_result):
    """Communicate with the FMU to launch a Cymdist simulation

    Args:
        model_filename (String): path to the cymdist grid model
        input_values (List): list of float with the same order as input_names
        input_names (List): list of String to describe the list of values
        output_names (List): list of String output names [voltage_A, voltage_B, ...]
        output_device_names (List): list of String output device name (same lenght as output_names)
        write_result (Boolean): if True the entire results are saved to the file system (add ~30secs)

    Example:
        >>> write_results = 0  # (or False)
        >>> model_filename = 'HL0004.sxst'
        >>> input_names = ['VMAG_A', 'VMAG_B', 'VMAG_C', 'P_A', 'P_B', 'P_C', 'Q_A', 'Q_B', 'Q_C']
        >>> input_values = [7287, 7299, 7318, 7272, 2118, 6719, -284, -7184, 3564]
        >>> output_names = ['voltage_A', 'voltage_B', 'voltage_C']
        >>> output_device_names = ['HOLLISTER_2104', 'HOLLISTER_2104', 'HOLLISTER_2104']

        >>> fmu_wrapper(model_filename, input_values, input_names,
                        output_names, output_device_names, write_result)
    """

    # Open the model
    cympy.study.Open(model_filename)

    # Create a dictionary from the input values and input names
    udata = {}
    for name, value in zip(input_names, input_values):
        udata[name] = value

    # Run load allocation function to set input values
    load_allocation_Cym(udata)

    # Run the power flow
    lf = cympy.sim.LoadFlow()
    lf.Run()

    # Get the full output data <--- optimize this part to gain time
    devices = list_devices_Cym()
    devices = get_voltage_Cym(devices)
    devices = get_overload_Cym(devices)
    devices = get_load_Cym(devices)
    devices = get_unbalanced_line_Cym(devices)
    devices = get_distance_Cym(devices)

    # Write full results?
    if write_result:
        # Get the full output data (time consuming)
        temp = list_devices_Cym()
        temp = get_voltage_Cym(temp)
        temp = get_overload_Cym(temp)
        temp = get_load_Cym(temp)
        temp = get_unbalanced_line_Cym(temp)
        temp = get_distance_Cym(temp)
        with open(model_filename + '_result_.pickle', 'wb') as output_file:
            pickle.dump(temp, output_file, protocol=2)

    # Filter the result for the right outputs value
    output = []
    DEFAULT_VALUE = 0  # value to output in case of a NaN value
    for device_name, category in zip(output_device_names, output_names):
        temp = devices[devices.device_number == device_name][category]

        if not temp.isnull().any():
            output.append(temp.iloc[0])
        else:
            output.append(DEFAULT_VALUE)

    return output


def list_devices_Cym(device_type=False, verbose=False):
    """List all devices and return a break down of their type

    Args:
        device_type (Device): if passed then list of device with the same type
        verbose (Boolean): if True print result (default True)

    Return:
        DataFrame <device, device_type, device_number, device_type_id>
    """

    # Get the list of devices
    if device_type:
        devices = cympy.study.ListDevices(device_type)
    else:
        # Get all devices
        devices = cympy.study.ListDevices()

    # Create a dataframe
    devices = pandas.DataFrame(devices, columns=['device'])
    devices['device_type_id'] = devices['device'].apply(lambda x: x.DeviceType)
    devices['device_number'] = devices['device'].apply(lambda x: x.DeviceNumber)
    devices['device_type'] = devices['device_type_id'].apply(lambda x: lookup.type_table[x])

    # Get the break down of each type
    if verbose:
        unique_type = devices['device_type'].unique().tolist()
        for device_type in unique_type:
            print('There are ' + str(devices[devices.device_type == device_type].count()[0]) +
                  ' ' + device_type)

    return devices


def _describe_object_Cym(device):
        for value in cympy.dm.Describe(device.GetObjType()):
            print(value.Name)


def get_device_Cym(id, device_type, verbose=False):
    """Return a device

    Args:
        id (String): unique identifier
        device_type (DeviceType): type of device
        verbose (Boolean): describe an object

    Return:
        Device (Device)
    """
    # Get object
    device = cympy.study.GetDevice(id, device_type)

    # Describe attributes
    if verbose:
        _describe_object(device)

    return device


def add_device_Cym(device_name, device_type, section_id):
    """Return a device

    Args:
        device_name (String): unique identifier
        device_type (DeviceType): type of device
        section_id (String): unique identifier

    Return:
        Device (Device)
    """
    return cympy.study.AddDevice(device_name, device_type, section_id)


def add_pv_Cym(device_name, section_id, ns=100, np=100, location="To"):
    """Return a device

    Args:
        device_name (String): unique identifier
        section_id (String): unique identifier
        ns (Int): number of pannel in serie (* 17.3 to find voltage)
        np (Int): number of pannel in parallel (ns * np * 0.08 to find kW)
        location (String): To or From

    Return:
        Device (Device)
    """
    my_pv = add_device_Cym(device_name, cympy.enums.DeviceType.Photovoltaic, section_id)
    my_pv.SetValue(location, "Location")
    return my_pv


def load_allocation_Cym(values):
    """Run a load allocation

    Args:
        values (dictionnary): value1 (KVA) and value2 (PF) for A, B and C
    """

    # Create Load Allocation object
    la = cympy.sim.LoadAllocation()

    # Create the Demand object
    demand = cympy.sim.Meter()

    # Fill in the demand values
    demand.IsTotalDemand = False
    demand.DemandA = cympy.sim.LoadValue()
    demand.DemandA.Value1 = values['P_A']
    demand.DemandA.Value2 = values['Q_A']
    demand.DemandB = cympy.sim.LoadValue()
    demand.DemandB.Value1 = values['P_B']
    demand.DemandB.Value2 = values['Q_B']
    demand.DemandC = cympy.sim.LoadValue()
    demand.DemandC.Value1 = values['P_C']
    demand.DemandC.Value2 = values['Q_C']
    demand.LoadValueType = cympy.enums.LoadValueType.KW_KVAR

    # Get a list of networks
    networks = cympy.study.ListNetworks()

    # Set the first feeders demand
    la.SetDemand(networks[0], demand)

    # Set up the right voltage [V to kV]
    cympy.study.SetValueTopo(values['VMAG_A'] / 1000,
        "Sources[0].EquivalentSourceModels[0].EquivalentSource.OperatingVoltage1", networks[0])
    cympy.study.SetValueTopo(values['VMAG_B'] / 1000,
        "Sources[0].EquivalentSourceModels[0].EquivalentSource.OperatingVoltage2", networks[0])
    cympy.study.SetValueTopo(values['VMAG_C'] / 1000,
        "Sources[0].EquivalentSourceModels[0].EquivalentSource.OperatingVoltage3", networks[0])

    # Run the load allocation
    la.Run([networks[0]])


def get_voltage_Cym(devices):
    """
    Args:
        devices (DataFrame): list of all the devices to include

    Return:
        devices_voltage (DataFrame): devices and their corresponding voltage for
            each phase
    """
    # Create a new frame to hold the results
    voltage = devices.copy()

    # Reset or create new columns to hold the result
    voltage['voltage_A'] = [0] * len(voltage)
    voltage['voltage_B'] = [0] * len(voltage)
    voltage['voltage_C'] = [0] * len(voltage)

    for device in devices.itertuples():
        # Get the according voltage per phase in a pandas dataframe
        voltage.loc[device.Index, 'voltage_A'] = cympy.study.QueryInfoDevice(
            "VpuA", device.device_number, int(device.device_type_id))
        voltage.loc[device.Index, 'voltage_B'] = cympy.study.QueryInfoDevice(
            "VpuB", device.device_number, int(device.device_type_id))
        voltage.loc[device.Index, 'voltage_C'] = cympy.study.QueryInfoDevice(
            "VpuC", device.device_number, int(device.device_type_id))

    # Cast the right type
    for column in ['voltage_A', 'voltage_B', 'voltage_C']:
        voltage[column] = voltage[column].apply(lambda x: None if x is '' else float(x))

    return voltage


def get_overload_Cym(devices):
    """
    Args:
        devices (DataFrame): list of all the devices to include
        first_n_devices (Int): number of row to return

    Return:
        overload_device (DataFrame): return the n devices with the highest load
    """
    # Create a new frame to hold the results
    overload = devices.copy()

    # Reset or create new columns to hold the result
    overload['overload_A'] = [0] * len(overload)
    overload['overload_B'] = [0] * len(overload)
    overload['overload_C'] = [0] * len(overload)

    for device in devices.itertuples():
        # Get the according overload per phase in a pandas dataframe
        overload.loc[device.Index, 'overload_A'] = cympy.study.QueryInfoDevice(
            "OverloadAmpsA", device.device_number, int(device.device_type_id))
        overload.loc[device.Index, 'overload_B'] = cympy.study.QueryInfoDevice(
            "OverloadAmpsB", device.device_number, int(device.device_type_id))
        overload.loc[device.Index, 'overload_C'] = cympy.study.QueryInfoDevice(
            "OverloadAmpsC", device.device_number, int(device.device_type_id))

    # Cast the right type
    for column in ['overload_A', 'overload_B', 'overload_C']:
        overload[column] = overload[column].apply(lambda x: None if x is '' else float(x))

    return overload


def get_load_Cym(devices):
    """
    Args:
        devices (DataFrame): list of all the devices to include

    Return:
        devices_voltage (DataFrame): devices and their corresponding load for
            each phase
    """
    # Create a new frame to hold the results
    load = devices.copy()

    # Reset or create new columns to hold the result
    load['KWA'] = [0] * len(load)
    load['KWB'] = [0] * len(load)
    load['KWC'] = [0] * len(load)
    load['KWTOT'] = [0] * len(load)
    load['KVARA'] = [0] * len(load)
    load['KVARB'] = [0] * len(load)
    load['KVARC'] = [0] * len(load)
    load['KVARTOT'] = [0] * len(load)

    import cympy
    for device in devices.itertuples():
        load.loc[device.Index, 'KWA'] = cympy.study.QueryInfoDevice(
            "KWA", device.device_number, int(device.device_type_id))
        load.loc[device.Index, 'KWB'] = cympy.study.QueryInfoDevice(
            "KWB", device.device_number, int(device.device_type_id))
        load.loc[device.Index, 'KWC'] = cympy.study.QueryInfoDevice(
            "KWC", device.device_number, int(device.device_type_id))
        load.loc[device.Index, 'KWTOT'] = cympy.study.QueryInfoDevice(
            "KWTOT", device.device_number, int(device.device_type_id))
        load.loc[device.Index, 'KVARA'] = cympy.study.QueryInfoDevice(
            "KVARA", device.device_number, int(device.device_type_id))
        load.loc[device.Index, 'KVARB'] = cympy.study.QueryInfoDevice(
            "KVARB", device.device_number, int(device.device_type_id))
        load.loc[device.Index, 'KVARC'] = cympy.study.QueryInfoDevice(
            "KVARC", device.device_number, int(device.device_type_id))
        load.loc[device.Index, 'KVARTOT'] = cympy.study.QueryInfoDevice(
            "KVARTOT", device.device_number, int(device.device_type_id))


    # Cast the right type
    for column in ['KWA', 'KWB', 'KWC', 'KWTOT', 'KVARA', 'KVARB', 'KVARC', 'KVARTOT']:
        load[column] = load[column].apply(lambda x: None if x is '' else float(x))

    print('################Next Place################')
    print(load.iloc[1:4, 2:4])
    print('################Next Place################')
    print(load.iloc[1:4, 4:7])
    print('################Next Place################')
    print(load.iloc[1:4, 7:10])
    print('################Next Place################')
    print(load.iloc[1:4, 10:13])
    #print('################Next Place################')
    #print(load.iloc[1:4, 13:15])

    return load


def get_distance_Cym(devices):
    """
    Args:
        devices (DataFrame): list of all the devices to include

    Return:
        devices_distance (DataFrame): devices and their corresponding distance from the substation
    """
    distance = devices.copy()

    # Reset or create new columns to hold the result
    distance['distance'] = [0] * len(distance)

    for device in devices.itertuples():
        # Get the according distance in a pandas dataframe
        distance.loc[device.Index, 'distance'] = cympy.study.QueryInfoDevice(
            "Distance", device.device_number, int(device.device_type_id))

    # Cast the right type
    for column in ['distance']:
        distance[column] = distance[column].apply(lambda x: None if x is '' else float(x))

    return distance


def get_unbalanced_line_Cym(devices):
    """This function requires the get_voltage function has been called before

    Args:
        devices (DataFrame): list of all the devices to include
        first_n_devices (Int): number of row to return

    Return:
        overload_device (DataFrame): return the n devices with the highest load
    """
    # Get all the voltage
    voltage = get_voltage_Cym(devices)
    print(voltage.iloc[1:4,2:5])
    print(voltage.iloc[1:4,5:8])
    print(voltage.iloc[1:4,8:11])
    print(voltage.iloc[1:4,11:14])
    print(voltage.iloc[1:4,14:16])
    print cympy.study.QueryInfoDevice("VA", '13217377', int(14))
    print cympy.study.QueryInfoDevice("VB", '13217377', int(14))
    print cympy.study.QueryInfoDevice("VC", '13217377', int(14))
    print cympy.study.QueryInfoDevice("IA", '13217377', int(14))
    print cympy.study.QueryInfoDevice("IB", '13217377', int(14))
    print cympy.study.QueryInfoDevice("IC", '13217377', int(14))
    print cympy.study.QueryInfoDevice("KWA", '13217377', int(14))
    print cympy.study.QueryInfoDevice("KWB", '13217377', int(14))
    print cympy.study.QueryInfoDevice("KWC", '13217377', int(14))
    lf = cympy.sim.LoadFlow()
    lf.Run()
    print cympy.study.QueryInfoDevice("VA", '13217377', int(14))
    print cympy.study.QueryInfoDevice("VB", '13217377', int(14))
    print cympy.study.QueryInfoDevice("VC", '13217377', int(14))
    print cympy.study.QueryInfoDevice("IA", '13217377', int(14))
    print cympy.study.QueryInfoDevice("IB", '13217377', int(14))
    print cympy.study.QueryInfoDevice("IC", '13217377', int(14))
    print cympy.study.QueryInfoDevice("KWA", '13217377', int(14))
    print cympy.study.QueryInfoDevice("KWB", '13217377', int(14))
    print cympy.study.QueryInfoDevice("KWC", '13217377', int(14))

    spotload = function_study_analysis.list_devices(cympy.enums.DeviceType.SpotLoad)
    for spotnum in spotload['device_number']:
        spot_load_device = cympy.study.GetDevice(spotnum, cympy.enums.DeviceType.SpotLoad)
        CustLoad = cympy.study.GetLoad(spotnum, 14)
        CustList = CustLoad.ListCustomers()
        FirstPhrase = "CustomerLoads.Get({num}).CustomerLoadModels.Get(1).".format(num=CustList[0])
        SecondPhrase, kWPhase = ModifySpotLoad.PhaseCheck(FirstPhrase, spot_load_device)
        print cympy.study.QueryInfoDevice("KWC", '1658875', int(14))
        for j in range(0, len(CustList)):
            customer_load_prop = "CustomerLoads.Get({value}).".format(value=CustList[j])
            CustType = spot_load_device.GetValue(customer_load_prop + "CustomerType")
            print spot_load_device.GetValue(FirstPhrase_Add + SecondPhrase + "LoadValue.KW")

    exit()

    # Get the mean voltage accross phase
    voltage['mean_voltage_ABC'] = voltage[['voltage_A', 'voltage_B', 'voltage_C']].mean(axis=1)

    # Get the max difference of the three phase voltage with the mean
    def _diff(value):
        diff = []
        for phase in ['voltage_A', 'voltage_B', 'voltage_C']:
            print 'in phase loop'
            print value
            diff.append(abs(value[phase] - value['mean_voltage_ABC']) * 100 / value['mean_voltage_ABC'])
        return max(diff)
    print 'before assignment'
    print voltage
    voltage['diff_with_mean'] = voltage[['mean_voltage_ABC', 'voltage_A', 'voltage_B', 'voltage_C']].apply(_diff, axis=1)
    print 'after assignment'
    print voltage
    exit()
    return voltage


def get_upmu_data_Cym(inputdt, upmu_path):
    """ Retrieves instantaneous P, Q, and voltage magnitude for specified datetime.

    Args:
        inputdt (datetime): timezone aware datetime object
        upmu_path (str): e.g., '/LBNL/grizzly_bus1/'
    Returns:
        {'P_A': , 'Q_A': , 'P_B': , 'Q_B': , 'P_C': , 'Q_C': ,
         'units': ('kW', 'kVAR'),
         'VMAG_A': , 'VMAG_B': , 'VMAG_C': }
    """

    bc = btrdb.HTTPConnection("miranda.cs.berkeley.edu")
    ur = btrdb.UUIDResolver("miranda.cs.berkeley.edu", "uuidresolver", "uuidpass", "upmu")

    # convert dt to nanoseconds since epoch
    epochns = btrdb.date(inputdt.strftime('%Y-%m-%dT%H:%M:%S'))

    # retrieve raw data from btrdb
    upmu_data = {}
    streams = ['L1MAG', 'L2MAG', 'L3MAG', 'C1MAG', 'C2MAG', 'C3MAG', 'L1ANG', 'L2ANG', 'L3ANG', 'C1ANG', 'C2ANG', 'C3ANG']
    for s in streams:
        pt = bc.get_stat(ur.resolve(upmu_path + s), epochns, epochns + int(9e6))
        upmu_data[s] = pt[0][2]

    output_dict = {}

    output_dict['P_A'] = (upmu_data['L1MAG']*upmu_data['C1MAG']*np.cos(upmu_data['L1ANG'] - upmu_data['C1ANG']))*1e-3
    output_dict['Q_A'] = (upmu_data['L1MAG']*upmu_data['C1MAG']*np.sin(upmu_data['L1ANG'] - upmu_data['C1ANG']))*1e-3

    output_dict['P_B'] = (upmu_data['L2MAG']*upmu_data['C2MAG']*np.cos(upmu_data['L2ANG'] - upmu_data['C2ANG']))*1e-3
    output_dict['Q_B'] = (upmu_data['L2MAG']*upmu_data['C2MAG']*np.sin(upmu_data['L2ANG'] - upmu_data['C2ANG']))*1e-3

    output_dict['P_C'] = (upmu_data['L3MAG']*upmu_data['C3MAG']*np.cos(upmu_data['L3ANG'] - upmu_data['C3ANG']))*1e-3
    output_dict['Q_C'] = (upmu_data['L3MAG']*upmu_data['C3MAG']*np.sin(upmu_data['L3ANG'] - upmu_data['C3ANG']))*1e-3

    output_dict['units'] = ('kW', 'kVAR', 'V')

    output_dict['VMAG_A'] = upmu_data['L1MAG']
    output_dict['VMAG_B'] = upmu_data['L2MAG']
    output_dict['VMAG_C'] = upmu_data['L3MAG']
    return output_dict