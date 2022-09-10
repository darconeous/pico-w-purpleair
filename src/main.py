import machine
import framebuf
import time
import network
import struct
import LCD_1inch14
import urequests
from utime import sleep

from writer import CWriter
import freesans20
import arial_50

from settings import purpleair_url,wifi_ssid,wifi_pass,ntp_host

def get_sensor_data():
    r = urequests.get(purpleair_url)
    try:
        return r.json()
    finally:
        r.close()

def get_aqi_from_data(data):
    aqi = (int(data["pm2.5_aqi"])+int(data["pm2.5_aqi_b"]))/2
    print("pm2.5_aqi_a:%d pm2.5_aqi_b:%d"%(int(data["pm2.5_aqi"]),int(data["pm2.5_aqi_b"])))
    return aqi

def fg_color_from_aqi(aqi):
    if (aqi<100):
        return [0,0,0]
    return [255,255,255]

def bg_color_from_aqi(aqi):
    if (aqi<0):
        return [63,63,63]
    if (aqi<50):
        return [0,255,0]
    if (aqi<100):
        return [255,255,0]
    if (aqi<150):
        return [255,150,0]
    if (aqi<200):
        return [255,0,0]
    if (aqi<300):
        return [143,63,151]
    return [126,0,35]

def desc_from_aqi(aqi):
    if (aqi<0):
        return "Unknown"
    if (aqi<50):
        return "Good"
    if (aqi<100):
        return "Moderate"
    if (aqi<150):
        return "Unhealthy-ish"
    if (aqi<200):
        return "Unhealthy"
    if (aqi<300):
        return "Very Unhealthy"
    return "HAZARDOUS"

if __name__=='__main__':
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(wifi_ssid,wifi_pass)

    LCD = LCD_1inch14.LCD_1inch14()
    backlight_level=0.25
    LCD.set_backlight(backlight_level)
    LCD.fill(LCD.white)

    fg = LCD.blue
    bg = LCD.white

    wri_aqi = CWriter(LCD, arial_50)
    wri_status = CWriter(LCD, freesans20)
    wri_aqi.setcolor(fg,bg)
    wri_status.setcolor(fg,bg)

    while(not wlan.isconnected()):
        CWriter.set_textpos(LCD, 60, 30)  # verbose = False to suppress console output
        LCD.fill(bg)
        wri_status.printstring('Connecting to WiFi')
        LCD.show()

    aqi = -1
    last_aqi = 0
    aqi_diff = 0
    data_ok = False

    while(1):
        aqi_string="Fetching AQI..."
        CWriter.set_textpos(LCD, row=100, col=int((LCD.width-wri_status.stringlen(aqi_string))/2))
        wri_status.printstring(aqi_string)
        LCD.show()

        try:
            data = get_sensor_data()
            data_ok = True
            last_aqi = aqi
            aqi = get_aqi_from_data(data)
            if (last_aqi == -1):
                last_aqi = aqi
        except x:
            print("Error: %s"%str(x))
            data_ok = False

        if data_ok:
            fg = fg_color_from_aqi(aqi)
            bg = bg_color_from_aqi(aqi)

            fg = LCD.rgb(fg[0],fg[1],fg[2])
            bg = LCD.rgb(bg[0],bg[1],bg[2])

            wri_aqi.setcolor(fg,bg)
            wri_status.setcolor(fg,bg)
            CWriter.set_textpos(LCD, row=30)
            LCD.fill(bg)
            aqi_string = '%d'%aqi;
            CWriter.set_textpos(LCD, col=int((LCD.width-wri_aqi.stringlen(aqi_string))/2))
            wri_aqi.printstring(aqi_string)
            wri_aqi.printstring('\n')

            desc_string=desc_from_aqi(aqi)
            CWriter.set_textpos(LCD, col=int((LCD.width-wri_status.stringlen(desc_string))/2))
            wri_status.printstring(desc_string)

            aqi_diff = (aqi_diff*3+aqi-last_aqi)/4
            print("aqi diff:%f"%aqi_diff)
            wri_status.printstring('\n')

            if (aqi_diff > 2):
                wri_status.printstring('+')
            elif (aqi_diff < -2):
                wri_status.printstring('-')
        else:
            LCD.fill(bg)
            CWriter.set_textpos(LCD, 20, 20)  # verbose = False to suppress console output
            wri_status.printstring('Error getting AQI\n')
            CWriter.set_textpos(LCD, 45, 20)  # verbose = False to suppress console output
            if(not wlan.isconnected()):
                wri_status.printstring('WiFi is disconnected\n')

        LCD.show()

        for x in range(100):
            sleep(0.1)
            if LCD.keyA.value() == 0:
                backlight_level += 0.05;
            if LCD.keyB.value() == 0:
                backlight_level -= 0.05;
            if backlight_level > 1.0:
                backlight_level = 1.0
            if backlight_level < 0.0:
                backlight_level = 0.0

            LCD.set_backlight(backlight_level)
