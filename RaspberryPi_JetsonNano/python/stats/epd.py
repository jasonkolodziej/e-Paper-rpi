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


def get_network_interfaces(epd, font: ImageFont.FreeTypeFont, fill = 0):
    """A clone of 'ifconfig' on UNIX.

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

    docker0:
        stats          : speed=0MB, duplex=?, mtu=1500, up=yes
        incoming       : bytes=3.48M, pkts=65470, errs=0, drops=0
        outgoing       : bytes=164.06M, pkts=112993, errs=0, drops=0
        IPv4 address   : 172.17.0.1
            broadcast : 172.17.0.1
            netmask   : 255.255.0.0
        IPv6 address   : fe80::42:27ff:fe5e:799e%docker0
            netmask   : ffff:ffff:ffff:ffff::
        MAC  address   : 02:42:27:5e:79:9e
            broadcast : ff:ff:ff:ff:ff:ff

    wlp3s0:
        stats          : speed=0MB, duplex=?, mtu=1500, up=yes
        incoming       : bytes=7.04G, pkts=5637208, errs=0, drops=0
        outgoing       : bytes=372.01M, pkts=3200026, errs=0, drops=0
        IPv4 address   : 10.0.0.2
            broadcast : 10.255.255.255
            netmask   : 255.0.0.0
        IPv6 address   : fe80::ecb3:1584:5d17:937%wlp3s0
            netmask   : ffff:ffff:ffff:ffff::
        MAC  address   : 48:45:20:59:a4:0c
            broadcast : ff:ff:ff:ff:ff:ff
    """
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
    stats = psutil.net_if_stats()
    io_counters = psutil.net_io_counters(pernic=True)
    logging.info("5.show network info, horizontal, just 1 Gary mode")
    
    Himage = Image.new('L', horizontal(epd), 0xFF)  #? 0xFF: clear the frame
    draw = ImageDraw.Draw(Himage)
    x = 10
    y = 0
    y_increment = font.size
    for nic, addrs in psutil.net_if_addrs().items():
        if "docker" in nic or nic == "lo":
            continue

        is_up = stats[nic].isup if nic in stats else False
        # print(c)
        # if nic in stats:
            # st = stats[nic]
        #     print("    stats          : ", end='')
        #     print(
        #         "speed=%sMB, duplex=%s, mtu=%s, up=%s"
        #         % (
        #             st.speed,
        #             duplex_map[st.duplex],
        #             st.mtu,
        #             "yes" if st.isup else "no",
        #         )
        #     )
        # if nic in io_counters:
        #     io = io_counters[nic]
        #     print("    incoming       : ", end='')
        #     print(
        #         "bytes=%s, pkts=%s, errs=%s, drops=%s"
        #         % (
        #             bytes2human(io.bytes_recv),
        #             io.packets_recv,
        #             io.errin,
        #             io.dropin,
        #         )
        #     )
        #     print("    outgoing       : ", end='')
        #     print(
        #         "bytes=%s, pkts=%s, errs=%s, drops=%s"
        #         % (
        #             bytes2human(io.bytes_sent),
        #             io.packets_sent,
        #             io.errout,
        #             io.dropout,
        #         )
        #     )
        c = format("(%s) %-1s:" % (u'✓' if is_up else u'✕', nic))
        logging.debug(c)
        draw.text((x, y), text=c, font=font)
        y += y_increment
        for addr in addrs:
            if addr.family == socket.AF_INET6: #? just get ipv4 and MAC
                continue
            c = format("      %-4s" % af_map.get(addr.family, addr.family))
            c += format(" address : %s" % addr.address)
            draw.text((x, y), text=c, font=font)
            y += y_increment
            logging.debug(c)
            # if addr.broadcast:
            #     print("         broadcast : %s" % addr.broadcast)
            # if addr.netmask:
            #     print("         netmask   : %s" % addr.netmask)
            # if addr.ptp:
            #     print("      p2p       : %s" % addr.ptp)
            
        logging.debug("y incremented to: %d", y)   
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


    get_network_interfaces(epd, font18)
    
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
