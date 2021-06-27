import datetime
import glob
from PreProUtil import *
import pandas as pd

# Data describe & variant binding
DataPath = "../../data/csse_covid_19_data/"
SeriesDataPath = DataPath + "csse_covid_19_time_series/"
DailyPath = DataPath + "csse_covid_19_daily_reports_us/"
DailyNum = len(glob.glob(DailyPath + "*.csv"))  # Counting Datafiles


def PreProcess():
    # Inspecting all feature in all datafiles due to data-incongruence
    datelist = DateStartFrom('2020-04-12',DailyNum)  # Generate all datafiles` timetoken list

    filePath = DailyPath + datelist[0] + ".csv"  # Using the first datafile as name-lat-long source
    f = open(filePath, 'r')
    dailyData = pd.read_csv(f)
    dailyData = UIDclear(dailyData)
    DeathsTimeSeries = pd.DataFrame(columns=["Province_State", "Lat", "Long_"])
    ConfirmedTimeSeries = pd.DataFrame(columns=["Province_State", "Lat", "Long_"])

    # Transform series to list to avoid index aligning problems
    ConfirmedTimeSeries["Province_State"] = DeathsTimeSeries["Province_State"] = \
        dailyData["Province_State"].tolist()

    ConfirmedTimeSeries["Lat"] = DeathsTimeSeries["Lat"] = \
        dailyData["Lat"].tolist()

    ConfirmedTimeSeries["Long_"] = DeathsTimeSeries["Long_"] = \
        dailyData["Long_"].tolist()

    for date,_ in datelist:
        filePath = DailyPath + date + ".csv"
        with open(filePath, 'r') as f:
            dailyData = pd.read_csv(f)
            dailyData = UIDclear(dailyData)
            ConfirmedTimeSeries[date] = dailyData["Confirmed"].tolist()
            DeathsTimeSeries[date] = dailyData["Deaths"].tolist()

    ConfirmedTimeSeries.to_csv("../dataPool/ConfirmedTimeSeries.csv", index=False)
    DeathsTimeSeries.to_csv("../dataPool/DeathsTimeSeries.csv", index=False)


if __name__ == "__main__":
    PreProcess()
