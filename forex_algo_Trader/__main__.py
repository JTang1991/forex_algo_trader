import logging, threading, os, schedule, time
from config.global_config import vScriptPath,vLogPath

def title(name):
    name = ' ' + name + ' '
    logging.info('='*100)
    logging.info('='*35 + name.ljust(65,'='))
    logging.info('='*100)

logdate = time.strftime("%Y%m%d_%H%M%S")
logging.basicConfig(filename= vLogPath + 'forex_algo_trader.log', level=logging.DEBUG,
                        format="%(asctime)s - %(levelname)s - %(message)s", datefmt='%Y-%m-%d %H:%M:%S')

title('Forex Algorithmic Trader Initiated')
logging.info('\n')


class RunThread(threading.Thread):
    def __init__(self, command):
        threading.Thread.__init__(self)
        self.cmd = command

    def run(self):
        logging.info("Initiating " + self.cmd)
        os.system(self.cmd)
        logging.info("Exiting " + self.cmd)

def run_multithreading(vList):
    for x in range(len(vList)):
        RunThread(vList[x]).start()

if __name__ == '__main__':
    run_list = [
        'python ' + vScriptPath + '/algo_runner.py',
        'python ' + vScriptPath + '/surveillance_runner.py'
    ]

    schedule.every(30).minutes.do(run_multithreading(run_list))

    while True:
        schedule.run_pending()
        time.sleep(1)