####################################################################################################################################################################
##-- Script Description : Oanda Functions for API calls and Order Execution 
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
import numpy as np, pandas as pd, os, json, sys, logging, pkg_resources

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

## Config
from master_config import *


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
## Oanda API Account Details Call Function
## ---------------------------------------
## Fuction will call the Oanda v20 API function the latest image of the FX Trading Account
################################################################################################################
def oanda_api_acct_info(vAccountID, vToken):
    client = oandapyV20.API(access_token=vToken)
    r = accounts.AccountDetails(vAccountID)
    client.request(r)
    response_json = r.response
    response_data = pd.jsons_normalize(response_json)

    return response_data



################################################################################################################
## Oanda Market Order API Execute Function
## ---------------------------------------
## Fuction execute spot market order request with define instrument, units, TP, SL or TSL
## Execution Order and the Successful Order JSON will be captured and store into the Orders Folder
################################################################################################################
def oanda_market_order_request(vAccountID, vToken, vInstrument, vUnits, vTakeProfit, vStopLoss, vTrailingStopLoss):
    client = oandapyV20.API(access_token=vToken)
    mo = MarketOrderRequest(instrument=vInstrument, units=vUnits)
    r = orders.OrderCreate(vAccountID, data=mo.data)
    rv = client.request(r)
    
print(json.dumps(mo.data, indent=4)) 

r = orders.OrderCreate(accountID, data=mo.data) 
rv = client.request(r)
print(rv)
print(json.dumps(rv, indent=4)) 