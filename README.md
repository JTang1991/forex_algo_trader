# forex_algo_trader
This is a forex trading algorithm developed by JTang1991 for learning purposes.
This project is intended to study harmonic patterns and flag Gartley, Butterfly,
Bat and Crab patterns to the user in a backtesting manner or as a live trading
environment. In addition it calculates the P&L payoff in the backtest to 
provide an estimate of the success rate of the patterns.
This is a development program and by no means guranteed to provide returns in 
a live trading setting. The author is not liable for any losses incurred from this 
trading program.


Package Structure

forex_algo_trader
|
|-- __init__.py
|-- __main__.py

|-- forex_algo_trader/
|   |-- __init__.py
|   |-- algo_runner.py
|   |-- surveillance_runner.py
|
|   |   config/
|   |   |-- __init__.py
|   |   |-- global_config.py
|   |   |-- account_config.py
|
|   |   keystore/
|   |   |-- __init__.py
|   |   |-- key.key
|   |   |-- acct_demo.encrypted
|   |   |-- token_demo.encrypted
|   |   |-- acct_live.encrypted
|   |   |-- token_live.encrypted
|
|   |   signals/
|   |   |-- __init__.py
|   |   |-- harmonic_signals.py
|   |   |-- technical_signals.py
|
|   |   execution/
|   |   |-- __init__.py
|   |   |-- oanda_api_functions.py
|
|   |   risk_management/
|   |   |-- __init__.py
|   |   |-- surveillance.py
|   |   |-- risk_triggers.py
|   |   |-- kill_function.py
|

|-- notebooks/

|-- tests/
|   |-- __init__.py
|   |-- oanda_historical_extraction.py
|   |-- harmonic_signals.py
|   |-- technical_signals.py
|   |-- pl_calculator.py


|-- LICENSE
|-- README.md