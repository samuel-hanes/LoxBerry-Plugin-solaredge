#!/usr/bin/python3

import os
import socket
import logging
from configparser import ConfigParser
import json
try:
    from solaredge_interface.api.SolarEdgeAPI import SolarEdgeAPI
except:
    print("Failed to load SolarEdgeAPI")
    return

def send_udp(MINISERVER_IP, UDP_PORT, MESSAGE):
    """ """
    try:
        # start the server listening on UDP socket
        sock = socket.socket( socket.AF_INET, socket.SOCK_DGRAM )
        sock.sendto( MESSAGE.encode('ascii'), (MINISERVER_IP, UDP_PORT) )
    except:
        logging.error("<ERROR> Failed to send message to miniserver socket!")
        logging.debug("<DEBUG> Message: ", MESSAGE)

def main():
    """loxberry plugin for solaredge PV API sends every 5 minutes the actual
    power production value to the miniserver"""
    # create file strings from os environment variables
    lbplog = os.environ['LBPLOG'] + "/synology/solaredge.log"
    lbpconfig = os.environ['LBPCONFIG'] + "/solaredge/plugin.cfg"
    lbsconfig = os.environ['LBSCONFIG'] + "/general.cfg"

    # creating log file and set log format
    logging.basicConfig(filename=lbplog,level=logging.DEBUG,format='%(asctime)s: %(message)s ')
    logging.info("<INFO> initialise logging...")
    # open config file and read options
    try:
        cfg = ConfigParser()
        global_cfg = ConfigParser()
        cfg.read(lbpconfig)
        global_cfg.read(lbsconfig)
    except:
        logging.error("<ERROR> Error parsing config files...")

    #define variables with values from config files
    apiKey = cfg.get("SOLAREDGE", "API_KEY")
    location = cfg.get("SOLAREDGE", "LOCATION")
    miniserver = global_cfg.get("MINISERVER1", "IPADDRESS")
    udp_port = int(cfg.get("MINISERVER", "PORT"))

    try:
        api = SolarEdgeAPI(api_key=apiKey, datetime_response=True, pandas_response=False)
        response = api.get_site_current_power_flow(location)
        y = json.loads(response.text)
        curPwr = y['siteCurrentPowerFlow']['PV']['currentPower']
        unit = y['siteCurrentPowerFlow']['unit']
        msg = str(curPwr)
    except:
        logging.error("<ERROR> Failed to execute API call...")
        msg = None

    if msg != None:
        send_udp(miniserver, udp_port, msg)
    else:
        logging.info("<INFO> Nothing sent to Miniserver IP", miniserver)


if __name__ == "__main__":
    main()
