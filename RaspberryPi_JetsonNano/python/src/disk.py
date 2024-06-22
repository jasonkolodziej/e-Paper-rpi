

import psutil
from psutil._common import bytes2human, sdiskpart, sdiskusage
from .utils import Detail, SystemSubSystem


class Disk(SystemSubSystem):
    __name__ = "Disk"
    def __init__(self, disk_part: sdiskpart = None):
        super().__init__(header=Detail("Disk"))
        self.disk_part = disk_part
        self.disk_usage: sdiskusage = psutil.disk_usage(self.disk_part.mountpoint)
        # self.disk = self.disk_part._asdict()
        # self.disk.update(self.disk_usage._asdict())

    def update(self):
        self.disk_usage = psutil.disk_usage(self.disk_part.mountpoint)
        # self.disk.update(self.disk_usage._asdict())
    
    def __repr__(self):
        return u'\n\t<{}> mountpoint: {}, total: {}, used: {}, free: {}, used_percentage: {}%'.format(
            self.__name__, 
            self.disk_part.mountpoint,
            bytes2human(self.disk_usage.total),
            bytes2human(self.disk_usage.used),
            bytes2human(self.disk_usage.free),
            self.disk_usage.percent
        )
    
    def __dict__(self):
        return {
            "mountpoint": self.disk_part.mountpoint,
            "total": bytes2human(self.disk_usage.total),
            "used": bytes2human(self.disk_usage.used),
            "free": bytes2human(self.disk_usage.free),
            "used_percentage": self.disk_usage.percent
        }
    
    # def display(self, epd):
    #         print("\nDisk usage of partition ", dp.mountpoint, ": ") 
    #         print("Total: ", int(psutil.disk_usage(dp.mountpoint).total/(1024*1024)), "MB")
    #         print("Used: ", int(psutil.disk_usage(dp.mountpoint).used/(1024*1024)), "MB")
    #         print("Free: ", int(psutil.disk_usage(dp.mountpoint).free/(1024*1024)), "MB")
    #         diskUsagePercent = psutil.disk_usage(dp.mountpoint).percent
    #         print("Used %: ", diskUsagePercent, "%")
    #         if (diskUsagePercent > 60):
    #             print("Sending alert on high disk usage.")


class Disks(SystemSubSystem):
    __name__ = "Disks"
    
    def __init__(self):
        super().__init__(header=Detail("Disks"))
        self.disks: list[Disk] = []
        
        for dp in psutil.disk_partitions():
            self.disks.append(Disk(dp))
    
    def __repr__(self):
        return u'<{}> {}\n'.format(self.__name__, self.disks)
    
    def update(self):
        for disk in self.disks:
            disk.update()

    def __dict__(self):
        return {
            "disks": [disk.__dict__() for disk in self.disks]
        }