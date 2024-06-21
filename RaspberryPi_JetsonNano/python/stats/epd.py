#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

import logging
from waveshare_epd import epd3in7
import time
from PIL import Image, ImageDraw, ImageFont
import traceback
#? Jason's imports
import psutil
from psutil._common import bytes2human
import socket

def create_image(epd, style='horizontal'):
    if style == 'vertical':
        return Image.new('L', (epd.width, epd.height), 0xFF)  #? 0xFF: clear the frame
    else:
     return Image.new('L', (epd.height, epd.width), 0xFF)  #? 0xFF: clear the frame

def vertical(epd) -> tuple[int, int]:
    return (epd.width, epd.height)

def horizontal(epd) -> tuple[int, int]:
    return (epd.height, epd.width)
    

def one(epd):
    #? Drawing on the Horizontal image
    logging.info("1.Drawing on the Horizontal image...")
    Himage = Image.new('L', horizontal(epd), 0xFF)  #? 0xFF: clear the frame
    draw = ImageDraw.Draw(Himage)
    draw.text((10, 0), 'hello world', font = font24, fill = 0)
    draw.text((10, 20), '3.7inch e-Paper', font = font24, fill = 0)
    draw.rectangle((10, 110, 154, 146), 'black', 'black')
    draw.text((10, 110), u'微雪电子', font = font36, fill = epd.GRAY1)
    draw.text((10, 150), u'微雪电子', font = font36, fill = epd.GRAY2)
    draw.text((10, 190), u'微雪电子', font = font36, fill = epd.GRAY3)
    draw.text((10, 230), u'微雪电子', font = font36, fill = epd.GRAY4)
    draw.line((20, 50, 70, 100), fill = 0)
    draw.line((70, 50, 20, 100), fill = 0)
    draw.rectangle((20, 50, 70, 100), outline = 0)
    draw.line((165, 50, 165, 100), fill = 0)
    draw.line((140, 75, 190, 75), fill = 0)
    draw.arc((140, 50, 190, 100), 0, 360, fill = 0)
    draw.rectangle((80, 50, 130, 100), fill = 0)
    draw.chord((200, 50, 250, 100), 0, 360, fill = 0)
    epd.display_4Gray(epd.getbuffer_4Gray(Himage))
    time.sleep(5)

def two(epd):
    logging.info("2.read 4 Gray bmp file")
    Himage = Image.open(os.path.join(picdir, '3in7_4gray2.bmp'))
    epd.display_4Gray(epd.getbuffer_4Gray(Himage))
    time.sleep(5)

def three(epd):
    logging.info("3.read bmp file on window")
    Himage2 = Image.new('1', horizontal(epd), 255)  # 255: clear the frame
    bmp = Image.open(os.path.join(picdir, '100x100.bmp'))
    Himage2.paste(bmp, (200,50))
    epd.display_4Gray(epd.getbuffer_4Gray(Himage2))
    time.sleep(5)

def four(epd):
    #? Drawing on the Vertical image
    logging.info("4.Drawing on the Vertical image...")
    Limage = Image.new('L', vertical(epd), 0xFF)  #? 0xFF: clear the frame
    draw = ImageDraw.Draw(Limage)
    draw.text((2, 0), 'hello world', font = font18, fill = 0)
    draw.text((2, 20), '3.7inch epd', font = font18, fill = 0)
    draw.rectangle((130, 20, 274, 56), 'black', 'black')
    draw.text((130, 20), u'微雪电子', font = font36, fill = epd.GRAY1)
    draw.text((130, 60), u'微雪电子', font = font36, fill = epd.GRAY2)
    draw.text((130, 100), u'微雪电子', font = font36, fill = epd.GRAY3)
    draw.text((130, 140), u'微雪电子', font = font36, fill = epd.GRAY4)
    draw.line((10, 90, 60, 140), fill = 0)
    draw.line((60, 90, 10, 140), fill = 0)
    draw.rectangle((10, 90, 60, 140), outline = 0)
    draw.line((95, 90, 95, 140), fill = 0)
    draw.line((70, 115, 120, 115), fill = 0)
    draw.arc((70, 90, 120, 140), 0, 360, fill = 0)
    draw.rectangle((10, 150, 60, 200), fill = 0)
    draw.chord((70, 150, 120, 200), 0, 360, fill = 0)
    epd.display_4Gray(epd.getbuffer_4Gray(Limage))
    time.sleep(5)


    
def five(epd, runtime=20):
    #? partial update, just 1 Gary mode
    logging.info("5.show time, partial update, just 1 Gary mode")
    epd.init(1)         # 1 Gary mode
    epd.Clear(0xFF, 1)
    time_image = Image.new('1', horizontal(epd), 255)
    time_draw = ImageDraw.Draw(time_image)
    num = 0
    while (True):
        time_draw.rectangle((10, 10, 120, 50), fill = 255)
        time_draw.text((10, 10), time.strftime('%H:%M:%S'), font = font24, fill = 0)
        epd.display_1Gray(epd.getbuffer(time_image))
        
        num = num + 1
        if(num == runtime):
            break

