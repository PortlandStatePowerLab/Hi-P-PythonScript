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
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import numpy as np
import time
from pytz import timezone
import json
#from IPython.display import clear_output
import sys
import re
import csv

pacific = timezone('US/Pacific')

# *********************************************
# Importing CYMPY Library from CYME EXE Folder
# *********************************************
CYMPY_LOCATION = r"C:\Program Files (x86)\CYME\CYME 7.1"
sys.path.insert(1, CYMPY_LOCATION)
import cympy
import cympy.rm
import cympy.db
import cympy.eq

import function_study_analysis_Base
from definitions_Base import *

# *********************************************
# Opening Self Contained File from directory
# *********************************************

if __name__ == "__main__":
    start = datetime.now()
    #Open study and list out devices

    function_study_analysis_Base.open_study(model_filename)

    #a = function_study_analysis_Base.read_cutsheet(temp_cutsheet_store_path, r"X:\Cutsheets\Emergency Switching Sheets\2018 Emergency Cutsheets\Mulino BR1_E_1155.pdf")

    breakers = function_study_analysis_Base.list_devices(cympy.enums.DeviceType.Breaker)

    transformers = function_study_analysis_Base.list_devices(cympy.enums.DeviceType.Transformer)

    #Create tables that will store ALL loading data for later <-- ALL LOADINGS

    temp = function_study_analysis_Base.create_tables(breakers, "Breaker")
    feeder_summer_table = temp["Summer"]
    feeder_winter_table = temp["Winter"]
    temp = function_study_analysis_Base.create_tables(transformers, "Transformer")
    transformer_summer_table = temp["Summer"]
    transformer_winter_table = temp["Winter"]
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

    function_study_analysis_Base.open_study(model_filename)

    temp = function_study_analysis_Base.season_overload_analysis(loadings_simulation_year_winter, "Winter",
                                                            winter_loadings_filename,
                                                            winter_overload_report_filename)

    breaker_overload_winter = temp["Breaker"]
    xfmr_overload_winter = temp["Transformer"]

    #Create base winter values in loading tables

    feeder_winter_table = feeder_winter_table.assign(**{"N-0 KVA": ""})
    for index, row in breaker_overload_winter.iterrows():
        feeder_winter_table.loc[
            cympy.study.GetDevice(row["device_number"], cympy.enums.DeviceType.Breaker).EquipmentID][
            "N-0 KVA"] = int(function_study_analysis_Base.max_current(row.device_number, cympy.enums.DeviceType.Breaker))
    transformer_winter_table = transformer_winter_table.assign(**{"N-0 KVA": ""})
    for index, row in transformers.iterrows():
        transformer_winter_table.loc[row["device_number"]][
            "N-0 KVA"] = int(
            float(cympy.study.QueryInfoDevice("KVATOT", row.device_number, cympy.enums.DeviceType.Transformer)))

    cympy.study.Close(False)

    # Re-open study and simulate summer loads for N-0

    function_study_analysis_Base.open_study(model_filename)

    temp = function_study_analysis_Base.season_overload_analysis(loadings_simulation_year_summer, "Summer",
                                                            summer_loadings_filename,
                                                            summer_overload_report_filename)
    breaker_overload_summer = temp["Breaker"]
    xfmr_overload_summer = temp["Transformer"]

    # Create base summer values in loading tables

    feeder_summer_table = feeder_summer_table.assign(**{"N-0 KVA": ""})
    for index, row in breaker_overload_summer.iterrows():
        feeder_summer_table.loc[
            cympy.study.GetDevice(row["device_number"], cympy.enums.DeviceType.Breaker).EquipmentID][
            "N-0 KVA"] = int(function_study_analysis_Base.max_current(row.device_number, cympy.enums.DeviceType.Breaker))
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

        function_study_analysis_Base.open_study(model_filename)

        temp = function_study_analysis_Base.season_overload_analysis(loadings_simulation_year_winter, "Winter",winter_loadings_filename,winter_overload_report_filename, temp_cutsheet_store_path,cutsheet_filename, save_contingency_selfcontained, contingency_selfcontained_store_dir)
        breaker_overload_winter = temp["Breaker"]
        xfmr_overload_winter = temp["Transformer"]

        # Enter winter values into loading tables

        feeder_winter_table = feeder_winter_table.assign(**{filename[:-4] + " KVA": ""})
        for index, row in breaker_overload_winter.iterrows():
            feeder_winter_table.loc[
                cympy.study.GetDevice(row["device_number"], cympy.enums.DeviceType.Breaker).EquipmentID][
                filename[:-4] + " KVA"] = int(
                function_study_analysis_Base.max_current(row.device_number, cympy.enums.DeviceType.Breaker))
        transformer_winter_table = transformer_winter_table.assign(**{filename[:-4] + " KVA": ""})
        for index, row in transformers.iterrows():
            transformer_winter_table.loc[row["device_number"]][
                filename[:-4] + " KVA"] = int(
                float(cympy.study.QueryInfoDevice("KVATOT", row.device_number,
                                                  cympy.enums.DeviceType.Transformer)))

        cympy.study.Close(False)

        # Re-open study and simulate summer loads for selected cutsheet

        function_study_analysis_Base.open_study(model_filename)

        temp = function_study_analysis_Base.season_overload_analysis(loadings_simulation_year_summer, "Summer",summer_loadings_filename,summer_overload_report_filename, temp_cutsheet_store_path,cutsheet_filename, save_contingency_selfcontained, contingency_selfcontained_store_dir)

        breaker_overload_summer = temp["Breaker"]
        xfmr_overload_summer = temp["Transformer"]

        # Enter summer values into loading tables

        feeder_summer_table = feeder_summer_table.assign(**{filename[:-4]+ " KVA": ""})
        for index, row in breaker_overload_summer.iterrows():
            feeder_summer_table.loc[
                cympy.study.GetDevice(row["device_number"], cympy.enums.DeviceType.Breaker).EquipmentID][
                filename[:-4]+ " KVA"] = int(
                function_study_analysis_Base.max_current(row.device_number, cympy.enums.DeviceType.Breaker))
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

    function_study_analysis_Base.write_overload_tables(feeder_winter_table,feeder_summer_table,transformer_winter_table,transformer_summer_table,loading_tables_filename)

    function_study_analysis_Base.open_study(model_filename)

    breakers = function_study_analysis_Base.list_devices(cympy.enums.DeviceType.Breaker)

    transformers = function_study_analysis_Base.list_devices(cympy.enums.DeviceType.Transformer)

    #Create graphs based on maximum loading values

    function_study_analysis_Base.plot_overload(feeder_N0_winter, feeder_N0_summer, "Breakers", "Feeder Loading (N-0)",
                                          [[67, "Black", "67% Seasonal Rating", .5],
                                           [100, "Red", "100% Seasonal Rating", 1]],
                                          feeder_normal_overload_plot_filename)
    function_study_analysis_Base.plot_overload(feeder_N1_feeder_winter, feeder_N1_feeder_summer,
                                          "Breakers", "Worst Feeder Contingencies (N-1 Feeders)",
                                          [[67, "Black", "67% Seasonal Rating", .5],
                                           [100, "Red", "100% Seasonal Rating", 1]],
                                          feeder_feeder_overload_plot_filename)
    function_study_analysis_Base.plot_overload(feeder_N1_xfmr_winter, feeder_N1_xfmr_summer,
                                          "Breakers", "Worst Feeder Contingencies (N-1 Transformers)",
                                          [[67, "Black", "67% Seasonal Rating", .5],
                                           [100, "Red", "100% Seasonal Rating", 1]],
                                          feeder_transformer_overload_plot_filename)
    function_study_analysis_Base.plot_overload(transformer_N0_winter, transformer_N0_summer,
                                          "Transformers", "Transformer Loading (N-0)",
                                          [[80, "Black", "80% Seasonal LBNR", .5],
                                           [100, "Red", "100% Seasonal LBNR", 1]],
                                          transformer_normal_overload_plot_filename)
    function_study_analysis_Base.plot_overload(transformer_N1_feeder_winter, transformer_N1_feeder_summer,
                                          "Transformers", "Worst Transformer Contingencies (N-1 Feeders)",
                                          [[80, "Black", "80% Seasonal LBNR", .5],
                                           [100, "Red", "100% Seasonal LBNR", 1]],
                                          transformer_feeder_overload_plot_filename)
    function_study_analysis_Base.plot_overload(transformer_N1_xfmr_winter, transformer_N1_xfmr_summer,
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
        function_study_analysis_Base.gen_load_analysis_report(breakers, loading_report_filename)
    else:
        print(' ')
        print('Skipping Loadings Report...')

    # *********************************************
    # Calculating Unbalance Phases in the system and uploading to DataFrame
    # *********************************************
    if unbalanced_voltage_report_needed == True:
        function_study_analysis_Base.gen_unbalanced_voltage_report(breakers, unbalanced_voltage_report_filename)
    else:
        print(' ')
        print('Skipping Voltage Report...')

    # *********************************************
    # Calculating Short Circuit in the system and uploading to DataFrame
    # *********************************************
    if short_circuit_report_needed == True:
        function_study_analysis_Base.gen_short_circuit_report(breakers, short_circuit_report_filename)
    else:
        print(' ')
        print('Skipping Short Circuit Report...')

    # *********************************************
    # Saving the actual Self-Contained File in the directory
    # *********************************************
    if saving_selfcontained_needed == True:
        function_study_analysis_Base.save_study()
    else:
        print(' ')
        print('Skipping Saving the Self-Contained File...')
    # *********************************************
    # Creating and Saving CYME Report in directory
    # *********************************************
    if cyme_report_needed == True:
        function_study_analysis_Base.gen_cyme_report(cyme_report_filename)
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
