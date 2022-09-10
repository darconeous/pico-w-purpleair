# https://www.waveshare.com/wiki/Pico-LCD-1.14

from machine import Pin,SPI,PWM
import framebuf
import time

BL = 13
DC = 8
RST = 12
MOSI = 11
SCK = 10
CS = 9

class BoolPalette(framebuf.FrameBuffer):

    def __init__(self, mode):
        buf = bytearray(4)  # OK for <= 16 bit color
        super().__init__(buf, 2, 1, mode)

    def fg(self, color):  # Set foreground color
        self.pixel(1, 0, color)

    def bg(self, color):
        self.pixel(0, 0, color)

def rbit8(v):
    v = (v & 0x0f) << 4 | (v & 0xf0) >> 4
    v = (v & 0x33) << 2 | (v & 0xcc) >> 2
    return (v & 0x55) << 1 | (v & 0xaa) >> 1

class LCD_1inch14(framebuf.FrameBuffer):
    # Convert r, g, b in range 0-255 to an 16 bit colour value
    #  acceptable to hardware: GGGBBBBBRRRRRGGG
    @staticmethod
    def rgb(r, g, b):
        r = (r>>3)
        g = (g>>2)
        b = (b>>3)
        comb = r + (b<<5) + (g<<10)
        return ((comb&0x1fff)<<3)+(comb>>13)

    def __init__(self):
        self.width = 240
        self.height = 135
        self.palette = BoolPalette(framebuf.RGB565)

        self.cs = Pin(CS,Pin.OUT)
        self.rst = Pin(RST,Pin.OUT)

        self.cs(1)
        self.spi = SPI(1,20000_000,polarity=0, phase=0,sck=Pin(SCK),mosi=Pin(MOSI),miso=None)
        self.dc = Pin(DC,Pin.OUT)
        self.dc(1)
        self.buffer = bytearray(self.height * self.width * 2)

        super().__init__(self.buffer, self.width, self.height, framebuf.RGB565)
        self.init_display()

        self.red   =  self.rgb(255,0,0) #0x07E0
        self.green =  self.rgb(0,255,0)# 0x001f
        self.blue  =  self.rgb(0,0,255)# 0xf800
        self.white =  self.rgb(255,255,255)# 0xffff

        self.pwm = PWM(Pin(BL))
        #self.set_backlight(0.5)

        self.keyA = Pin(15,Pin.IN,Pin.PULL_UP)
        self.keyB = Pin(17,Pin.IN,Pin.PULL_UP)

        self.keyUp = Pin(2 ,Pin.IN,Pin.PULL_UP) #上
        self.keyCenter = Pin(3 ,Pin.IN,Pin.PULL_UP)#中
        self.keyLeft = Pin(16 ,Pin.IN,Pin.PULL_UP)#左
        self.keyDown = Pin(18 ,Pin.IN,Pin.PULL_UP)#下
        self.keyRight = Pin(20 ,Pin.IN,Pin.PULL_UP)#右


    def set_backlight(self, level):
        self.pwm.freq(1000)
        self.pwm.duty_u16(int(level*65535))

    def write_cmd(self, cmd):
        self.cs(1)
        self.dc(0)
        self.cs(0)
        self.spi.write(bytearray([cmd]))
        self.cs(1)

    def write_data(self, buf):
        self.cs(1)
        self.dc(1)
        self.cs(0)
        self.spi.write(bytearray([buf]))
        self.cs(1)

    def init_display(self):
        """Initialize dispaly"""
        self.rst(1)
        self.rst(0)
        self.rst(1)

        self.write_cmd(0x36)
        self.write_data(0x70)

        self.write_cmd(0x3A)
        self.write_data(0x05)

        self.write_cmd(0xB2)
        self.write_data(0x0C)
        self.write_data(0x0C)
        self.write_data(0x00)
        self.write_data(0x33)
        self.write_data(0x33)

        self.write_cmd(0xB7)
        self.write_data(0x35)

        self.write_cmd(0xBB)
        self.write_data(0x19)

        self.write_cmd(0xC0)
        self.write_data(0x2C)

        self.write_cmd(0xC2)
        self.write_data(0x01)

        self.write_cmd(0xC3)
        self.write_data(0x12)

        self.write_cmd(0xC4)
        self.write_data(0x20)

        self.write_cmd(0xC6)
        self.write_data(0x0F)

        self.write_cmd(0xD0)
        self.write_data(0xA4)
        self.write_data(0xA1)

        self.write_cmd(0xE0)
        self.write_data(0xD0)
        self.write_data(0x04)
        self.write_data(0x0D)
        self.write_data(0x11)
        self.write_data(0x13)
        self.write_data(0x2B)
        self.write_data(0x3F)
        self.write_data(0x54)
        self.write_data(0x4C)
        self.write_data(0x18)
        self.write_data(0x0D)
        self.write_data(0x0B)
        self.write_data(0x1F)
        self.write_data(0x23)

        self.write_cmd(0xE1)
        self.write_data(0xD0)
        self.write_data(0x04)
        self.write_data(0x0C)
        self.write_data(0x11)
        self.write_data(0x13)
        self.write_data(0x2C)
        self.write_data(0x3F)
        self.write_data(0x44)
        self.write_data(0x51)
        self.write_data(0x2F)
        self.write_data(0x1F)
        self.write_data(0x1F)
        self.write_data(0x20)
        self.write_data(0x23)

        self.write_cmd(0x21)

        self.write_cmd(0x11)

        self.write_cmd(0x29)

    def show(self):
        self.write_cmd(0x2A)
        self.write_data(0x00)
        self.write_data(0x28)
        self.write_data(0x01)
        self.write_data(0x17)

        self.write_cmd(0x2B)
        self.write_data(0x00)
        self.write_data(0x35)
        self.write_data(0x00)
        self.write_data(0xBB)

        self.write_cmd(0x2C)

        self.cs(1)
        self.dc(1)
        self.cs(0)
        self.spi.write(self.buffer)
        self.cs(1)

