#!/usr/bin/python3

import os
import socket
import logging
from configparser import ConfigParser
import json

def send_udp(MINISERVER_IP, UDP_PORT, MESSAGE):
    """ """
    try:
        # start the server listening on UDP socket
        sock = socket.socket( socket.AF_INET, socket.SOCK_DGRAM )
        sock.sendto( MESSAGE.encode('ascii'), (MINISERVER_IP, UDP_PORT) )
        logging.debug("<DEBUG> Message: ", MESSAGE)
    except:
        logging.error("<ERROR> Failed to send message to miniserver socket!")
        logging.debug("<DEBUG> Message: ", MESSAGE)

def main():
    """loxberry plugin for solaredge PV API sends every 5 minutes the actual
    power production value to the miniserver"""
    # create file strings from os environment variables
    lbplog = os.environ['LBPLOG'] + "/solaredge/solaredge.log"
    lbpconfig = os.environ['LBPCONFIG'] + "/solaredge/plugin.cfg"
    lbsconfig = os.environ['LBSCONFIG'] + "/general.cfg"

    # creating log file and set log format
    logging.basicConfig(filename=lbplog,level=logging.INFO,format='%(asctime)s: %(message)s ')
    # open config file and read options
    try:
        from solaredge_interface.api.SolarEdgeAPI import SolarEdgeAPI
    except:
        logging.error("<ERROR> Error loading SolarEdgeAPI module... exit script")
        return
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
    # comment for local debugging
    miniserver = global_cfg.get("MINISERVER1", "IPADDRESS")
    udp_port = int(cfg.get("MINISERVER", "PORT"))
    # uncomment for local debugging
    #miniserver = "127.0.0.1"
    #udp_port = 15555


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
        logging.info("<INFO> Message sent to Miniserver IP: %s" % miniserver)
    else:
        logging.error("<ERROR> Nothing sent to Miniserver IP: %s" % miniserver)


if __name__ == "__main__":
    main()
