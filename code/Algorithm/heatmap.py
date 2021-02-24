import datetime
import json

import numpy as np
import requests
from pyecharts import options as opts
from pyecharts.charts import Geo
from pyecharts.globals import ChartType


def catch():
    pass

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
    k, v = [], []
    geo_heatmap(k, v)


if __name__ == '__main__':
    main()