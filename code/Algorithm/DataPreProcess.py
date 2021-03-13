import numpy as np
import pandas as pd
import datetime
import time


def dateRange(beginDate, endDate):
    """
    Date range generating function.
    """
    dates = []
    dt = datetime.datetime.strptime(beginDate, "%Y-%m-%d")
    date = beginDate[:]
    while date <= endDate:
        dates.append(date)
        dt = dt + datetime.timedelta(1)
        date = dt.strftime("%Y-%m-%d")
    return dates

def Timeindex(begin):
    #(YYYYnow, MMnow, DDnow) = (time.localtime()[0], time.localtime()[1], time.localtime()[2])
    now=time.strftime("%Y-%m-%d", time.localtime())
    # Get present time string
    PassedTime=dateRange(begin, now)
    for i in range(len(PassedTime)):
        raw=PassedTime[i]
        year=raw[0:4]
        month=raw[5:7]
        day=raw[8:]
        PassedTime[i]=month+'-'+day+'-'+year
    return PassedTime

if __name__ == '__main__':
    DataPath = "../../data/csse_covid_19_data/"
    SeriesDataPath = "csse_covid_19_time_series/"
    DailyPath = "csse_covid_19_daily_reports_us/"
    datelist=Timeindex('2020-04-12')
    for date in datelist:
        filePath=DataPath+DailyPath+date+".csv"
        try:
            with open(filePath, 'r') as f:
                dailyData=pd.read_csv(f)

        except:break




