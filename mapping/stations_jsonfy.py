#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import codecs

csvfile = "meta_traffic_stations_latlon.csv"

if __name__ == "__main__":
    stations = []
    with codecs.open(csvfile, 'r', encoding='utf8') as f:
        lines = [l for l in f]

    for l in lines[1:]:
        print l.split(';')
        code, lam_code, name_tsa, name_fi, lat, lon = l.split(';')[0:6]
        stations.append({'code'    : int(code),
                         'lam_code': int(lam_code),
                         'name_fi' : name_fi,
                         'name_tsa': name_tsa,
                         'lat'     : float(lat),
                         'lon'     : float(lon)})

    with codecs.open('meta_traffic_stations.json', 'w', encoding='utf8') as f:
        json.dump(stations, f, ensure_ascii=False)

