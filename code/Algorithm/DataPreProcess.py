import numpy as np
import pandas as pd
import datetime
import time
import glob

# Data describe & variant binding
DataPath = "../../data/csse_covid_19_data/"
SeriesDataPath = DataPath + "csse_covid_19_time_series/"
DailyPath = DataPath + "csse_covid_19_daily_reports_us/"
DailyNum = len(glob.glob(DailyPath + "*.csv"))  # Counting Datafiles


def dateRange(beginDate, num):
    """
    Date range generating function.
    """
    dates = []
    i = 0
    dt = datetime.datetime.strptime(beginDate, "%Y-%m-%d")
    date = beginDate[:]
    while i < num:
        dates.append(date)
        dt = dt + datetime.timedelta(1)
        date = dt.strftime("%Y-%m-%d")
        i += 1
    return dates


def TillLast(begin, num):
    PassedTime = dateRange(begin, num)
    # Time format transform
    for i in range(len(PassedTime)):
        raw = PassedTime[i]
        year = raw[0:4]
        month = raw[5:7]
        day = raw[8:]
        PassedTime[i] = month + '-' + day + '-' + year
    return PassedTime


def UIDclear(df):
    df = df[(df["UID"] >= 84000000) &
            (df["UID"] <= 84000056) &
            (df["UID"] != 84000002)]  # RULE: Including only 50 province states of America mainland.
    return df

def PreProcess():
    # Inspecting all feature in all datafiles due to data-incongruence
    datelist = TillLast('2020-04-12', DailyNum)  # Generate all datafiles` timetoken list

    featureSet = set()
    date = datelist[0]  # Using first datafile`s features as base feature set
    filePath = DailyPath + date + ".csv"
    f = open(filePath, 'r')
    dailyData = pd.read_csv(f)
    dailyData = UIDclear(dailyData)
    featureSet = featureSet.union(set(list(dailyData)))

    for date in datelist:
        filePath = DailyPath + date + ".csv"
        f = open(filePath, 'r')
        dailyData = pd.read_csv(f)
        dailyData = UIDclear(dailyData)
        featureSet = featureSet & set(list(dailyData))  # Enumerate all datafile to get common features within it

    # Delete missing data column
    commonFeatureList = list(featureSet)
    for date in datelist:
        filePath = DailyPath + date + ".csv"
        with open(filePath, 'r') as f:
            dailyData = pd.read_csv(f)
            dailyData = UIDclear(dailyData)
            for feature in commonFeatureList:
                if dailyData[feature].isnull().all():
                    commonFeatureList.remove(feature)  # Enumerate all datafile to get lagged features removed

    filePath = DailyPath + datelist[0] + ".csv"  # Using the first datafile as name-lat-long source
    f = open(filePath, 'r')
    dailyData = pd.read_csv(f)
    dailyData = UIDclear(dailyData)
    IncidentRateTimeSeries = pd.DataFrame(columns=["Province_State", "Lat", "Long_"])
    TestingRateTimeSeries = pd.DataFrame(columns=["Province_State", "Lat", "Long_"])

    # Transform series to list to avoid index aligning problems
    TestingRateTimeSeries["Province_State"] = IncidentRateTimeSeries["Province_State"] = \
        dailyData["Province_State"].tolist()

    TestingRateTimeSeries["Lat"] = IncidentRateTimeSeries["Lat"] = \
        dailyData["Lat"].tolist()

    TestingRateTimeSeries["Long_"] = IncidentRateTimeSeries["Long_"] = \
        dailyData["Long_"].tolist()

    for date in datelist:
        filePath = DailyPath + date + ".csv"
        with open(filePath, 'r') as f:
            dailyData = pd.read_csv(f)
            dailyData = UIDclear(dailyData)
            TestingRateTimeSeries[date] = dailyData["Testing_Rate"].tolist()
            IncidentRateTimeSeries[date] = dailyData["Incident_Rate"].tolist()

    TestingRateTimeSeries.to_csv("../../data/TestingRateTimeSeries.csv",index=False)
    IncidentRateTimeSeries.to_csv("../../data/IncidentRateTimeSeries.csv",index=False)

if __name__=="__main__":
    PreProcess()