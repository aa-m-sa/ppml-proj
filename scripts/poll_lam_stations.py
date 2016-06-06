#!/usr/bin/env python
# -*- coding: utf-8 -*-

import xml.etree.ElementTree as ET
import requests
import json
import datetime
import time

# a hackish script that polls the XML API
# saves data as txt (JSON?)

# loads the station IDs to poll from special textfile stations-to-use.txt

dt = "{http://tie.digitraffic.fi/sujuvuus/schemas}"
dump_path = './lam_dumps/'

wait_long = 10*60
wait_short = 5*60

def store_data(ldr, time_stamp):
    print "storing", time_stamp
    # data
    data = {}
    for d in ldr.find(dt+"lamdynamicdata").findall(dt+"lamdata"):
        lamid = d.find(dt+"lamid").text
        utc  = d.find(dt+"measurementtime").find(dt+"utc").text
        vol1 = d.find(dt+"trafficvolume1").text
        vol2 = d.find(dt+"trafficvolume2").text
        data[lamid] = {"utc": utc, "vol1": float(vol1), "vol2": float(vol2)}


    with open(dump_path + "dump" + time_stamp + ".json", 'w') as dump:
        dump.write(json.dumps(data, indent=2))

while True:
    print "...sending request"
    r = requests.get("http://tie.digitraffic.fi/sujuvuus/ws/lamData")

    prev_ts_utc = None

    if r and r.status_code == 200:
        root = ET.fromstring(r.text)

        #TODO robusteness to be inserted

        ldr = root[0][0] # LamDataResponse
        # timestamp
        ts_utc_text = ldr.find(dt+"timestamp").find(dt+"utc").text
        ts_local_text = ldr.find(dt+"timestamp").find(dt+"localtime").text
        print "got", ts_utc_text
        ts_utc = datetime.datetime.strptime(ts_utc_text, "%Y-%m-%dT%H:%M:%SZ")

        if not prev_ts_utc or (ts_utc - prev_ts_utc).seconds > wait_long:
            prev_ts_utc = ts_utc
            store_data(ldr, datetime.datetime.strftime(ts_utc, "%Y-%m-%dT%H%M"))
    else:
        print "response not ok"
        if r and r.status_code:
            print r.status_code
            if str(r.status_code)[0] in ('4', '5'):
                print "uhuh terminating"
                exit(1)
        else:
            print "panic"
            exit(1)

    print "sleep period"
    time.sleep(wait_short) 
