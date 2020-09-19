####################################################################################################################################################################
##-- Script Description : Peak Valley Detection and Harmonic Pattern Signal Indicator
##-- Sources            : 
##-- Created            : Sep 2020 
##-- Author             : Jason TANG
####################################################################################################################################################################
##-- Amendment History  : 
####################################################################################################################################################################


################################################################################################################
## Python Libraries
################################################################################################################
import sys
import os
import numpy as np
import pandas as pd


################################################################################################################
## Peak Valley Detector
## --------------------
## Function aims to detect all highs and lows of a given time series with user defined variance. A higher 
## variance mean a larger diference between the two extremas to exist before the two extrema can be identified 
## as peaks and valleys. A default variance is set to 0.01 which can be changed to optimise the model.
## The function will return a pandas dataframe with a peak and valley signal
################################################################################################################
def peak_valley_indicator(vDataframe, vVariance = 0.01, vTrend = False):
    df = vDataframe[['Date','Close']]
    min_value = np.Inf
    max_value = -np.Inf
    min_position = np.NaN
    max_position = np.NaN
    max_finder = True

    for i in range(1, len(df)):
        rate = df.loc[i,'Close']

        if rate > max_value:
            max_value = rate
            max_position = i

        if rate < min_value:
            min_value = rate
            min_position = i

        if max_finder:
            if rate < max_value - vVariance:
                df.loc[max_position, 'Value'] = max_value
                df.loc[max_position, 'Peak_Valley'] = 'Peak'
                min_value = rate
                min_position = i
                max_finder = False
        else:
            if rate > min_value + vVariance:
                df.loc[min_position, 'Value'] = min_value
                df.loc[min_position, 'Peak_Valley'] = 'Valley'
                max_value = rate
                max_position = i
                max_finder = True
    if max_finder:
        df.loc[max_position, 'Value'] = max_value
        df.loc[max_position,' Peak_Valley'] = 'Peak'
        max_finder = False
    else:
        df.loc[min_position, 'Value'] = min_value
        df.loc[min_position, 'Peak_Valley'] = 'Valley'
        max_finder = True

    if max_finder:
        df.loc[len(df)-1, 'Value'] = df.loc[len(df)-1, 'Close']
        df.loc[len(df)-1, 'Peak_Valley'] = 'Peak'
    else:
        df.loc[len(df)-1, 'Value'] = df.loc[len(df)-1, 'Close']
        df.loc[len(df)-1, 'Peak_Valley'] = 'Valley'

    if vTrend == True:
        df.loc[df['Peak_Valley'] == 'Peak', 'Trend'] = 'Downtrend'
        df.loc[df['Peak_Valley'] == 'Valley', 'Trend'] = 'Uptrend'

        for i in range(1, len(df)):
            if (df.loc[i, 'Peak_Valley'] != 'Peak') & (df.loc[i, 'Peak_Valley'] != 'Valley'):
                df.loc[i, 'Trend'] = df.loc[i-1, 'Trend']
        
        df.loc[df['Peak_Valley'].notnull(), 'Trend'] = 'Reversal'

    return df


