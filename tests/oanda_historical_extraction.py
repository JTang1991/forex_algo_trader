import json
from oandapyV20 import API
from oandapyV20.contrib.factories import InstrumentsCandlesFactory
import pandas as pd
import os
import sys


temp = pd.read_csv('Oanda_hist_param.csv')
pair = ['USD_JPY', 'EUR_USD', 'USD_CHF', 'USD_CAD', 'NZD_USD']
interval = [tuple(x) for x in temp.values]


vPath = os.getcwd() + '\FX_Rates_Historical'

token = '5384f34ef2a9fe1200c27a0740f051bc-f0d6c51e28018b134176f89e32cabf57'
accountID = 'JTang123456789'
client = API(access_token=token)



for x in pair:
    for tf,_from,_to in interval:
        
        temp = []
        client = API(access_token=token)
        params = {
                 "from": _from,
                 "to" : _to,
                 "granularity": tf,
                 "count": 2500,
                 }
        for r in InstrumentsCandlesFactory(instrument=x, params=params):
            client.request(r)
            df = pd.json_normalize(r.response.get('candles'))
            temp.append(df)

        final = pd.concat(temp)
        final.rename({'complete' : 'Finalised',
                     'mid.o' : 'Open',
                            'mid.h' : 'High',
                            'mid.l' : 'Low',
                            'mid.c' : 'Close'}, axis=1, inplace=True)
        final['Pair'] = x
        vFile = os.path.join(vPath, x + '_' + tf + '_' + _from[:10] + '_' + _to[:10] + '.csv')
        final.to_csv(vFile)
        print( x + '_' + tf + '_' + _from + '_' + _to)
