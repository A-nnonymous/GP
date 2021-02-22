import datetime
import json

import numpy as np
import requests
from pyecharts import options as opts
from pyecharts.charts import Geo
from pyecharts.globals import ChartType


def Rep():
    lines = []
    with open("place.txt", mode='r', encoding='gbk') as ef:
        while True:
            line = ef.readline()
            if not line:
                break
            line = line.strip('\n')
            lines.append(line)
    return lines


def catch():
    url = 'https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5'
    data = json.loads(requests.get(url=url).json()['data'])
    distb = data['areaTree'][0]
    growth = data['chinaDayList']
    provinces = distb['children']
    cityTotalConfirm = {}
    cityTotalSuspect = {}
    cityTotalDead = {}
    cityTotalHeal = {}
    cityTodayConfirm = {}
    cityTodaySuspect = {}
    cityTodayDead = {}
    cityTodayHeal = {}

    for province in provinces:
        for city in province['children']:
            cityTotalConfirm.update({city['name']: city['total']['confirm']})
            cityTotalSuspect.update({city['name']: city['total']['suspect']})
            cityTotalDead.update({city['name']: city['total']['dead']})
            cityTotalHeal.update({city['name']: city['total']['heal']})
            cityTodayConfirm.update({city['name']: city['today']['confirm']})
            cityTodaySuspect.update({city['name']: city['today']['suspect']})
            cityTodayDead.update({city['name']: city['today']['dead']})
            cityTodayHeal.update({city['name']: city['today']['heal']})
    return cityTodayConfirm, \
           cityTodaySuspect, \
           cityTodayDead, \
           cityTodayHeal, \
           cityTotalConfirm, \
           cityTotalSuspect, \
           cityTotalDead, \
           cityTotalHeal


def geo_heatmap(k, v) -> Geo:
    try:
        c = Geo()
        c.add_schema(maptype="china")
        c.add(
            "ratio",
            [list(z) for z in zip(k, v)],
            type_=ChartType.HEATMAP,
        )
    except TypeError:
        print("地址有误，开始排错......")
        with open("place.txt", mode="a") as f:
            i = 0
            c = Geo()
            c.add_schema(maptype="china")
            while i < len(k):
                try:
                    c.add(
                        "ratio",
                        [list(z) for z in zip(k[:i], v[:i])],
                        type_=ChartType.HEATMAP,
                    )
                except:
                    print(k[i - 1])
                    f.writelines(k[i - 1])
                    f.writelines('\n')
                    del k[i - 1]
                    del v[i - 1]
                    i -= 1
                    continue
                else:
                    i += 1
        geo_heatmap(k,v)
    else:
        c.set_series_opts(label_opts=opts.LabelOpts(is_show=False))
        timen = datetime.datetime.now().strftime('%Y-%m-%d')
        timea = datetime.datetime.now().strftime('%Y-%m-%d %H.%M.%S')
        c.set_global_opts(visualmap_opts=opts.VisualMapOpts(),
                          title_opts=opts.TitleOpts(title="2019nCoV{} BY PZW".format(timen))
                          )

        Geo.render(c, path='{}HEATMAP.html'.format(timea))
        print('渲染完毕')


def main(raw=0):
    tdc, tds, tdd, tdh, ttc, tts, ttd, tth = catch()
    cities, numbers = list(ttc.keys()), list(tdc.values())
    k, v = [], []
    ep = Rep()
    for i in range(len(cities)):
        if cities[i] != '地区待确认' and cities[i] not in ep:
            k.append(cities[i])
            v.append(numbers[i])
        else:
            continue
    if raw == 0:
        v = np.array(v)
        v = np.log2(v+1)*10
        v = list(v)
    else:
        pass
    geo_heatmap(k, v)


if __name__ == '__main__':
    main()