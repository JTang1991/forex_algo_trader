####################################################################################################################################################################
##-- Script Description : Get Live FX Prices for M1 and above timeframes
##-- Sources            : 
##-- Created            : Sep 2020 
##-- Author             : Jason TANG
####################################################################################################################################################################
##-- Amendment History  : 
####################################################################################################################################################################


################################################################################################################
## Python Libraries
################################################################################################################
## Common Libraries
import numpy as np, pandas as pd, os, json

## Oanda Libraries
import oandapyV20
from oandapyV20 import API
# Endpoints
import oandapyV20.endpoints.accounts as accounts 
import oandapyV20.endpoints.instruments as v20instruments
import oandapyV20.endpoints.orders as orders 
import oandapyV20.endpoints.positions as positions
# Requests
from oandapyV20.contrib.requests import PositionCloseRequest
from oandapyV20.contrib.requests import MarketOrderRequest


################################################################################################################
## Variables and Paths
################################################################################################################
token = 'ab76634af1721b2f72a277a400a63ef5-1d702d9778da8a0bda76a049a31aea6e'
accountID = '101-004-16285502-001'


################################################################################################################
## Oanda API Live Rate Call Function
## ---------------------------------
## Fuction will call the Oanda v20 API function to return any forex pair for your specified timeframe
## The function will return a pandas dataframe with a peak and valley signal
################################################################################################################
def oanda_api_live_call(vPair, vTimeframe, vToken, vCount = 5000):
    api = API(access_token = vToken)

    params = {"count" : vCount, "granularity" : vTimeframe}
    r = v20instruments.InstrumentsCandles(instrument=vPair,params=params)
    response_json = api.request(r)['candles']
    response_data = pd.jsons_normalize(response_json)
    response_data.rename({'mid.o' : 'Open',
                    'mid.h' : 'High',
                    'mid.l' : 'Low',
                    'mid.c' : 'Close',
                    'complete' : 'Completed'}, axis=1, inplace=True)
    response_data['Pair'] = vPair
    response_data['Timeframe'] = vTimeframe

    return response_data



################################################################################################################
## Oanda API Live Account Details Call Function
## --------------------------------------------
## Fuction will call the Oanda v20 API function the latest image of the FX Trading Account
## The function will return a pandas dataframe with a peak and valley signal
################################################################################################################
def oanda_api_acct_info(vAccountID, vToken):
    client = oandapyV20.API(access_token=vToken)
    r = accounts.AccountDetails(vAccountID)
    client.request(r)
    response_json = r.response
    response_data = pd.jsons_normalize(response_json)

    return response_data



################################################################################################################
## Oanda API Live Account Details Call Function
## --------------------------------------------
## Fuction will call the Oanda v20 API function the latest image of the FX Trading Account
## The function will return a pandas dataframe with a peak and valley signal
################################################################################################################
token = 'ab76634af1721b2f72a277a400a63ef5-1d702d9778da8a0bda76a049a31aea6e'
client = oandapyV20.API(access_token=token)
mo = MarketOrderRequest(instrument="EUR_USD", units=10000)
print(json.dumps(mo.data, indent=4)) 

r = orders.OrderCreate(accountID, data=mo.data) 
rv = client.request(r)
print(rv)
print(json.dumps(rv, indent=4)) 



import json
from oandapyV20 import API
import oandapyV20.endpoints.positions as positions
from oandapyV20.contrib.requests import PositionCloseRequest

token = 'ab76634af1721b2f72a277a400a63ef5-1d702d9778da8a0bda76a049a31aea6e'
client = oandapyV20.API(access_token=token)

ordr = PositionCloseRequest(longUnits=10000)
print(json.dumps(ordr.data, indent=4))


r = positions.PositionClose(accountID, instrument="EUR_USD",data=ordr.data)
rv = client.request(r)
print(rv) 