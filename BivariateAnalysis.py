# -*- coding: utf-8 -*-
"""
Created on Sun Apr 26 16:32:06 2020

@author: Prthamesh
"""

from pymongo import MongoClient

client = MongoClient("mongodb+srv://Prathamesh:abcd123@cluster0-gln4i.mongodb.net/test")

db = client["ChallengerDatabase"]

collection = db.ChallengerCollection2

import numpy as np

# Chi2
# Categorical attribute 1: O-ring failure
# Categorical attribute 2: Leak-check pressure
#
arrN = np.zeros(shape=(2,3))
arrE = np.zeros(shape=(2,3))

for item in collection.find():
    o_ring_failure = item["O-Ring failure"]
    leak_check_pressure = item["Leak-check pressure"]
    if o_ring_failure == "0":
        if leak_check_pressure == "Low": 
            arrN[0][0] += 1
        if leak_check_pressure == "Medium": 
            arrN[0][1] += 1
        if leak_check_pressure == "High": 
            arrN[0][2] += 1
    if o_ring_failure == "1":
        if leak_check_pressure == "Low": 
            arrN[1][0] += 1
        if leak_check_pressure == "Medium": 
            arrN[1][1] += 1
        if leak_check_pressure == "High": 
            arrN[1][2] += 1

total = sum(sum(arrN))
for i in range(2):
    for j in range(3):
        arrE[i][j] = (np.sum(arrN[i,:]))*(np.sum(arrN[:,j]))/total
  
arrN_E = arrN-arrE
arrN_E2 = np.power(arrN_E,2)
arrN_E2DE = arrN_E2/arrE 
chi_2 = sum(sum(arrN_E2DE))
print("Chi2 = {}".format(chi_2))

# Z Test
# Numerical attribute is Launch Temperature
# Categorical attribute is O_ring Failure

ltn = []
lty = []

for item in collection.find():
    o_ring_failure = item["O-Ring failure"]
    launch_temperature = int(item["Launch temperature"])
    if o_ring_failure == "0":
        ltn.append(launch_temperature)
    else:
        lty.append(launch_temperature)

launchTemperatureN = np.array(ltn)
launchTemperatureY = np.array(lty)

avgLaunchTemperatureN = np.average(launchTemperatureN)
avgLaunchTemperatureY = np.average(launchTemperatureY)

launchTemperatureN_avg = launchTemperatureN - avgLaunchTemperatureN
launchTemperatureY_avg = launchTemperatureY - avgLaunchTemperatureY

launchTemperatureN_avg_2 = np.power(launchTemperatureN_avg,2)
launchTemperatureY_avg_2 = np.power(launchTemperatureY_avg,2)

varN = np.sum(launchTemperatureN_avg_2)/len(launchTemperatureN_avg_2)
varY = np.sum(launchTemperatureY_avg_2)/len(launchTemperatureY_avg_2)

numerator = avgLaunchTemperatureN - avgLaunchTemperatureY
denominator = (varN/len(launchTemperatureN)+varY/len(launchTemperatureY))**0.5
z = numerator/denominator
print("Z = {}".format(z))

# Linear Correlation
# Numerical attribute 1: Launch temperature 
# Numerical attribute 2: Leak-check pressure numerical

lt = []
lcpn = []

for item in collection.find():
    lt.append(int(item["Launch temperature"]))
    lcpn.append(int(item["Leak-check pressure numerical"]))

launchTemperatures = np.array(lt)
leakCheckPressuresNumerical = np.array(lcpn)

avgLaunchTemperature = np.average(launchTemperatures)
avgLeakCheckPressure = np.average(leakCheckPressuresNumerical)

launchTemperatures_avg = launchTemperatures - avgLaunchTemperature
leakCheckPressure_avg = leakCheckPressuresNumerical - avgLeakCheckPressure

launchTemperatures_avg_2 = np.power(launchTemperatures_avg,2)
leakCheckPressure_avg_2 = np.power(leakCheckPressure_avg,2)

varianceLaunchTemperature = np.sum(launchTemperatures_avg_2)/len(lt)
varianceLeakCheckPressure = np.sum(leakCheckPressure_avg_2)/len(lcpn)

lt_avg_lcp_avg = np.multiply(launchTemperatures_avg, leakCheckPressure_avg)
covariance = np.sum(lt_avg_lcp_avg)/len(lt)

correlation = covariance / ((varianceLaunchTemperature*varianceLeakCheckPressure)**0.5)

print("Correlation = {}".format(correlation))
    