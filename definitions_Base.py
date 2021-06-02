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
# 8888888b.  8888888888 8888888888 8888888 888b    888 8888888 88888888888 8888888 .d88888b.  888b    888  .d8888b.
# 888  "Y88b 888        888          888   8888b   888   888       888       888  d88P" "Y88b 8888b   888 d88P  Y88b
# 888    888 888        888          888   88888b  888   888       888       888  888     888 88888b  888 Y88b.
# 888    888 8888888    8888888      888   888Y88b 888   888       888       888  888     888 888Y88b 888  "Y888b.
# 888    888 888        888          888   888 Y88b888   888       888       888  888     888 888 Y88b888     "Y88b.
# 888    888 888        888          888   888  Y88888   888       888       888  888     888 888  Y88888       "888
# 888  .d88P 888        888          888   888   Y8888   888       888       888  Y88b. .d88P 888   Y8888 Y88b  d88P
# 8888888P"  8888888888 888        8888888 888    Y888 8888888     888     8888888 "Y88888P"  888    Y888  "Y8888P"
#
# *********************************************
# Importing needed Libraries from Python
# *********************************************
#import cympy
#import cympy.rm
#import cympy.db
#
# *********************************************
# PATH FOR DEFINITIONS
# *********************************************
model_filename = 'C:\\Users\\pwrlab07\\PycharmProjects\\PGEPython\\INPUT\\Mulino_PythonTest_CYME_Analysis_Base.sxst'

winter_loadings_filename = "C:\\Users\\pwrlab07\\PycharmProjects\\PGEPython\\INPUT\\FEEDER_LoadAllocation_Winter_Historical Loading.xlsx"
summer_loadings_filename = "C:\\Users\\pwrlab07\\PycharmProjects\\PGEPython\\INPUT\\FEEDER_LoadAllocation_Summer_Historical Loading.xlsx"
loadings_simulation_year_summer = 2016
loadings_simulation_year_winter = 2016

cutsheet_filepath = r"C:\Users\pwrlab07\Cutsheets\EmergencySwitchingSheets\2018EmergencyCutsheets\\"
cutsheet_keywords = ["Mulino"]

temp_cutsheet_store_path = r"C:\temp\temp_cutsheet.csv"

# *********************************************
# PLEASE indicate Reports NEEDED
# *********************************************
winter_overload_report_filename = "C:\\Users\\pwrlab07\\PycharmProjects\\PGEPython\\OUTPUT_Base\\Overload_Winter_Analysis_data.csv"
summer_overload_report_filename = "C:\\Users\\pwrlab07\\PycharmProjects\\PGEPython\\OUTPUT_Base\\Overload_Summer_Analysis_data.csv"

feeder_normal_overload_plot_filename = "C:\\Users\\pwrlab07\\PycharmProjects\\PGEPython\\OUTPUT_Base\\Feeder_Normal_Overload_Plot.png"
feeder_feeder_overload_plot_filename = "C:\\Users\\pwrlab07\\PycharmProjects\\PGEPython\\OUTPUT_Base\\Feeder_Worst_N1Feeder_Overload_Plot.png"
feeder_transformer_overload_plot_filename = "C:\\Users\\pwrlab07\\PycharmProjects\\PGEPython\\OUTPUT_Base\\Feeder_Worst_N1Transformer_Overload_Plot.png"
transformer_normal_overload_plot_filename = "C:\\Users\\pwrlab07\\PycharmProjects\\PGEPython\\OUTPUT_Base\\Transformer_Normal_Overload_Plot.png"
transformer_feeder_overload_plot_filename = "C:\\Users\\pwrlab07\\PycharmProjects\\PGEPython\\OUTPUT_Base\\Transformer_Worst_N1Feeder_Overload_Plot.png"
transformer_transformer_overload_plot_filename = "C:\\Users\\pwrlab07\\PycharmProjects\\PGEPython\\OUTPUT_Base\\Transformer_Worst_N1Transformer_Overload_Plot.png"

loading_tables_filename = "C:\\Users\\pwrlab07\\PycharmProjects\\PGEPython\\OUTPUT_Base\\Loading_Tables.xlsx"

loading_report_needed = True
loading_report_filename = "C:\\Users\\pwrlab07\\PycharmProjects\\PGEPython\\OUTPUT_Base\\Load_Analysis_data.csv"

unbalanced_voltage_report_needed = False
unbalanced_voltage_report_filename = "C:\\Users\\pwrlab07\\PycharmProjects\\PGEPython\\OUTPUT_Base\\Voltage_Analysis_data.csv"

short_circuit_report_needed = False
short_circuit_report_filename = "C:\\Users\\pwrlab07\\PycharmProjects\\PGEPython\\OUTPUT_Base\\ShortCircuit_Analysis_data.csv"

cyme_report_needed = False
cyme_report_filename = "C:\\Users\\pwrlab07\\PycharmProjects\\PGEPython\\OUTPUT_Base\\cyme_analysis_data.xlsx"

# *********************************************
# PLEASE indicate if you would like to SAVE CHANGES to Self Contain
# *********************************************
save_contingency_selfcontained = False
contingency_selfcontained_store_dir = "C:\\Users\\pwrlab07\\PycharmProjects\\PGEPython\\OUTPUT\\"

saving_selfcontained_needed = False