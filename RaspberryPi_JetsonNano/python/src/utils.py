import logging
import os
import sys
from PIL import ImageFont, ImageDraw, Image


# Python program showing
# abstract base class work
from abc import ABC, abstractmethod

picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pics')
fontdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'font')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')

if os.path.exists(libdir):
    sys.path.append(libdir)


def Font(size:int = 36, for_unicode:bool = False, font_file_name:str = 'Ubuntu-Regular.ttf') -> ImageFont.FreeTypeFont:
        f = 'Font.ttc' if for_unicode else font_file_name
        logging.debug(fontdir)
        return ImageFont.truetype(os.path.join(fontdir, f), size=size)

class Detail:
    def __init__(self, text:str, font = Font(18)):
        self.text = text
        self.font = font
    
    def __str__(self):
        return self.text

    def __repr__(self):
        return self.text

def horizontal(epd) -> tuple[int,int]:
    return (epd.height, epd.width)

class SystemSubSystem(ABC):
    
    def __init__(self, header: Detail = None, detail_font_size: int = 12):
        self.header: Detail = header
        self.detail_font_size = detail_font_size
        self.details: list[Detail] = []
        pass
    
    def add_detail(self, text:str):
        self.details.append(Detail(text, Font(self.detail_font_size)))
    
    @abstractmethod
    def update(self):
        pass
    
    @abstractmethod
    def display(self, epd, drawer: ImageDraw, x: int = 0, y: int = 0) -> tuple[int, int]:
        pass
    
    def drawer(self, epd, vertical:bool = False) -> ImageDraw:
        sizing = horizontal(epd) # if vertical is False else vertical(epd)
        self.image = Image.new('1', sizing, 255) #* Image.new('L', sizing, 0xFF) #? 0xFF: clear the frame
        self.draw = ImageDraw.Draw(self.image)
        return self.draw
    
    # @abstractmethod
    # def __del__(self):
    #     pass
    
    @abstractmethod
    def __repr__(self):
        pass
    
    @abstractmethod
    def __name__(self):
        pass