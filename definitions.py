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
#model_filename = 'C:\\Users\\pwrlab07\\PycharmProjects\\PGEPython\\INPUT\\Mulino_PythonTest_CYME_Analysis_Test.sxst'
#model_filename = 'C:\\Users\\pwrlab07\\PycharmProjects\\PGEPython\\INPUT\\Cedar Hills Connections.sxst'
#model_filename = 'C:\\Users\\pwrlab07\\PycharmProjects\\PGEPython\\INPUT\\Swan_Island_Connections.sxst'
model_filename = 'C:\\Users\\pwrlab07\\PycharmProjects\\PGEPython\\INPUT\\Swan_Island_New_Connections.sxst'

int_demandprofiles=[[],[],[],[],[],[],[]]
ValueUse=10
if ValueUse == 0:
    int_demandprofiles[0] = "C:\\Users\\pwrlab07\\Desktop\\ToUDemandProfiles\\LowPenetrationProfiles\\Off\\DemandProfile0LowOff.xlsx"
    int_demandprofiles[1] = "C:\\Users\\pwrlab07\\Desktop\\ToUDemandProfiles\\LowPenetrationProfiles\\Off\\DemandProfile1LowOff.xlsx"
    int_demandprofiles[2] = "C:\\Users\\pwrlab07\\Desktop\\ToUDemandProfiles\\LowPenetrationProfiles\\Off\\DemandProfile3LowOff.xlsx"
    int_demandprofiles[3] = "C:\\Users\\pwrlab07\\Desktop\\ToUDemandProfiles\\LowPenetrationProfiles\\Off\\DemandProfile4LowOff.xlsx"
    int_demandprofiles[4] = "C:\\Users\\pwrlab07\\Desktop\\ToUDemandProfiles\\LowPenetrationProfiles\\Off\\DemandProfile5LowOff.xlsx"
    int_demandprofiles[5] = "C:\\Users\\pwrlab07\\Desktop\\ToUDemandProfiles\\LowPenetrationProfiles\\Off\\DemandProfile6LowOff.xlsx"
    int_demandprofiles[6] = "C:\\Users\\pwrlab07\\Desktop\\ToUDemandProfiles\\LowPenetrationProfiles\\Off\\DemandProfile7LowOff.xlsx"
elif ValueUse == 1:
    int_demandprofiles[0] = "C:\\Users\\pwrlab07\\Desktop\\ToUDemandProfiles\\LowPenetrationProfiles\\Mid\\DemandProfile0LowMid.xlsx"
    int_demandprofiles[1] = "C:\\Users\\pwrlab07\\Desktop\\ToUDemandProfiles\\LowPenetrationProfiles\\Mid\\DemandProfile1LowMid.xlsx"
    int_demandprofiles[2] = "C:\\Users\\pwrlab07\\Desktop\\ToUDemandProfiles\\LowPenetrationProfiles\\Mid\\DemandProfile3LowMid.xlsx"
    int_demandprofiles[3] = "C:\\Users\\pwrlab07\\Desktop\\ToUDemandProfiles\\LowPenetrationProfiles\\Mid\\DemandProfile4LowMid.xlsx"
    int_demandprofiles[4] = "C:\\Users\\pwrlab07\\Desktop\\ToUDemandProfiles\\LowPenetrationProfiles\\Mid\\DemandProfile5LowMid.xlsx"
    int_demandprofiles[5] = "C:\\Users\\pwrlab07\\Desktop\\ToUDemandProfiles\\LowPenetrationProfiles\\Mid\\DemandProfile6LowMid.xlsx"
    int_demandprofiles[6] = "C:\\Users\\pwrlab07\\Desktop\\ToUDemandProfiles\\LowPenetrationProfiles\\Mid\\DemandProfile7LowMid.xlsx"
