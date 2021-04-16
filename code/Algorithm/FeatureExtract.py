import numpy as np
import pandas as pd

import DataPreProcess as dpp

filePath = "../dataPool/"
confirm="ConfirmedTimeSeries"
death="DeathsTimeSeries"
CRTS = filePath + confirm+".csv"
DRTS = filePath + death+".csv"
datelist = dpp.DateStartFrom("2020-04-12")
dateNum = len(datelist)


def extract(path, daterange,fname):
    f = open(path, "r")
    data = pd.read_csv(f)
    print(path + " opened successfully,start extracting feature...")
    columnTag = []
    for state in data.index:
        name = str(data.iloc[state, :].loc["Province_State"])
        #columnTag.append(name + "_Lat")
        #columnTag.append(name + "_Long")
        for i in range(batchSize):
            columnTag.append(name + str(i + 1) + "day")
    Feature_Size = len(columnTag)
    result = pd.DataFrame(np.zeros([dateNum - batchSize + 1, Feature_Size]), columns=columnTag)
    head = 0
    while (head + batchSize <= dateNum):
        for state in data.index:  # For each state in raw dataset
            name = str(data.iloc[state, :].loc["Province_State"])
            #lat = data.iloc[state].loc["Lat"]
            #long = data.iloc[state].loc["Long_"]
            #result.iloc[head].loc[name + "_Lat"] = lat
            #result.iloc[head].loc[name + "_Long"] = long
            for i in range(batchSize):
                result.iloc[head].loc[name + str(i + 1) + "day"] = data.iloc[state].loc[datelist[head + i]]
        print("Feature extracted {} out of {}".format(head + 1, dateNum - batchSize + 1))
        head += 1
    result.to_csv("./"+fname+ "Feature.csv", index=False)

def Output(path,batchSize,fname):
    f = open(path, "r")
    data = pd.read_csv(f)
    print(path + " opened successfully,start transforming output...")
    tags = data["Province_State"]
    result = data.iloc[:, 2+batchSize:].T
    result.columns = tags
    result.to_csv("./"+fname + "OUT.csv", index=False)
    print("finished.")

if __name__ == "__main__":
    batchSize = 14
    extract(CRTS, batchSize,confirm)
    Output(CRTS,batchSize,confirm)
    extract(DRTS, batchSize,death)
    Output(DRTS,batchSize,death)
