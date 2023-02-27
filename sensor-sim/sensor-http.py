#
# Simple, http based sensor data simulator for sending fata Thingsboard IoT Gateway via REST
# Experimental and only for demo purposes
#

import sys
import os
import requests
import json
import argparse
import logging
import urllib3
import random
import time


urllib3.disable_warnings()

#
# Globals
#

tb_gateway = ""
access_token = ""
interval = 5
telemetry_key = ""
telemetry_min = 10
telemetry_max = 20
firmware_version = ""
target_firmware_version = ""
serial_number = ""

# Logging
module = sys.modules['__main__'].__file__
logger = logging.getLogger(module)

# Generates new random value that is within 3% range from previous value
def gen_next_value(prev_value, min_val, max_val): 
    ran = random.random()
    value = prev_value + ((max_val - min_val) * (ran - 0.5)) * 0.03
    value = round(max([min_val, min(max_val, value)]), 2)
    return value


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Sensor simulator')


    parser.add_argument(
            '--server',  type=str, default='http://localhost:5000/my_devices',
            help='Thingsboard Gateway HTTP Endpoint [default: http://localhost:5000/my_devices]')

    parser.add_argument(
            '--token',  type=str, 
            help='ACCESS_TOKEN of the device')    

    parser.add_argument(
            '--interval',  type=int, default=5,
            help='Frequency of submitted data')

    parser.add_argument(
            '--telemetry_key',  type=str, default='temp',
            help='telemetry key [default: temp]' ) 

    parser.add_argument(
            '--telemetry_min',  type=int, default=20,
            help='telemetry min value [default: 20]' ) 

    parser.add_argument(
            '--telemetry_max',  type=int, default=30,
            help='telemetry max value [default: 30]' ) 

    parser.add_argument('-l', '--log-level', default='WARNING',
                                help='Set log level to ERROR, WARNING, INFO or DEBUG')
    
    parser.add_argument(
            '--sensor_name',  type=str, default='Sensor T1',
            help='Sensor name [default: Sensor T1]' ) 

    parser.add_argument(
            '--sensor_model',  type=str, default='IIoT Sensor',
            help='Sensor model [default: IIoT Sensor]' ) 

    parser.add_argument(
            '--firmware_version',  type=str, default='1.0.1',
            help='firmware version [default: 1.0.1]' ) 

    parser.add_argument(
            '--serial_number',  type=str, default='SN-001',
            help='serial_number [default: SN-001]' )             

    args = parser.parse_args()


    #
    # Configure logging
    #


    log_level = os.getenv("LOG_LEVEL", default=args.log_level)

    try:
        logging.basicConfig(stream=sys.stderr, level=log_level, format='%(name)s (%(levelname)s): %(message)s')
    except ValueError:
        logger.error("Invalid log level: {}".format(log_level))
        sys.exit(1)

    logger.info("Log level set: {}".format(logging.getLevelName(logger.getEffectiveLevel())))

    tb_gateway = os.getenv("SERVER", default=args.server)
    access_token = os.getenv("TOKEN", default=args.token)
    sensor_name = os.getenv("NAME", default=args.sensor_name)
    sensor_model = os.getenv("MODEL", default=args.sensor_model)
    interval = int(os.getenv("INTERVAL", default=args.interval))
    telemetry_key = os.getenv("TELEMETRY_KEY", default=args.telemetry_key)
    telemetry_min = int(os.getenv("TELEMETRY_MIN", default=args.telemetry_min))
    telemetry_max = int(os.getenv("TELEMETRY_MAX", default=args.telemetry_max))
    firmware_version = os.getenv("FIRMWARE_VERSION", default=args.firmware_version)
    serial_number = os.getenv("SERIAL_NUMBER", default=args.serial_number)


    headers = {'Content-type': 'application/json'}

    url = tb_gateway 

    telemetry_value = telemetry_min

    while True:
        try:
            telemetry_value =  gen_next_value(telemetry_value, telemetry_min, telemetry_max )
            logger.info("Send telemetry: {},  {}".format(telemetry_key, telemetry_value))
            r = requests.post(url, headers=headers, json={'sensorName': sensor_name, 'sensorModel': sensor_model, 'firmwareVersion': firmware_version, 'serialNumber': serial_number  , telemetry_key: telemetry_value},  verify=False )
            if r.status_code != 200:
                logger.error("http POST faild: {}, Code: {}".format(url, r.status_code))

        except requests.exceptions.RequestException as e:  
            raise SystemExit(e)
        
        time.sleep(interval)