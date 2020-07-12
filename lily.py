from machine import I2C,Pin,reset,SPI
import st7789my as st7789
import axp202c as axp202
import pcf8563
import time
# import focaltouch


def maprange(point,fromrange,torange):
    pnew=int( (float(point)-fromrange[0])*float(torange[1]-torange[0])/float(fromrange[1]-fromrange[0])+torange[0] )
    pnew=min(torange[1],pnew)
    pnew=max(torange[0],pnew)
    return(pnew)
    

    


class LILY(object):
    def __init__(self):
        self.axp=axp=axp202.PMU()
        self.axp.enablePower(axp202.AXP202_LDO2)
        self.axp.enablePower(axp202.AXP202_DCDC3)
        # useful shorthands
        self.reset=reset
        self.shutdown=self.axp.shutdown
        self.bl=Pin(12,Pin.OUT)
        self.bl.on()
        self.ir=Pin(13,Pin.OUT)
        self.ir.off()
        self.buzz=Pin(4,Pin.OUT)
        self.disp=st7789.ST7789font(None,240,240,reset=None,cs=Pin(5,Pin.OUT),dc=Pin(27,Pin.OUT))
        self.i2c0 = axp.bus  # I2C(0,scl.Pin(22), sda=Pin(21))
        self.i2c1 = I2C(1,scl=Pin(32), sda=Pin(23))
        self.disp.init()
        self.disp.writestring("booting..",0,0)
        self.testimg=self.disp.testimg
        self.hwrtc=pcf8563.PCF8563(self.i2c0)
        datetime=self.hwrtc.datetime()
        #                      (20, 7, 9, 4, 1, 44, 13)
        yy,mon,dd,dow,hh,mm,ss=datetime
        self.disp.writestring("%04d-%02d-%02d %02d:%02d:%02d" % (2000+yy,mon,dd,hh,mm,ss) ,0,10)
        # self.ft=focaltouch.FocalTouch(self.i2c1)
        self.orientation=2 # 0 is same as touchscreen. button is on the upper right. 1 rotate ccw, 2 upside down. 3  cw
        self.xrange=[20,220] # position of touch on screen
        self.yrange=[20,220]

    def maptouch(self,touches): # map and rotate touchinput
        mapped=[self.touchmap(touch) for touch in touches]
        return mapped
        
    def touchmap(self,touch):
        x=touch['x']
        y=touch['y']
        id=touch['id']
        x=maprange(x,self.xrange,[0,self.disp.width-1])
        y=maprange(y,self.yrange,[0,self.disp.height-1])
        if self.orientation == 2:
            x=self.disp.width-1-x
            y=self.disp.height-1-y
        elif self.orientation == 1 or self.orientation == 3:
            assert("not implemented")
        return{'x':x, 'id':id , 'y':y }
            
    def paint(self):
        ft=self.ft
        while True:
            if ft.touched:
                touches=self.maptouch(ft.touches)
                print(touches)
                touch=touches[0]
                self.disp.pixel(touch['x'],touch['y'],st7789.RED)
            else:
                time.sleep_ms(50)

# i2c0        
# scan 25 (0x19) bosch BMA423 accellerometer
# scan 53 (0x35) AXP202 power managment?
# scan 81 (0x51) PCF8563 RTC 

#i2c1
# scan 56 (0x38) focaltouch FT6236U


