
import logging
import socket
import psutil
from psutil._common import bytes2human, snicstats, snicaddr, snetio
from .utils import Font, SystemSubSystem

# logger = logging.getLogger(__name__)

class NetworkInterface(SystemSubSystem):
    __name__ = "NetworkInterface"
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
    def __init__(self, nic: str, addrs: list[snicaddr], stats: snicstats, io_counters: snetio):
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
        self.nic = nic
        self.is_up: bool = stats.isup if stats else False
        self.addrs: list[snicaddr] = addrs
        self.stats: snicstats = stats
        self.io_counters: snetio = io_counters
    
    def up(self):
        return self.up_map[self.is_up]
    
    def addr_repr(self):
        for addr in self.addrs:
            if addr.family == socket.AF_INET6:
                continue
            yield format("%-4s  address: %s" % (self.af_map.get(addr.family, addr.family), addr.address))
    
    
    def update(self):
        self.addrs = psutil.net_if_addrs().get(self.nic)
        self.stats = psutil.net_if_stats().get(self.nic)
        self.io_counters = psutil.net_io_counters(pernic=True).get(self.nic)
    
    def other_repr(self, include_broadcast:bool = False, include_netmask: bool = False, include_ptp: bool = False):
        for addr in self.addrs:
            if addr.family == socket.AF_INET6:
                continue
            if include_broadcast and addr.broadcast: 
                yield format("broadcast: %s" % addr.broadcast)
            if include_netmask and addr.netmask: 
                yield format("   netmask: %s" % addr.netmask)
            if include_ptp and addr.ptp: 
                yield format("       ptp: %s" % addr.ptp)
    
    def io_repr(self, include_io_count: bool = False):
        if include_io_count:
            incoming_bytes = bytes2human(self.io_counters.bytes_recv) if self.io_counters else None
            incoming_packets = self.io_counters.packets_recv if self.io_counters else None
            incoming_errs = self.io_counters.errin if self.io_counters else None
            incoming_drops = self.io_counters.dropin if self.io_counters else None
            outgoing_bytes = bytes2human(self.io_counters.bytes_sent) if self.io_counters else None 
            outgoing_packets = self.io_counters.packets_sent if self.io_counters else None
            outgoing_errs = self.io_counters.errout if self.io_counters else None
            outgoing_drops = self.io_counters.dropout if self.io_counters else None
            yield format("incoming: bytes=%s, pkts=%s, errs=%s, drops=%s" % (
                incoming_bytes, incoming_packets, incoming_errs, incoming_drops
            ))
            yield format("outgoing: bytes=%s, pkts=%s, errs=%s, drops=%s" % (
                outgoing_bytes, outgoing_packets, outgoing_errs, outgoing_drops
            ))
    
    def __repr__(self):
        return u'\n\t<{}> ({}) {} {}'.format(self.__name__, self.up(), self.nic, list(self.addr_repr()))
    
    def __dict__(self):
        return {
            "nic": self.nic,
            "is_up": self.is_up,
            "addrs": list(self.addr_repr()),
            "stats": self.stats._asdict() if self.stats else None,
            "io_counters": self.io_counters._asdict() if self.io_counters else None
        }
    


class Network(SystemSubSystem):
    __name__ = "Network"
    def __init__(self, 
                include_broadcast:bool = False, include_netmask: bool = False,
                include_ptp: bool = False, include_io_count: bool = False) -> None:
        self.network_ifaces: list[NetworkInterface] = []
        
        logging.info("Filter network info")
        stats = psutil.net_if_stats()
        io_counters = psutil.net_io_counters(pernic=True) if include_io_count else None
        
        for nic, addrs in psutil.net_if_addrs().items():
            if "docker" in nic or "lo" in nic:
                continue
            self.network_ifaces.append(NetworkInterface(nic, addrs, stats.get(nic), io_counters.get(nic) if io_counters else None))
    
    def update(self):
        self.network_ifaces = psutil.net_if_addrs().items()
        self.network_stats = psutil.net_if_stats()
    
    def __repr__(self):
        return u'<{}>\n{}'.format(self.__name__, self.network_ifaces)
    
    def __dict__(self):
        return {
            "network_interfaces": [iface.__dict__() for iface in self.network_ifaces]
        }
    
    # def network(self, 
    #                  ):

    #     # Himage = Image.new('L', horizontal(epd), 0xFF)  #? 0xFF: clear the frame
    #     # draw = ImageDraw.Draw(Himage)
    #     x = 0
    #     y = 0
        
    #     # epd.display_4Gray(epd.getbuffer_4Gray(Himage))
    #     # time.sleep(300)