################################################################################################################
## Harmonic Signals Live Trader
## ----------------------------
## Function aims to detect the following harmonic patterns: Gartley, Butterfly, Bat and Crab for bullish and
## bearish signals. It is used to identify at that moment and previous time interval whether it has identified
## a possible harmonic pattern and alert the user to initiate a trade.
## The function will reutnr a pandas dataframe with the Signal to Long or Short and the Pattern signalled.
################################################################################################################
def harmonic_signal_live_trder(vDataframe, vErrorAllowed = 5.0):
    pattern = vDataframe[vDataframe['Peak_Valley'].notnull()].tail(5)

    if pattern.shape[0] < 4:
        print('Not enough Signals to generate Pattern')
        signals_df = []

    else:
        pattern.reset_index(inplace=True)
        signals=[]
        err_allowed = vErrorAllowed/100

        XA = pattern['Value'][1] - pattern['Value'][0]
        AB = pattern['Value'][2] - pattern['Value'][1]
        BC = pattern['Value'][3] - pattern['Value'][2]
        CD = pattern['Value'][4] - pattern['Value'][3]

        AB_range_gart = np.array([0.618 - err_allowed, 0.618 + err_allowed]) * abs(XA)
        BC_range_gart = np.array([0.382 - err_allowed, 0.886 + err_allowed]) * abs(AB)
        CD_range_gart = np.array([1.272 - err_allowed, 1.618 + err_allowed]) * abs(BC)
        
        AB_range_but = np.array([0.786 - err_allowed, 0.786 + err_allowed]) * abs(XA)
        BC_range_but = np.array([0.382 - err_allowed, 0.886 + err_allowed]) * abs(AB)
        CD_range_but = np.array([1.618 - err_allowed, 2.618 + err_allowed]) * abs(BC)
            
        AB_range_bat = np.array([0.382 - err_allowed, 0.5 + err_allowed]) * abs(XA)
        BC_range_bat = np.array([0.382 - err_allowed, 0.886 + err_allowed]) * abs(AB)
        CD_range_bat = np.array([1.618 - err_allowed, 2.618 + err_allowed]) * abs(BC)
            
        AB_range_crab = np.array([0.382 - err_allowed, 0.618 + err_allowed]) * abs(XA)
        BC_range_crab = np.array([0.382 - err_allowed, 0.886 + err_allowed]) * abs(AB)
        CD_range_crab = np.array([2.24 - err_allowed, 3.618 + err_allowed]) * abs(BC)

        if XA > 0 and AB < 0 and BC > 0 and CD < 0:
            if AB_range_gart[0] < abs(AB) < AB_range_gart[1] and BC_range_gart[0] < abs(BC) < BC_range_gart[1] and CD_range_gart[0] < abs(CD) < CD_range_gart[1]:
                print('Bull Gartley at date : ' + str(pattern['Date'][4]))
                if (pattern['Date'][4] == vDataframe.loc[len(vDataframe)-2,'Date']) | (pattern['Date'][4] == vDataframe.loc[len(vDataframe)-1,'Date']):
                    signals.append(['Long','Gartley',pattern['Date'][0],pattern['Date'][1],pattern['Date'][2],pattern['Date'][3],pattern['Date'][4],pattern['Value'][0],pattern['Value'][1],pattern['Value'][2],pattern['Value'][3],pattern['Value'][4]])
                
            elif AB_range_but[0] < abs(AB) < AB_range_but[1] and BC_range_but[0] < abs(BC) < BC_range_but[1] and CD_range_but[0] < abs(CD) < CD_range_but[1]:
                print('Bull Butterfly at date : ' + str(pattern['Date'][4]))
                if (pattern['Date'][4] == vDataframe.loc[len(vDataframe)-2,'Date']) | (pattern['Date'][4] == vDataframe.loc[len(vDataframe)-1,'Date']):
                    signals.append(['Long','Butterfly',pattern['Date'][0],pattern['Date'][1],pattern['Date'][2],pattern['Date'][3],pattern['Date'][4],pattern['Value'][0],pattern['Value'][1],pattern['Value'][2],pattern['Value'][3],pattern['Value'][4]])
                
            elif AB_range_bat[0] < abs(AB) < AB_range_bat[1] and BC_range_bat[0] < abs(BC) < BC_range_bat[1] and CD_range_bat[0] < abs(CD) < CD_range_bat[1]:
                print('Bull Bat at date : ' + str(pattern['Date'][4]))
                if (pattern['Date'][4] == vDataframe.loc[len(vDataframe)-2,'Date']) | (pattern['Date'][4] == vDataframe.loc[len(vDataframe)-1,'Date']):
                    signals.append(['Long','Bat',pattern['Date'][0],pattern['Date'][1],pattern['Date'][2],pattern['Date'][3],pattern['Date'][4],pattern['Value'][0],pattern['Value'][1],pattern['Value'][2],pattern['Value'][3],pattern['Value'][4]])
                
            elif AB_range_crab[0] < abs(AB) < AB_range_crab[1] and BC_range_crab[0] < abs(BC) < BC_range_crab[1] and CD_range_crab[0] < abs(CD) < CD_range_crab[1]:
                print('Bull Crab at date : ' + str(pattern['Date'][4]))
                if (pattern['Date'][4] == vDataframe.loc[len(vDataframe)-2,'Date']) | (pattern['Date'][4] == vDataframe.loc[len(vDataframe)-1,'Date']):
                    signals.append(['Long','Crab',pattern['Date'][0],pattern['Date'][1],pattern['Date'][2],pattern['Date'][3],pattern['Date'][4],pattern['Value'][0],pattern['Value'][1],pattern['Value'][2],pattern['Value'][3],pattern['Value'][4]])
                
        if XA < 0 and AB > 0 and BC < 0 and CD > 0:
            if AB_range_gart[0] < abs(AB) < AB_range_gart[1] and BC_range_gart[0] < abs(BC) < BC_range_gart[1] and CD_range_gart[0] < abs(CD) < CD_range_gart[1]:
                print('Bear Gartley at date : ' + str(pattern['Date'][4]))
                if (pattern['Date'][4] == vDataframe.loc[len(vDataframe)-2,'Date']) | (pattern['Date'][4] == vDataframe.loc[len(vDataframe)-1,'Date']):
                    signals.append(['Short','Gartley',pattern['Date'][0],pattern['Date'][1],pattern['Date'][2],pattern['Date'][3],pattern['Date'][4],pattern['Value'][0],pattern['Value'][1],pattern['Value'][2],pattern['Value'][3],pattern['Value'][4]])
                
            elif AB_range_but[0] < abs(AB) < AB_range_but[1] and BC_range_but[0] < abs(BC) < BC_range_but[1] and CD_range_but[0] < abs(CD) < CD_range_but[1]:
                print('Bear Butterfly at date : ' + str(pattern['Date'][4]))
                if (pattern['Date'][4] == vDataframe.loc[len(vDataframe)-2,'Date']) | (pattern['Date'][4] == vDataframe.loc[len(vDataframe)-1,'Date']):
                    signals.append(['Short','Butterfly',pattern['Date'][0],pattern['Date'][1],pattern['Date'][2],pattern['Date'][3],pattern['Date'][4],pattern['Value'][0],pattern['Value'][1],pattern['Value'][2],pattern['Value'][3],pattern['Value'][4]])
                
            elif AB_range_bat[0] < abs(AB) < AB_range_bat[1] and BC_range_bat[0] < abs(BC) < BC_range_bat[1] and CD_range_bat[0] < abs(CD) < CD_range_bat[1]:
                print('Bear Bat at date : ' + str(pattern['Date'][4]))
                if (pattern['Date'][4] == vDataframe.loc[len(vDataframe)-2,'Date']) | (pattern['Date'][4] == vDataframe.loc[len(vDataframe)-1,'Date']):
                    signals.append(['Short','Bat',pattern['Date'][0],pattern['Date'][1],pattern['Date'][2],pattern['Date'][3],pattern['Date'][4],pattern['Value'][0],pattern['Value'][1],pattern['Value'][2],pattern['Value'][3],pattern['Value'][4]])
                
            elif AB_range_crab[0] < abs(AB) < AB_range_crab[1] and BC_range_crab[0] < abs(BC) < BC_range_crab[1] and CD_range_crab[0] < abs(CD) < CD_range_crab[1]:
                print('Bear Crab at date : ' + str(pattern['Date'][4]))
                if (pattern['Date'][4] == vDataframe.loc[len(vDataframe)-2,'Date']) | (pattern['Date'][4] == vDataframe.loc[len(vDataframe)-1,'Date']):
                    signals.append(['Short','Crab',pattern['Date'][0],pattern['Date'][1],pattern['Date'][2],pattern['Date'][3],pattern['Date'][4],pattern['Value'][0],pattern['Value'][1],pattern['Value'][2],pattern['Value'][3],pattern['Value'][4]])
                
        else:
            print('No visable pattern')
            signals_df = []

    return signals_df