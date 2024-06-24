import os
import psutil
from psutil._common import bytes2human
import logging
from PIL import ImageDraw
# from .libs.waveshare_epd import epd2in13_V2
from .utils import Detail, SystemSubSystem

class Processor(SystemSubSystem):
    __name__ = "Processor"
    
    def __init__(self, machine_type: str = None):
        super().__init__(header=Detail("Processor"))
        self.machine_type = os.uname().machine
        logging.debug("collecting cpu usage")
        self.cores:int = psutil.cpu_count(logical=False)
        self.use:float = psutil.cpu_percent()
        self.add_detail(self.short_repr())
        
    def update(self):
        self.details.clear()
        self.use = psutil.cpu_percent()
        self.add_detail(self.short_repr())
        
    def short_repr(self):
        return u'processor: {}, {} cores, usage: {}%'.format(
            self.machine_type,
            self.cores,
            self.use
        )
    
    def display(self, epd, drawer: ImageDraw = None, x: int = 0, y: int = 0) -> tuple[int, int]:
        pass
    
    def __repr__(self):
        return u'<{}> cores: {}, usage: {}%'.format(
            self.__name__, 
            self.cores,
            self.use
        )
    
    def __dict__(self):
        return {
            "cores": self.cores,
            "usage_percent": self.use
        }
        
        # # t1 = timedelta(self.cpu_capture)
        # # usage1 = self.cpu_use
        # # t2 = self.cpu_capture = datetime.now()
        # # self.cpu_use = psutil.cpu_percent()
        # # delta_t = t2 - t1        
        # # delta_usage = self.cpu_use - usage1
        # # logging.debug("in %s CPU usage was at %s %", delta_t.second, delta_usage)
        
        # print("CPU usage %: ", self.cpu_use, "%")
        # print("CPU count: ", self.cpu_cores, "cores")
        # cpuUsagePercent = psutil.cpu_percent(1)
        # print("CPU usage in last 10 secs: ", cpuUsagePercent, "%")
        # # if (cpuUsagePercent > 20):
        #     # print("Sending alert on high cpu usage.")
        #     # alertMsg = {"device_name": os.uname().nodename, "cpu_alert": "cpu usage is high: "+ str(cpuUsagePercent) + "%"}
        #     # sendWebhookAlert(alertMsg)