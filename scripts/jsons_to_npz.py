#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import sys
import os
import numpy as np

# reads jsons from a dir and collects them to numpy arrays
# saved as npz

def add_to_dict(js_obj, np_dt, np_vs):
    for k,obs in js_obj.iteritems():
        tmp_dt = np.datetime64(obs['utc'])
        tmp_vars = np.array([obs['vol1'], obs['vol2']])
        if k not in np_vs:
            np_vs[k] = tmp_vars
            np_dt[k] = tmp_dt
        else:
            np_vs[k] = np.vstack([np_vs[k], tmp_vars])
            np_dt[k] = np.vstack([np_dt[k], tmp_dt])


json_path = sys.argv[1]

files = [n for n in os.listdir(json_path) if n.endswith(".json")]
files = sorted(files)

np_dt = dict()
np_vs = dict()

for f in files:
    fpath = os.path.join(json_path, f)
    print fpath
    with open(fpath, 'r') as dump:
        js_obj = json.load(dump)
        add_to_dict(js_obj, np_dt, np_vs)

np.savez('out_dates', **np_dt)
np.savez('out_vars', **np_vs)
