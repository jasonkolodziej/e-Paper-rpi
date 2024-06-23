


import io
import logging
import os
from src import SystemStatus, Network, NetworkInterface
from lib.waveshare_epd import epd2in13_V4 as epd_board
from PIL import Image, ImageDraw, ImageFont
import sys, time, random

fontdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'python/font')
# print(fontdir)
font24 = ImageFont.truetype(os.path.join(fontdir, 'Font.ttc'), 24)

def clear_and_sleep(epd):
    logging.info("Clear...")
    epd.init()
    epd.Clear(0xFF)
    logging.info("Goto Sleep...")
    epd.sleep()
    
logging.basicConfig(level=logging.DEBUG)

if __name__ == '__main__':
    try:
        logging.info("Executing main.py...")
        epd = epd_board.EPD()
        logging.info("init and Clear")
        epd.init_fast()
        # epd.Clear(0xFF, 0)
        # partial(epd)
        s = SystemStatus()
        network: Network = s.network
        network.display(epd)
        time.sleep(300)
        clear_and_sleep(epd)
        # for net in network.network_ifaces:
        #     print(net.header)
        #     print(net.details)
        # s.generate_qr()
        # print(s.to_json())
    except IOError as e:
        logging.info(e)
        clear_and_sleep(epd)
    except KeyboardInterrupt:    
        logging.info("ctrl + c:")
        epd_board.epdconfig.module_exit(cleanup=True)
        exit()
