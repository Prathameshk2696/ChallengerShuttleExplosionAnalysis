from pymongo import MongoClient
client = MongoClient("mongodb+srv://nikhilneroor:Lihkin2103@cluster0-k2u7z.mongodb.net/test?retryWrites=true&w=majority")
mydb = client["DBDSdata"]
mycoll = mydb.challenger
import numpy as np
import statistics
from collections import Counter
from decimal import Decimal
total_count = mycoll.count_documents({},{})
count = mycoll.count_documents({"O-Ring failure" : "0"} ,{})
count_percent = (count/total_count)*100

ltArr = []
def Average(ltArr):
    return sum(ltArr)/len(ltArr)

for item in mycoll.find():
    launch_temperature = float(item["Launch temperature"])
    ltArr.append(launch_temperature)
print(ltArr)
ltArr.sort()

minimum = ltArr[0]
maximum = ltArr[-1]
range = maximum - minimum
mean = Average(ltArr)
#median = statistics.median(map(Decimal,ltArr))
median = statistics.median(map(Decimal,ltArr))
mode = statistics.mode(ltArr)
stdDev = statistics.pstdev(ltArr)
variance = np.power(stdDev,2)
coeff_var = (stdDev/mean)*100

print("The number of elements with O-Ring failure = 0 is " +str(count)+ " and the corresponding count percent is " +str(count_percent))
print("Minimum = {}".format(minimum))
print("Maximum = {}".format(maximum))
print("Range = " +str(range))
print("Mean = " +str(mean))
print("Median = " +str(median))
print("Mode = " +str(mode))
print("Standard Deviation = " +str(stdDev))
print("Variance = " +str(variance))
print("Coefficient of Variation = " +str(coeff_var))
 