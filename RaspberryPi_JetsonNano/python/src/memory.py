from psutil._common import bytes2human
import psutil
import logging

from .utils import Detail, SystemSubSystem


class Memory(SystemSubSystem):
    __name__ = "Memory"
    def __init__(self):
        super().__init__(header=Detail("Memory"))
        logging.debug("collecting memory usage")
        self.virtual = psutil.virtual_memory()
        self.swap = psutil.swap_memory()
    
    def update(self):
        self.virtual = psutil.virtual_memory()
        self.swap = psutil.swap_memory()
    
    def __repr__(self):
        return u'<{}>  total: {}, used: {}, available: {}, used_percentage: {}%, swap_used_percentage: {}%'.format(
            self.__name__, 
            bytes2human(self.virtual.total),
            bytes2human(self.virtual.used),
            bytes2human(self.virtual.available),
            self.virtual.percent,
            self.swap.percent
        )
    
    def __dict__(self):
        return {
            "total": bytes2human(self.virtual.total),
            "used": bytes2human(self.virtual.used),
            "available": bytes2human(self.virtual.available),
            "used_percentage": self.virtual.percent,
            "swap_used_percentage": self.swap.percent
        }