elif ValueUse == 2:
    int_demandprofiles[0] = "C:\\Users\\pwrlab07\\Desktop\\ToUDemandProfiles\\LowPenetrationProfiles\\On\\DemandProfile0LowOn.xlsx"
    int_demandprofiles[1] = "C:\\Users\\pwrlab07\\Desktop\\ToUDemandProfiles\\LowPenetrationProfiles\\On\\DemandProfile1LowOn.xlsx"
    int_demandprofiles[2] = "C:\\Users\\pwrlab07\\Desktop\\ToUDemandProfiles\\LowPenetrationProfiles\\On\\DemandProfile3LowOn.xlsx"
    int_demandprofiles[3] = "C:\\Users\\pwrlab07\\Desktop\\ToUDemandProfiles\\LowPenetrationProfiles\\On\\DemandProfile4LowOn.xlsx"
    int_demandprofiles[4] = "C:\\Users\\pwrlab07\\Desktop\\ToUDemandProfiles\\LowPenetrationProfiles\\On\\DemandProfile5LowOn.xlsx"
    int_demandprofiles[5] = "C:\\Users\\pwrlab07\\Desktop\\ToUDemandProfiles\\LowPenetrationProfiles\\On\\DemandProfile6LowOn.xlsx"
    int_demandprofiles[6] = "C:\\Users\\pwrlab07\\Desktop\\ToUDemandProfiles\\LowPenetrationProfiles\\On\\DemandProfile7LowOn.xlsx"
elif ValueUse == 3:
    int_demandprofiles[0] = "C:\\Users\\pwrlab07\\Desktop\\ToUDemandProfiles\\MediumPenetrationProfiles\\Off\\DemandProfile0MedOff.xlsx"
    int_demandprofiles[1] = "C:\\Users\\pwrlab07\\Desktop\\ToUDemandProfiles\\MediumPenetrationProfiles\\Off\\DemandProfile1MedOff.xlsx"
    int_demandprofiles[2] = "C:\\Users\\pwrlab07\\Desktop\\ToUDemandProfiles\\MediumPenetrationProfiles\\Off\\DemandProfile3MedOff.xlsx"
    int_demandprofiles[3] = "C:\\Users\\pwrlab07\\Desktop\\ToUDemandProfiles\\MediumPenetrationProfiles\\Off\\DemandProfile4MedOff.xlsx"
    int_demandprofiles[4] = "C:\\Users\\pwrlab07\\Desktop\\ToUDemandProfiles\\MediumPenetrationProfiles\\Off\\DemandProfile5MedOff.xlsx"
    int_demandprofiles[5] = "C:\\Users\\pwrlab07\\Desktop\\ToUDemandProfiles\\MediumPenetrationProfiles\\Off\\DemandProfile6MedOff.xlsx"
    int_demandprofiles[6] = "C:\\Users\\pwrlab07\\Desktop\\ToUDemandProfiles\\MediumPenetrationProfiles\\Off\\DemandProfile7MedOff.xlsx"
elif ValueUse == 4:
    int_demandprofiles[0] = "C:\\Users\\pwrlab07\\Desktop\\ToUDemandProfiles\\MediumPenetrationProfiles\\Mid\\DemandProfile0MedMid.xlsx"
    int_demandprofiles[1] = "C:\\Users\\pwrlab07\\Desktop\\ToUDemandProfiles\\MediumPenetrationProfiles\\Mid\\DemandProfile1MedMid.xlsx"
    int_demandprofiles[2] = "C:\\Users\\pwrlab07\\Desktop\\ToUDemandProfiles\\MediumPenetrationProfiles\\Mid\\DemandProfile3MedMid.xlsx"
    int_demandprofiles[3] = "C:\\Users\\pwrlab07\\Desktop\\ToUDemandProfiles\\MediumPenetrationProfiles\\Mid\\DemandProfile4MedMid.xlsx"
    int_demandprofiles[4] = "C:\\Users\\pwrlab07\\Desktop\\ToUDemandProfiles\\MediumPenetrationProfiles\\Mid\\DemandProfile5MedMid.xlsx"
    int_demandprofiles[5] = "C:\\Users\\pwrlab07\\Desktop\\ToUDemandProfiles\\MediumPenetrationProfiles\\Mid\\DemandProfile6MedMid.xlsx"
    int_demandprofiles[6] = "C:\\Users\\pwrlab07\\Desktop\\ToUDemandProfiles\\MediumPenetrationProfiles\\Mid\\DemandProfile7MedMid.xlsx"
