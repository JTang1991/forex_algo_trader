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