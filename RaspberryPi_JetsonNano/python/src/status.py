import logging
import os
import segno
import json
from datetime import datetime
from .disk import Disks
from .cpu import Processor
from .memory import Memory
from .network import Network

class SystemStatus:
    __name__ = "SystemStatus"
    
    def __init__(self):
        logging.info("System Status")
        self.cpu = Processor()
        self.memory = Memory()
        self.network = Network()
        self.disks = Disks()
        self.general: os.uname_result = os.uname()
        
    def update(self):
        self.cpu.update()
        self.memory.update()
        self.network.update()
        logging.info("System Status updated")
    
    # def show_time(self):
    #     import time
    #     from utils import Font
    #     epd.init(1)         # 1 Gray mode
    #     epd.Clear(0xFF, 1)
    #     time_image = Image.new('1', (epd.height, epd.width), 255)
    #     img_draw = ImageDraw.Draw(time_image)
    #     while (True):
    #         time_draw.rectangle((10, 10, 120, 50), fill = 255)
    #         time_draw.text((10, 10), time.strftime('%H:%M:%S'), font = Font(24), fill = 0)
    #         epd.display_1Gray(epd.getbuffer(time_image))
    
    # def display(self, epd):
    #     epd.init()
    #     epd.Clear()
    #     epd.display(self.cpu.image)
    #     epd.display(self.memory.image)
    #     epd.display(self.network.image)
    #     epd.sleep()
    #     logging.info("System Status displayed")
        
    def __del__(self):
        logging.info("System Status deleted")
        del self.cpu
        del self.memory
        del self.network
        del self.disks
    
    def architecture(self):
        return self.general.machine
    
    def hostname(self):
        return self.general.nodename
    
    def os(self):
        return self.general.sysname
    
    def kernel_version(self):
        return self.general.release
    
    def general_repr(self):
        return u'<General>: hostname: {}, architecture: {}, os: {}, kernel_version: {}'.format(
            self.hostname(), self.architecture(), self.os(), self.kernel_version()
        )
    
    def general_dict(self):
        return {
            "hostname": self.hostname(),
            "timestamp": datetime.now().isoformat(),
            "architecture": self.architecture(),
            "os": self.os(),
            "kernel_version": self.kernel_version()
        }
    
    def __dict__(self):
        return {
            "general": self.general_dict(),
            "cpu": self.cpu.__dict__(),
            "memory": self.memory.__dict__(),
            "network": self.network.__dict__(),
            "disks": self.disks.__dict__()
        }
    
    def to_json(self):
        return json.dumps(self.__dict__())
    
    def generate_qr(self):
        segno.make(content=json.dumps(self.general_dict())).save("system_status.png")
    def __repr__(self):
        return u'<{}>\n general: {},\n cpu: {},\n memory: {},\n network: {},\n disks: {}'.format(
            self.__name__, 
            self.general_repr(), 
            self.cpu, 
            self.memory, 
            self.network, 
            self.disks
        )