elif ValueUse == 5:
    int_demandprofiles[0] = "C:\\Users\\pwrlab07\\Desktop\\ToUDemandProfiles\\MediumPenetrationProfiles\\On\\DemandProfile0MedOn.xlsx"
    int_demandprofiles[1] = "C:\\Users\\pwrlab07\\Desktop\\ToUDemandProfiles\\MediumPenetrationProfiles\\On\\DemandProfile1MedOn.xlsx"
    int_demandprofiles[2] = "C:\\Users\\pwrlab07\\Desktop\\ToUDemandProfiles\\MediumPenetrationProfiles\\On\\DemandProfile3MedOn.xlsx"
    int_demandprofiles[3] = "C:\\Users\\pwrlab07\\Desktop\\ToUDemandProfiles\\MediumPenetrationProfiles\\On\\DemandProfile4MedOn.xlsx"
    int_demandprofiles[4] = "C:\\Users\\pwrlab07\\Desktop\\ToUDemandProfiles\\MediumPenetrationProfiles\\On\\DemandProfile5MedOn.xlsx"
    int_demandprofiles[5] = "C:\\Users\\pwrlab07\\Desktop\\ToUDemandProfiles\\MediumPenetrationProfiles\\On\\DemandProfile6MedOn.xlsx"
    int_demandprofiles[6] = "C:\\Users\\pwrlab07\\Desktop\\ToUDemandProfiles\\MediumPenetrationProfiles\\On\\DemandProfile7MedOn.xlsx"
elif ValueUse == 6:
    int_demandprofiles[0] = "C:\\Users\\pwrlab07\\Desktop\\ToUDemandProfiles\\HighPenetrationProfiles\\Off\\DemandProfile0HighOff.xlsx"
    int_demandprofiles[1] = "C:\\Users\\pwrlab07\\Desktop\\ToUDemandProfiles\\HighPenetrationProfiles\\Off\\DemandProfile1HighOff.xlsx"
    int_demandprofiles[2] = "C:\\Users\\pwrlab07\\Desktop\\ToUDemandProfiles\\HighPenetrationProfiles\\Off\\DemandProfile3HighOff.xlsx"
    int_demandprofiles[3] = "C:\\Users\\pwrlab07\\Desktop\\ToUDemandProfiles\\HighPenetrationProfiles\\Off\\DemandProfile4HighOff.xlsx"
    int_demandprofiles[4] = "C:\\Users\\pwrlab07\\Desktop\\ToUDemandProfiles\\HighPenetrationProfiles\\Off\\DemandProfile5HighOff.xlsx"
    int_demandprofiles[5] = "C:\\Users\\pwrlab07\\Desktop\\ToUDemandProfiles\\HighPenetrationProfiles\\Off\\DemandProfile6HighOff.xlsx"
    int_demandprofiles[6] = "C:\\Users\\pwrlab07\\Desktop\\ToUDemandProfiles\\HighPenetrationProfiles\\Off\\DemandProfile7HighOff.xlsx"
elif ValueUse == 7:
    int_demandprofiles[0] = "C:\\Users\\pwrlab07\\Desktop\\ToUDemandProfiles\\HighPenetrationProfiles\\Mid\\DemandProfile0HighMid.xlsx"
    int_demandprofiles[1] = "C:\\Users\\pwrlab07\\Desktop\\ToUDemandProfiles\\HighPenetrationProfiles\\Mid\\DemandProfile1HighMid.xlsx"
    int_demandprofiles[2] = "C:\\Users\\pwrlab07\\Desktop\\ToUDemandProfiles\\HighPenetrationProfiles\\Mid\\DemandProfile3HighMid.xlsx"
    int_demandprofiles[3] = "C:\\Users\\pwrlab07\\Desktop\\ToUDemandProfiles\\HighPenetrationProfiles\\Mid\\DemandProfile4HighMid.xlsx"
    int_demandprofiles[4] = "C:\\Users\\pwrlab07\\Desktop\\ToUDemandProfiles\\HighPenetrationProfiles\\Mid\\DemandProfile5HighMid.xlsx"
    int_demandprofiles[5] = "C:\\Users\\pwrlab07\\Desktop\\ToUDemandProfiles\\HighPenetrationProfiles\\Mid\\DemandProfile6HighMid.xlsx"
    int_demandprofiles[6] = "C:\\Users\\pwrlab07\\Desktop\\ToUDemandProfiles\\HighPenetrationProfiles\\Mid\\DemandProfile7HighMid.xlsx"