class PiStats:
    font36 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 36)
    font24 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 24)
    font18 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 18)
    font16 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 16)
    font14 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 14)
    font12 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 12)
    af_map = {
        socket.AF_INET: 'IPv4',
        socket.AF_INET6: 'IPv6',
        psutil.AF_LINK: 'MAC',
    }
    duplex_map = {
        psutil.NIC_DUPLEX_FULL: "full",
        psutil.NIC_DUPLEX_HALF: "half",
        psutil.NIC_DUPLEX_UNKNOWN: "?",
    }
    up_map = {
        True: u'✓',
        False: u'✕'
    }
    def __init__(self, epd):
        self.epd = epd
        self.network_ifaces: dict[str, list[psutil.snicaddr]] = psutil.net_if_addrs().items()
        self.network_stats: dict[str, psutil.snicstats] = psutil.net_if_stats()
    
    def edp_init(self):
        self.epd.init(0)
        self.epd.Clear(0xFF, 0) #? 0xFF: clear the frame, 0: 4Gray (opts: or 1: 1Gray)
    def filter_stats(self, 
                     include_broadcast:bool = False, include_netmask: bool = False,
                     include_ptp: bool = False, include_io_count: bool = False):
        """
        A clone of 'ifconfig' on UNIX.
        ```
            $ python3 scripts/ifconfig.py
            lo:
                stats          : speed=0MB, duplex=?, mtu=65536, up=yes
                incoming       : bytes=1.95M, pkts=22158, errs=0, drops=0
                outgoing       : bytes=1.95M, pkts=22158, errs=0, drops=0
                IPv4 address   : 127.0.0.1
                     netmask   : 255.0.0.0
                IPv6 address   : ::1
                     netmask   : ffff:ffff:ffff:ffff:ffff:ffff:ffff:ffff
                MAC  address   : 00:00:00:00:00:00
        ```
        Args:
            include_broadcast (bool, optional): include broadcast value. Defaults to False.
            include_netmask (bool, optional): include netmask value. Defaults to False.
            include_ptp (bool, optional): include ptp value. Defaults to False.
            include_io_count (bool, optional): include stats on network packet drop, etc. Defaults to False.
        """
        Himage = Image.new('L', horizontal(epd), 0xFF)  #? 0xFF: clear the frame
        draw = ImageDraw.Draw(Himage)
        x = 0
        y = 0
        logging.info("Filter network info")
        stats = self.network_stats
        io_counters = psutil.net_io_counters(pernic=True) if include_io_count else None
        for nic, addrs in self.network_ifaces:
            x = 0
            font = self.font18
            if "docker" in nic or nic == "lo":
                continue
            #? Stats
            mb_speed = stats[nic].speed if nic in stats else None
            duplex = self.duplex_map[stats[nic].duplex] if nic in stats else None
            mtu = stats[nic].mtu if nic in stats else None
            is_up = self.up_map[stats[nic].isup] if nic in stats else self.up_map[False]
            #? More stats:
            c = format("(%s) %s:" % (is_up, nic))
            logging.debug(c)
            draw.text((x, y), text=c, font=font)
            y += font.size
            for addr in addrs:
                x = 30
                font = self.font16
                if addr.family == socket.AF_INET6: #? just get ipv4 and MAC
                    continue
                # data = str.format(" {} address: {}", self.af_map.get(addr.family, addr.family), addr.address )
                data = format("%-4s  address: %s" % (self.af_map.get(addr.family, addr.family), addr.address))
                logging.debug(data)
                draw.text((x,y), text=data, font=font)
                y += font.size
                if include_broadcast and addr.broadcast: 
                    data = format("broadcast: %s" % addr.broadcast)
                    logging.debug(data)
                    draw.text((x,y), text=data, font=font)
                    y+=font.size
                if include_netmask and addr.netmask: 
                    data = format("   netmask: %s" % addr.netmask)
                    logging.debug(data)
                    draw.text((x,y), text=data, font=font)
                    y+=font.size
                if include_ptp and addr.ptp: 
                    data = format("       ptp: %s" % addr.ptp)
                    logging.debug(data)
                    draw.text((x,y), text=data, font=font)
                    y+=font.size
  
            #? IO stats:
            if io_counters:
                #? Incoming
                incoming_bytes = bytes2human(io_counters[nic].bytes_recv) if nic in io_counters else None
                incoming_packets = io_counters[nic].packets_recv if nic in io_counters else None
                incoming_errs = io_counters[nic].errin if nic in io_counters else None
                incoming_drops = io_counters[nic].dropin if nic in io_counters else None
                #? Outgoing
                outgoing_bytes = bytes2human(io_counters[nic].bytes_sent) if nic in io_counters else None 
                outgoing_packets = io_counters[nic].packets_sent if nic in io_counters else None
                outgoing_errs = io_counters[nic].errout if nic in io_counters else None
                outgoing_drops = io_counters[nic].dropout if nic in io_counters else None
            
            logging.debug("y incremented to pos: %d", y)  
        epd.display_4Gray(epd.getbuffer_4Gray(Himage))
        time.sleep(300)


logging.basicConfig(level=logging.DEBUG)






try:
    logging.info("epd3in7 Demo")
    epd = epd3in7.EPD()
    logging.info("init and Clear")
    epd.init(0)
    epd.Clear(0xFF, 0) #? 0xFF: clear the frame, 0: 4Gray (opts: or 1: 1Gray)
    
    font36 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 36)
    font24 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 24)
    font18 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 18)
    # four(epd)
    # five(epd, 80)


    # get_network_interfaces(epd, font18)
    pi = PiStats(epd=epd)
    pi.filter_stats()
    
    logging.info("Clear...")
    epd.init(0)
    epd.Clear(0xFF, 0)
    
    logging.info("Goto Sleep...")
    epd.sleep()
    
except IOError as e:
    logging.info(e)
    
except KeyboardInterrupt:    
    logging.info("ctrl + c:")
    epd3in7.epdconfig.module_exit(cleanup=True)
    exit()
