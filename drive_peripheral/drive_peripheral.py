import argparse
import time
import os
from logging import config, getLogger
from dotenv import load_dotenv
load_dotenv(override=True)


config.fileConfig('logging.conf')
logger = getLogger(__name__)


from ble_peripheral import DrivePeripheral


def run_peripheral():
    peripheral = DrivePeripheral('Drive peripheral')
    logger.info('Starting drive peripheral')
    peripheral.start()
    while True:
        time.sleep(1)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Drive peripheral')
    args = parser.parse_args()
    if hasattr(args, 'help'):
        parser.print_help()
    else:
        run_peripheral()
