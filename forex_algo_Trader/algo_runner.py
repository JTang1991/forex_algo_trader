####################################################################################################################################################################
##-- Script Description : Main Algorithmic Trader Application Runner
##-- Sources            : 
##-- Created            : Sep 2020 
##-- Author             : Jason TANG
####################################################################################################################################################################
##-- Amendment History  : 
####################################################################################################################################################################


################################################################################################################
## Python Libraries
################################################################################################################
import sys, os, logging, time
import pandas as pd
from config.global_config import vLogPath, vOrdersPath, vRatesPath
from config.account_config import vAccountID,vAPIToken
from execution import oanda_api_functions
from signals import harmonic_signals


    
#market_order.to_csv(os.path.join(vOrdersPath,vInstrument + '_MO_' + vExecutionTime + '.txt', sep='|'))
#transaction.to_csv(os.path.join(vOrdersPath,vInstrument + '_MT_' + vExecutionTime + '.txt', sep='|'))