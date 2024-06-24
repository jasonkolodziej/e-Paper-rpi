


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
logging.basicConfig(level=logging.DEBUG)

def clear_and_sleep(epd):
    logging.info("Clear...")
    epd.init()
    epd.Clear() #? 0xFF
    logging.info("Goto Sleep...")
    epd.sleep()
    
def normal_refresh(epd):
    # Normal refresh
    logging.info("Normal refresh...")
    epd.init()


class Drawer:
    def __init__(self, epd:any = None, size:tuple[int, int] = (0,0), vertical:bool = False):
        self.display = epd
        self.size = (self.display.width, self.display.height) if self.display else size
        self.image = Image.new('1', self.vertical(), 0xFF) if vertical else Image.new('1', self.horizontal(), 0xFF)
        self.size = self.image.size
        
    def vertical(self) -> tuple[int, int]:
        return (self.width, self.height)

    def horizontal(self) -> tuple[int, int]:
        return (self.height, self.width)
    
    @property
    def width(self) -> int:
        return self.size[0]
    @property
    def height(self) -> int:
        return self.size[1]
    
    def resize(self, img: Image, width_refactor: int = None, height_refactor: int = 1) -> Image:
        resized = img
        if width_refactor:
            focus_width = int(self.width/width_refactor)
            width_percent = (focus_width/float(img.size[0]))
            height_resize = int((float(img.size[1])*float(width_percent)))
            resized = img.resize((focus_width, height_resize), Image.Resampling.LANCZOS)
        elif height_refactor:
            focus_height = int(self.height/height_refactor)
            height_percent = (focus_height/float(img.size[1]))
            width_resize = int((float(img.size[0])*float(height_percent)))
            resized = img.resize((width_resize, focus_height), Image.Resampling.LANCZOS)
        
        # width, height = size
        # resized = ImageOps.contain(img, size=(100, 100))
        print("width: %d, height: %d" % resized.size)
        return resized
    
    def paste(self, img: Image, x:tuple[bool, int] = (False, 0), y:tuple[bool, int] = (False, 0)):
    # def paste(self, img: Image, pos: tuple[int, int]= (0,0)):
        x = self.width - img.size[0] if x[0] else x[1]
        y = self.height - img.size[1] if y[0] else y[1]
        
        self.image.paste(img, (x, y))
    
    def show(self):
        self.image.show()
    


if __name__ == '__main__':
    try:
        logging.info("Executing main.py...")
        epd = epd_board.EPD()
        logging.info("init and Clear")
        epd.Init_4Gray()
        # epd.Clear(0xFF, 0)
        # partial(epd)
        s = SystemStatus()
        disks = s.disks
        print(disks)
        # s.logo(epd)
        # s.generate_qr(epd)
        # print(s.generate_qr())
        # network: Network = s.network
        # network.display(epd)
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
