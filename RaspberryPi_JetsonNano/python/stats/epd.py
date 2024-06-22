import sys
import os
import time
import logging
picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
fontdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'font')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')

if os.path.exists(libdir):
    sys.path.append(libdir)

import logging
from typing import Callable
from waveshare_epd import epd3in7, epdconfig
# from datetime import timedelta, datetime, time
import traceback
#? Jason's imports
import psutil
from psutil._common import bytes2human
from PIL import Image, ImageDraw, ImageFont, ImageOps
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


class GRAYS:
    GRAY1  = 0xff #* white
    WHITE  = GRAY1
    GRAY2  = 0xC0 #* Close to white
    GRAY3  = 0x80 #* Close to black
    GRAY4  = 0x00 #* black
    BLACK  = GRAY4
    CLEAR  = 0xFF #* Clear Frame

class PiStats:
    def Font(size:int = 36, for_unicode:bool = False, font_file_name:str = 'Ubuntu-Regular.ttf'):
        f = 'Font.ttc' if for_unicode else font_file_name
        return ImageFont.truetype(os.path.join(fontdir, f), size=size) 
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
    
    def __init__(self, epd, exit_cb: Callable):
        self.epd = epd
        self.__on_exit__ = exit_cb
        # self.epd_init()
        #? network stats
        self.network_ifaces: dict[str, list[psutil.snicaddr]] = psutil.net_if_addrs().items()
        self.network_stats: dict[str, psutil.snicstats] = psutil.net_if_stats()
        #? cpu stats
        # self.cpu_capture: datetime = datetime.now()
        self.cpu_use: float = psutil.cpu_percent()
        self.cpu_cores: int = psutil.cpu_count()
        #? mem stats
        self.memory_stats: psutil.svmem = psutil.virtual_memory()
        #? logo
        self.name = os.uname()
        logging.debug(self.name)
        self.logo_image: Image = Image.open(os.path.join(picdir, 'ubuntu-logo.bmp'))
        self.logo_image_width, self.logo_image_height = self.logo_image.size
    
    def resize_logo(self, size: tuple[int, int] = (100, 100)):
        self.logo_image = ImageOps.contain(self.logo_image, size=size)
        self.logo_image_width, self.logo_image_height = self.logo_image.size
        logging.debug("width: %d, height: %d", self.logo_image_width, self.logo_image_height)
        
    def logo(self):
        logging.info("Read logo file on window")
        Himage2 = Image.new('1', horizontal(self.epd), 255)  # 255: clear the frame
        self.resize_logo()
        Himage2.paste(self.logo_image, (self.epd.width + self.logo_image_width, 0))
        self.epd.display_4Gray(self.epd.getbuffer_4Gray(Himage2))
        time.sleep(50)
    
    def write_text(self, text:str = ''): 
        Himage = Image.new('L', horizontal(epd), 0xFF)  #? 0xFF: clear the frame
        draw = ImageDraw.Draw(Himage)
        draw.text((10, 0), text='', font = self.font48, fill = 0)
        draw.text((10, 50), '', font = font24, fill = 0)
        epd.display_4Gray(epd.getbuffer_4Gray(Himage))
        time.sleep(300)
        
    def network(self, 
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
            font = PiStats.Font(16)
            sFont = PiStats.Font(16, for_unicode=True)
            if "docker" in nic or nic == "lo":
                continue
            #? Stats
            mb_speed = stats[nic].speed if nic in stats else None
            duplex = self.duplex_map[stats[nic].duplex] if nic in stats else None
            mtu = stats[nic].mtu if nic in stats else None
            is_up = self.up_map[stats[nic].isup] if nic in stats else self.up_map[False]
            #? More stats:
            c = format("        %s:" %  nic)
            draw.text((x,y), text=format("(%s)" % is_up), font=sFont)
            logging.debug(c)
            draw.text((x, y), text=c, font=font)
            y += font.size
            for addr in addrs:
                x = 30
                font = PiStats.Font(14)
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

    def cpu_usage(self):
        logging.debug("collecting cpu usage")
        cores = self.cpu_cores
        
        # t1 = timedelta(self.cpu_capture)
        # usage1 = self.cpu_use
        # t2 = self.cpu_capture = datetime.now()
        # self.cpu_use = psutil.cpu_percent()
        # delta_t = t2 - t1        
        # delta_usage = self.cpu_use - usage1
        # logging.debug("in %s CPU usage was at %s %", delta_t.second, delta_usage)
        
        print("CPU usage %: ", self.cpu_use, "%")
        print("CPU count: ", self.cpu_cores, "cores")
        cpuUsagePercent = psutil.cpu_percent(1)
        print("CPU usage in last 10 secs: ", cpuUsagePercent, "%")
        # if (cpuUsagePercent > 20):
            # print("Sending alert on high cpu usage.")
            # alertMsg = {"device_name": os.uname().nodename, "cpu_alert": "cpu usage is high: "+ str(cpuUsagePercent) + "%"}
            # sendWebhookAlert(alertMsg)
    
    def memory_usage(self):
        logging.debug("collecting memory usage")
        total = bytes2human(self.memory_stats.total)
        used = bytes2human(self.memory_stats.used)
        used_percent = self.memory_stats.percent
        avail = bytes2human(self.memory_stats.available)
        swap_mem_percent = psutil.swap_memory().percent
        logging.debug("Total: %s\nUsed: %s\n Avail:%s\n", total, used, avail)
        # print("Mem Total:", int(psutil.virtual_memory().total/(1024*1024)), "MB")
        # print("Mem Used:", int(psutil.virtual_memory().used/(1024*1024)), "MB")
        # print("Mem Available:", int(psutil.virtual_memory().available/(1024*1024)), "MB")
        # memUsagePercent = 
        print("Mem Usage %:", used_percent, "%")
        print("Swap Usage %:", swap_mem_percent, "%")
        # if (memUsagePercent > 80):
        #     print("Sending alert on high memory usage.")
        #     alertMsg = {"device_name": os.uname().nodename, "memory_alert": "memory usage is high: "+ str(memUsagePercent) + "%"}
            # sendWebhookAlert(alertMsg)

    def disk_usage(self):
        for dp in psutil.disk_partitions():
            # print(x)
            print("\nDisk usage of partition ", dp.mountpoint, ": ") 
            print("Total: ", int(psutil.disk_usage(dp.mountpoint).total/(1024*1024)), "MB")
            print("Used: ", int(psutil.disk_usage(dp.mountpoint).used/(1024*1024)), "MB")
            print("Free: ", int(psutil.disk_usage(dp.mountpoint).free/(1024*1024)), "MB")
            diskUsagePercent = psutil.disk_usage(dp.mountpoint).percent
            print("Used %: ", diskUsagePercent, "%")
            if (diskUsagePercent > 60):
                print("Sending alert on high disk usage.")
                alertMsg = {"device_name": os.uname().nodename, "disk_alert": "disk usage is high: "+ str(diskUsagePercent) + "%" +" in partition: " + 
                                dp.mountpoint}
                # sendWebhookAlert(alertMsg)

    def current_time(self): 
        #? partial update, just 1 Gary mode
        logging.info("5.show time, partial update, just 1 Gary mode")
        self.epd_init(GRAYS.GRAY1)         # 1 Gary mode
        # epd.Clear(0xFF, 1)
        #? Create 1 px bit horizontal, staring with white
        time_image = Image.new('1', horizontal(epd), 255)
        time_draw = ImageDraw.Draw(time_image)
        num = 0
        while (True):
            time_draw.rectangle((10, 10, 120, 50), fill = 255)
            time_draw.text((10, 10), time.strftime('%H:%M:%S'), font = PiStats.Font(24), fill= GRAYS.GRAY4)
            epd.display_1Gray(epd.getbuffer(time_image))
            num = num + 1
            if(num == 20):
                break
    
    def epd_init(self, mode: GRAYS, color: GRAYS = GRAYS.CLEAR):
        self.epd.init(mode)
        self.epd.Clear(color, mode) #? 0xFF: clear the frame, 0: 4Gray (opts: or 1: 1Gray)
    
    def sleep(self):
        logging.info("Goto Sleep...")
        self.epd.sleep()
    
    def __exit__(self, cleanup:bool = True):
        self.epd.Clear(0xFF, 0)
        return self.__on_exit__(cleanup=cleanup)
        


pi: PiStats = None

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    try:
        logging.info("epd3in7 Demo")
        epd = epd3in7.EPD()
        logging.info("init and Clear")
        epd.init(0)
        epd.Clear(0xFF, 0) #? 0xFF: clear the frame, 0: 4Gray (opts: or 1: 1Gray)
    
    
        font36 = ImageFont.truetype(os.path.join(fontdir, 'Ubuntu-Regular.ttf'), 36)
        font24 = ImageFont.truetype(os.path.join(fontdir, 'Ubuntu-Regular.ttf'), 24)
        font18 = ImageFont.truetype(os.path.join(fontdir, 'Ubuntu-Regular.ttf'), 18)
        # four(epd)
        # five(epd, 80)


        # get_network_interfaces(epd, font18)
        pi = PiStats(epd, epdconfig.module_exit)
        pi.logo()
        # pi.memory_usage()
        # pi.cpu_usage()
        # pi.logo()
        # pi.filter_stats()
        # three(epd)
        
        logging.info("Clear...")
        epd.init(0)
        epd.Clear(0xFF, 0)
        
        
        
    except IOError as e:
        logging.info(e)
        
    except KeyboardInterrupt:    
        logging.info("ctrl + c:")
        pi.__exit__()
        # epdconfig.module_exit(cleanup=True)
        exit()