if __name__=='__main__':
    pwm = PWM(Pin(BL))
    pwm.freq(1000)
    pwm.duty_u16(32768)#max 65535

    LCD = LCD_1inch14()
    #color BRG
    LCD.fill(LCD.white)

    LCD.show()
    LCD.text("Raspberry Pi Pico",90,40,LCD.red)
    LCD.text("PicoGo",90,60,LCD.green)
    LCD.text("Pico-LCD-1.14",90,80,LCD.blue)



    LCD.hline(10,10,220,LCD.blue)
    LCD.hline(10,125,220,LCD.blue)
    LCD.vline(10,10,115,LCD.blue)
    LCD.vline(230,10,115,LCD.blue)


    LCD.show()
    keyA = Pin(15,Pin.IN,Pin.PULL_UP)
    keyB = Pin(17,Pin.IN,Pin.PULL_UP)

    key2 = Pin(2 ,Pin.IN,Pin.PULL_UP) #上
    key3 = Pin(3 ,Pin.IN,Pin.PULL_UP)#中
    key4 = Pin(16 ,Pin.IN,Pin.PULL_UP)#左
    key5 = Pin(18 ,Pin.IN,Pin.PULL_UP)#下
    key6 = Pin(20 ,Pin.IN,Pin.PULL_UP)#右

    while(1):
        if(keyA.value() == 0):
            LCD.fill_rect(208,12,20,20,LCD.red)
        else :
            LCD.fill_rect(208,12,20,20,LCD.white)
            LCD.rect(208,12,20,20,LCD.red)


        if(keyB.value() == 0):
            LCD.fill_rect(208,103,20,20,LCD.red)
        else :
            LCD.fill_rect(208,103,20,20,LCD.white)
            LCD.rect(208,103,20,20,LCD.red)




        if(key2.value() == 0):#上
            LCD.fill_rect(37,35,20,20,LCD.red)
        else :
            LCD.fill_rect(37,35,20,20,LCD.white)
            LCD.rect(37,35,20,20,LCD.red)


        if(key3.value() == 0):#中
            LCD.fill_rect(37,60,20,20,LCD.red)
        else :
            LCD.fill_rect(37,60,20,20,LCD.white)
            LCD.rect(37,60,20,20,LCD.red)



        if(key4.value() == 0):#左
            LCD.fill_rect(12,60,20,20,LCD.red)
        else :
            LCD.fill_rect(12,60,20,20,LCD.white)
            LCD.rect(12,60,20,20,LCD.red)


        if(key5.value() == 0):#下
            LCD.fill_rect(37,85,20,20,LCD.red)
        else :
            LCD.fill_rect(37,85,20,20,LCD.white)
            LCD.rect(37,85,20,20,LCD.red)


        if(key6.value() == 0):#右
            LCD.fill_rect(62,60,20,20,LCD.red)
        else :
            LCD.fill_rect(62,60,20,20,LCD.white)
            LCD.rect(62,60,20,20,LCD.red)


        LCD.show()
    time.sleep(1)
    LCD.fill(0xFFFF)