elif ValueUse == 8:
    int_demandprofiles[0] = "C:\\Users\\pwrlab07\\Desktop\\ToUDemandProfiles\\HighPenetrationProfiles\\On\\DemandProfile0HighOn.xlsx"
    int_demandprofiles[1] = "C:\\Users\\pwrlab07\\Desktop\\ToUDemandProfiles\\HighPenetrationProfiles\\On\\DemandProfile1HighOn.xlsx"
    int_demandprofiles[2] = "C:\\Users\\pwrlab07\\Desktop\\ToUDemandProfiles\\HighPenetrationProfiles\\On\\DemandProfile3HighOn.xlsx"
    int_demandprofiles[3] = "C:\\Users\\pwrlab07\\Desktop\\ToUDemandProfiles\\HighPenetrationProfiles\\On\\DemandProfile4HighOn.xlsx"
    int_demandprofiles[4] = "C:\\Users\\pwrlab07\\Desktop\\ToUDemandProfiles\\HighPenetrationProfiles\\On\\DemandProfile5HighOn.xlsx"
    int_demandprofiles[5] = "C:\\Users\\pwrlab07\\Desktop\\ToUDemandProfiles\\HighPenetrationProfiles\\On\\DemandProfile6HighOn.xlsx"
    int_demandprofiles[6] = "C:\\Users\\pwrlab07\\Desktop\\ToUDemandProfiles\\HighPenetrationProfiles\\On\\DemandProfile7HighOn.xlsx"
elif ValueUse == 9:
    int_demandprofiles[0] = "C:\\Users\\pwrlab07\\Desktop\\ToUDemandProfiles\\Hosting\\Low\\DemandProfile0LowHost.xlsx"
    int_demandprofiles[1] = "C:\\Users\\pwrlab07\\Desktop\\ToUDemandProfiles\\Hosting\\Low\\DemandProfile1LowHost.xlsx"
    int_demandprofiles[2] = "C:\\Users\\pwrlab07\\Desktop\\ToUDemandProfiles\\Hosting\\Low\\DemandProfile3LowHost.xlsx"
    int_demandprofiles[3] = "C:\\Users\\pwrlab07\\Desktop\\ToUDemandProfiles\\Hosting\\Low\\DemandProfile4LowHost.xlsx"
    int_demandprofiles[4] = "C:\\Users\\pwrlab07\\Desktop\\ToUDemandProfiles\\Hosting\\Low\\DemandProfile5LowHost.xlsx"
    int_demandprofiles[5] = "C:\\Users\\pwrlab07\\Desktop\\ToUDemandProfiles\\Hosting\\Low\\DemandProfile6LowHost.xlsx"
    int_demandprofiles[6] = "C:\\Users\\pwrlab07\\Desktop\\ToUDemandProfiles\\Hosting\\Low\\DemandProfile7LowHost.xlsx"
elif ValueUse == 10:
    int_demandprofiles[0] = "C:\\Users\\pwrlab07\\Desktop\\ToUDemandProfiles\\Hosting\\Medium\\DemandProfile0MedHost.xlsx"
    int_demandprofiles[1] = "C:\\Users\\pwrlab07\\Desktop\\ToUDemandProfiles\\Hosting\\Medium\\DemandProfile1MedHost.xlsx"
    int_demandprofiles[2] = "C:\\Users\\pwrlab07\\Desktop\\ToUDemandProfiles\\Hosting\\Medium\\DemandProfile3MedHost.xlsx"
    int_demandprofiles[3] = "C:\\Users\\pwrlab07\\Desktop\\ToUDemandProfiles\\Hosting\\Medium\\DemandProfile4MedHost.xlsx"
    int_demandprofiles[4] = "C:\\Users\\pwrlab07\\Desktop\\ToUDemandProfiles\\Hosting\\Medium\\DemandProfile5MedHost.xlsx"
    int_demandprofiles[5] = "C:\\Users\\pwrlab07\\Desktop\\ToUDemandProfiles\\Hosting\\Medium\\DemandProfile6MedHost.xlsx"
    int_demandprofiles[6] = "C:\\Users\\pwrlab07\\Desktop\\ToUDemandProfiles\\Hosting\\Medium\\DemandProfile7MedHost.xlsx"
elif ValueUse == 11:
    int_demandprofiles[0] = "C:\\Users\\pwrlab07\\Desktop\\ToUDemandProfiles\\Hosting\\High\\DemandProfile0HighHost.xlsx"

    int_demandprofiles[1] = "C:\\Users\\pwrlab07\\Desktop\\ToUDemandProfiles\\Hosting\\High\\DemandProfile1HighHost.xlsx"
    int_demandprofiles[2] = "C:\\Users\\pwrlab07\\Desktop\\ToUDemandProfiles\\Hosting\\High\\DemandProfile3HighHost.xlsx"
    int_demandprofiles[3] = "C:\\Users\\pwrlab07\\Desktop\\ToUDemandProfiles\\Hosting\\High\\DemandProfile4HighHost.xlsx"
    int_demandprofiles[4] = "C:\\Users\\pwrlab07\\Desktop\\ToUDemandProfiles\\Hosting\\High\\DemandProfile5HighHost.xlsx"
    int_demandprofiles[5] = "C:\\Users\\pwrlab07\\Desktop\\ToUDemandProfiles\\Hosting\\High\\DemandProfile6HighHost.xlsx"
    int_demandprofiles[6] = "C:\\Users\\pwrlab07\\Desktop\\ToUDemandProfiles\\Hosting\\High\\DemandProfile7HighHost.xlsx"

