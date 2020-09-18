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
import numpy as np, pandas as pd, os, json, sys, logging, time

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
from oandapyV20.contrib.requests import TakeProfitDetails
from oandapyV20.contrib.requests import TrailingStopLossDetails
from oandapyV20.contrib.requests import StopLossDetails

## Config
from config.global_config import vOrdersPath,vRatesPath


################################################################################################################
## Oanda API Live Rate Call Function
## ---------------------------------
## Fuction will call the Oanda v20 API function to return any forex pair for your specified timeframe at that 
## moment in time
################################################################################################################
def oanda_api_live_call(vPair, vTimeframe, vToken, vCount = 5000):
    if vCount > 5000:
        print('Max Records returned is at 5000 records, setting to 5000')
        vCount = 5000

    api = API(access_token = vToken)

    params = {"count" : int(vCount), "granularity" : vTimeframe}
    r = v20instruments.InstrumentsCandles(instrument=vPair,params=params)
    response_json = api.request(r)['candles']
    response_data = pd.json_normalize(response_json)
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
    response_data = pd.json_normalize(response_json)

    return response_data



################################################################################################################
## Oanda Market Order API Execute Function
## ---------------------------------------
## Fuction execute spot market order request with define instrument, units, TP, SL or TSL
## Execution Order and the Successful Order JSON will be captured and store into the Orders Folder
################################################################################################################
def oanda_market_order_request(vAccountID, vToken, vInstrument, vUnits, vTakeProfitPrice = 0, vStopLossPrice = 0, vTrailingStopLoss = 0):
    TP = TakeProfitDetails(price=float(vTakeProfitPrice)).data if vTakeProfitPrice != 0 else None
    SL = StopLossDetails(price=float(vStopLossPrice)).data if vStopLossPrice != 0 else None
    TSL = TrailingStopLossDetails(distance=float(vTrailingStopLoss)).data if vTrailingStopLoss != 0 else None
    vExecutionTime = time.strftime("%Y%m%d_%H%M%S")

    client = oandapyV20.API(access_token=vToken)
    mo = MarketOrderRequest(instrument=vInstrument, units=int(vUnits), takeProfitOnFill=TP, stopLossOnFill=SL, trailingStopLossOnFill=TSL)
    r = orders.OrderCreate(vAccountID, data=mo.data)
    rv = client.request(r)

    market_order = pd.json_normalize(mo.data)
    transaction = pd.json_normalize(rv)
    market_order.to_csv(os.path.join(vOrdersPath,vInstrument + '_MO_' + vExecutionTime + '.txt', sep='|'))
    transaction.to_csv(os.path.join(vOrdersPath,vInstrument + '_MT_' + vExecutionTime + '.txt', sep='|'))

    return market_order, transaction



################################################################################################################
## Oanda Close Order API Execute Function
## --------------------------------------
## Fuction execute spot market order request to close with define instrument, units, by placing an opposite order
## with the same number of units.
## Execution Order and the Successful Order JSON will be captured and store into the Orders Folder
################################################################################################################
def oanda_close_position_request(vAccountID, vToken, vInstrument, vUnits):
    client = oandapyV20.API(access_token=vToken)
    ordr = PositionCloseRequest(longUnits=int(vUnits)) if int(vUnits) >=0 else PositionCloseRequest(shortUnits=int(vUnits))
    r = positions.PositionClose(vAccountID, instrument=vInstrument,data=ordr.data)
    rv = client.request(r)
    vExecutionTime = time.strftime("%Y%m%d_%H%M%S")

    close_order = pd.json_normalize(ordr.data)
    transaction = pd.json_normalize(rv)
    close_order.to_csv(os.path.join(vOrdersPath,vInstrument + '_CO_' + vExecutionTime + '.txt', sep='|'))
    transaction.to_csv(os.path.join(vOrdersPath,vInstrument + '_CT_' + vExecutionTime + '.txt', sep='|'))


    return close_order, transaction
    
