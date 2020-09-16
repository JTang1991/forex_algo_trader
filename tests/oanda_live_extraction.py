## Import Libraries
from __future__ import print_function

import numpy as np
import pandas as pd
import os
import json
import oandapyV20
from oandapyV20 import API
import oandapyV20.endpoints.instruments as v20instruments
from collections import OrderedDict


## Paths and Variables
vPath = os.getcwd() + '\FX_Rates_Historical'

token = '5384f34ef2a9fe1200c27a0740f051bc-f0d6c51e28018b134176f89e32cabf57'
accountID = 'JTang123456789'

instruments = ["GBP_USD", "USD_JPY","EUR_USD",
               "USD_CHF","USD_CAD","AUD_USD","NZD_USD"]
time_frames = ['M1','M5','M30','H1','H4','D']

## API Details and 
api = API(access_token=token)


for tf in time_frames:
    for instr in instruments:
        
        params = {
          "count": 5000,
          "granularity": tf,
          "start" : "2017-03-27T21:00:00"
        }
        
        r = v20instruments.InstrumentsCandles(instrument=instr,params=params)
        data =  api.request(r)
        data = data['candles']
        data = pd.json_normalize(data)
        data.drop(columns={'complete'},inplace=True)
        data.rename({'mid.o' : 'Open',
                    'mid.h' : 'High',
                    'mid.l' : 'Low',
                    'mid.c' : 'Close'}, axis=1, inplace=True)
        data['Pair'] = instr
        vFile = os.path.join(vPath, instr + '_' + tf + '.csv')
        data.to_csv(vFile)
        del data
