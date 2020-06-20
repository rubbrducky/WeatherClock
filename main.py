import requests
import os
import datetime
import xml.etree.ElementTree as ET
from itertools import islice
from PIL import Image, ImageDraw, ImageFont
from waveshare_epd import epd4in2
#import logging
#logging.basicConfig(level=logging.INFO)


fc_URL = "https://www.yr.no/place/Sweden/Stockholm/Stockholm/forecast.xml"
fc_periods = [None]*3
fc_symbols = [None]*3
fc_descriptions = [None]*3
fc_temps = [None]*3
dir = os.path.dirname(os.path.abspath(__file__))
font_large = ImageFont.truetype(os.path.join(dir, 'Roboto-Bold.ttf'), size=120)
font_small = ImageFont.truetype(os.path.join(dir, 'Roboto-Regular.ttf'), size=18)
now = datetime.datetime.now()


# Screen size and positions
SCREEN_WIDTH       = 400
SCREEN_HEIGHT      = 300
time_offset_h = 5
fc_periods_offset_h = 140
fc_descs_offset_h = 245
fc_temps_offset_h = 270

fc_periods_width = 130
fc_periods_offset_w = [5, 135, 265]
fc_symbols_offset = [(20, 155),
                     (150, 155),
                     (280, 155)] # yr's symbols are 100x100 pixels: +(130-100)/2 offset
lines = [(135, 155, 135, 280),
         (265, 155, 265, 280)]

epd = epd4in2.EPD()

def dlNewForecast():

    ## download new file, if successful delete old file if exists
    try:
        fcDL = requests.get(fc_URL)
        if fcDL:
            if os.path.isfile(os.path.join(dir, "forecast.xml")):
                os.remove(os.path.join(dir, "forecast.xml"))
            open(os.path.join(dir, "forecast.xml"),'wb').write(fcDL.content)

    except:
        fcSymbol = "error.png", "error.png", "error.png"

def update_forecast():
    fcTree = ET.parse(os.path.join(dir, "forecast.xml"))
    fcRoot = fcTree.getroot()

    i = 0
    for f in islice(fcRoot.iter("time"),0,3): # next three forecast periods

        # from-to forecast hours
        fc_periods[i] = (f.attrib["from"][11:13] + ' - ' + f.attrib["to"][11:13])

        # weather image codes, descriptions, temps
        for s in f.iter("symbol"):
            fc_symbols[i] = os.path.join(dir + os.sep + "icons" + os.sep + s.attrib["var"] + ".png")
        for s in f.iter("symbol"):
            fc_descriptions[i] = str(s.attrib["name"]).center(15)
        for s in f.iter("temperature"):
            fc_temps[i] = str((s.attrib["value"] + chr(176))).center(15)

        i += 1

def new_clock_image():

    image = Image.new('L',(SCREEN_WIDTH,SCREEN_HEIGHT), 'white')
    draw = ImageDraw.Draw(image)

    current_time = str(now.hour).zfill(2) + ':' + str(now.minute).zfill(2)
    offset_w_centered = (SCREEN_WIDTH - draw.textsize(current_time, font=font_large)[0]) / 2 # center text
    draw.text((offset_w_centered, time_offset_h), current_time, fill='black', font=font_large)
    
    i = 0
    for i in range (0,3):
        fc_symbol = Image.open(fc_symbols[i])
        image.paste(fc_symbol, fc_symbols_offset[i])
        
        offset_w_centered = fc_periods_offset_w[i] + (fc_periods_width - draw.textsize(fc_periods[i], font=font_small)[0]) / 2
        draw.text((offset_w_centered, fc_periods_offset_h), fc_periods[i], fill='rgb(80, 80, 80)', font=font_small)

        offset_w_centered = fc_periods_offset_w[i] + (fc_periods_width - draw.textsize(fc_descriptions[i], font=font_small)[0]) / 2
        draw.text((offset_w_centered, fc_descs_offset_h), fc_descriptions[i], fill='rgb(80, 80, 80)', font=font_small)

        offset_w_centered = fc_periods_offset_w[i] + (fc_periods_width - draw.textsize(fc_temps[i], font=font_small)[0]) / 2
        draw.text((offset_w_centered, fc_temps_offset_h), fc_temps[i], fill='rgb(80, 80, 80)', font=font_small)

        i += 1

    draw.line(lines[0], fill='rgb(170, 170, 170)', width=1)
    draw.line(lines[1], fill='rgb(170, 170, 170)', width=1)
    image.save(os.path.join(dir,'clock.png'))

def update_screen():
    epd.init()
    Himage = Image.open(os.path.join(dir, 'clock.png'))
    epd.display(epd.getbuffer(Himage))
    epd4in2.epdconfig.module_exit()


if __name__ == "__main__":

    try:
        # every new hour, download updated forecast
        if now.minute < 51:
            dlNewForecast()
            #print ('New forecast:', now.hour, ':', now.minute, fc_periods, fc_temps, fc_symbols, fc_descriptions)

        update_forecast()
        new_clock_image()
        update_screen()
        exit(0)

    except:
        exit(0)
