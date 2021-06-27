import datetime
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


def DateStartFrom(begin,DayNum):
    PassedTime = dateRange(begin, DayNum)
    # Time format transform
    for i in range(len(PassedTime)):
        raw = PassedTime[i]
        year = raw[0:4]
        month = raw[5:7]
        day = raw[8:]
        PassedTime[i] = (month + '-' + day + '-' + year,PassedTime[i])
    return PassedTime


def UIDclear(df):
    df = df[(df["UID"] >= 84000000) &
            (df["UID"] <= 84000056)]  # RULE: Including only 50 province states of America mainland.
    return df


def commonFeature(datelist):
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

