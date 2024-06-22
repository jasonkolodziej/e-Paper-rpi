


import io
import logging
import os
from src import SystemStatus, Network, NetworkInterface
from lib.waveshare_epd import epd3in7
from PIL import Image, ImageDraw, ImageFont
import sys, time, random
from tqdm import tqdm

fontdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'python/font')
# print(fontdir)
font24 = ImageFont.truetype(os.path.join(fontdir, 'Font.ttc'), 24)


def progressBar(count_value, total, suffix=''):
    bar_length = 10
    filled_up_Length = int(round(bar_length* count_value / float(total)))
    percentage = round(100.0 * count_value/float(total),1)
    bar = '=' * filled_up_Length + '-' * (bar_length - filled_up_Length)
    return str.format("[{}] {}% ...{}", bar, percentage, suffix)

def new_bar(img: Image, x, y, width, height, progress, bg=(129, 66, 97), fg=(211,211,211), fg2=(15,15,15)):
    # Draw the background
    img.draw.rectangle((x+(height/2), y, x+width+(height/2), y+height), fill=255, width=10)
    img.draw.ellipse((x+width, y, x+height+width, y+height), fill=fg2)
    img.draw.ellipse((x, y, x+height, y+height), fill=fg2)
    width = int(width*progress)
    # Draw the part of the progress bar that is actually filled
    img.draw.rectangle((x+(height/2), y, x+width+(height/2), y+height), fill=fg, width=10)
    img.draw.ellipse((x+width, y, x+height+width, y+height), fill=fg)
    img.draw.ellipse((x, y, x+height, y+height), fill=fg)
    
def partial(epd):
    logging.info("5.show time, partial update, just 1 Gary mode")
    epd.init(1)         # 1 Gary mode
    epd.Clear(0xFF, 1)
    time_image = Image.new('1', (epd.height, epd.width), 255)
    img_draw = ImageDraw.Draw(time_image)
    num = 0
    x = y = 10
    width = 100
    height = 25
    for i in range(2):
        progress =  (i/epd.width) * 100 # progressBar(i, 10)
        # progress_wrapper.flush()
        # logging.info(progress)
        # Draw the background
        img_draw.rectangle((x+(height/2), y, x+width+(height/2), y+height), fill=255, width=10)
        img_draw.ellipse((x+width, y, x+height+width, y+height), fill=255)
        img_draw.ellipse((x, y, x+height, y+height), fill=255)
        width = int(width*progress)
        # Draw the part of the progress bar that is actually filled
        img_draw.rectangle((x+(height/2), y, x+width+(height/2), y+height), fill=0, width=10)
        img_draw.ellipse((x+width, y, x+height+width, y+height), fill=0)
        img_draw.ellipse((x, y, x+height, y+height), fill=0)
        
        
        
        # time_draw.rectangle((10, 100, 10, 100), fill = 255)
        # time_draw.text((10, 100), text=progress, font = font24, fill = 0)
        # time_draw.text((10, 10), time.strftime('%H:%M:%S'), font = font24, fill = 0)
        epd.display_1Gray(epd.getbuffer(time_image))
        # time.sleep(random.random())
    
    # while (True):
    #     time_draw.rectangle((10, 10, 120, 50), fill = 255)
    #     time_draw.text((10, 10), time.strftime('%H:%M:%S'), font = font24, fill = 0)
    #     epd.display_1Gray(epd.getbuffer(time_image))
        
        # num = num + 1
        # if(num == 20):
        #     break
            
    logging.info("Clear...")
    epd.init(0)
    epd.Clear(0xFF, 0)
    
    logging.info("Goto Sleep...")
    epd.sleep()

logging.basicConfig(level=logging.DEBUG)

if __name__ == '__main__':
    try:
        # logging.info("Executing main.py...")
        # epd = epd3in7.EPD()
        # logging.info("init and Clear")
        
        # epd.init(0)
        # epd.Clear(0xFF, 0)
        # partial(epd)
        s = SystemStatus()
        # network: Network = s.network
        # for net in network.network_ifaces:
        #     print(net.header)
        #     print(net.details)
        # s.generate_qr()
        print(s.to_json())
    except IOError as e:
        logging.info(e)
    
    except KeyboardInterrupt:    
        logging.info("ctrl + c:")
        epd3in7.epdconfig.module_exit(cleanup=True)
        exit()