winter_loadings_filename = "C:\\Users\\pwrlab07\\PycharmProjects\\PGEPython\\INPUT\\FEEDER_LoadAllocation_Winter_Historical Loading.xlsx"
summer_loadings_filename = "C:\\Users\\pwrlab07\\PycharmProjects\\PGEPython\\INPUT\\FEEDER_LoadAllocation_Summer_Historical Loading.xlsx"
loadings_simulation_year_summer = 2016
loadings_simulation_year_winter = 2016

#cutsheet_filepath = r"C:\Users\pwrlab07\PycharmProjects\PGEPython\INPUT\\"
cutsheet_filepath = 'C:\\Users\\pwrlab07\\Cutsheets\\EmergencySwitchingSheets\\2018EmergencyCutsheets\\'
cutsheet_keywords = ["Mulino"]

temp_cutsheet_store_path = r"C:\temp\temp_cutsheet.csv"

# *********************************************
# PLEASE indicate Reports NEEDED
# *********************************************
winter_overload_report_filename = "C:\\Users\\pwrlab07\\PycharmProjects\\PGEPython\\OUTPUT\\Overload_Winter_Analysis_data.csv"
summer_overload_report_filename = "C:\\Users\\pwrlab07\\PycharmProjects\\PGEPython\\OUTPUT\\Overload_Summer_Analysis_data.csv"

feeder_normal_overload_plot_filename = "C:\\Users\\pwrlab07\\PycharmProjects\\PGEPython\\OUTPUT\\Feeder_Normal_Overload_Plot.png"
feeder_feeder_overload_plot_filename = "C:\\Users\\pwrlab07\\PycharmProjects\\PGEPython\\OUTPUT\\Feeder_Worst_N1Feeder_Overload_Plot.png"
feeder_transformer_overload_plot_filename = "C:\\Users\\pwrlab07\\PycharmProjects\\PGEPython\\OUTPUT\\Feeder_Worst_N1Transformer_Overload_Plot.png"
transformer_normal_overload_plot_filename = "C:\\Users\\pwrlab07\\PycharmProjects\\PGEPython\\OUTPUT\\Transformer_Normal_Overload_Plot.png"
transformer_feeder_overload_plot_filename = "C:\\Users\\pwrlab07\\PycharmProjects\\PGEPython\\OUTPUT\\Transformer_Worst_N1Feeder_Overload_Plot.png"
transformer_transformer_overload_plot_filename = "C:\\Users\\pwrlab07\\PycharmProjects\\PGEPython\\OUTPUT\\Transformer_Worst_N1Transformer_Overload_Plot.png"

loading_tables_filename = "C:\\Users\\pwrlab07\\PycharmProjects\\PGEPython\\OUTPUT\\Loading_Tables.xlsx"

loading_report_needed = True
loading_report_filename = "C:\\Users\\pwrlab07\\PycharmProjects\\PGEPython\\OUTPUT\\Load_Analysis_data.csv"

unbalanced_voltage_report_needed = False
unbalanced_voltage_report_filename = "C:\\Users\\pwrlab07\\PycharmProjects\\PGEPython\\OUTPUT\\Voltage_Analysis_data.csv"

short_circuit_report_needed = False
short_circuit_report_filename = "C:\\Users\\pwrlab07\\PycharmProjects\\PGEPython\\OUTPUT\\ShortCircuit_Analysis_data.csv"

cyme_report_needed = False
cyme_report_filename = "C:\\Users\\pwrlab07\\PycharmProjects\\PGEPython\\OUTPUT\\cyme_analysis_data.xlsx"

# *********************************************
# PLEASE indicate if you would like to SAVE CHANGES to Self Contain
# *********************************************
save_contingency_selfcontained = False
contingency_selfcontained_store_dir = "C:\\Users\\pwrlab07\\PycharmProjects\\PGEPython\\OUTPUT\\"

saving_selfcontained_needed = False
