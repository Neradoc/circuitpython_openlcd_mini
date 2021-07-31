import time
import board

DISPLAY_ADDRESS1 = 0x72
i2c = board.I2C()

# from sparkfun_serlcd import Sparkfun_SerLCD_I2C
# lcd = Sparkfun_SerLCD_I2C(i2c,DISPLAY_ADDRESS1)

import sparkfun_openlcd_mini
lcd = sparkfun_openlcd_mini.OpenLCD(i2c,DISPLAY_ADDRESS1)

def wheel(WheelPos):
	WheelPos = 255 - (WheelPos%256)
	if WheelPos < 85:
		return (255 - WheelPos * 3, 0, WheelPos * 3)
	if WheelPos < 170:
		WheelPos -= 85
		return (0, WheelPos * 3, 255 - WheelPos * 3)
	WheelPos -= 170
	return (WheelPos * 3, 255 - WheelPos * 3, 0)

lcd.clear()
lcd.write("Hello World !")

for x in range(0,256,8):
	lcd.backlight = wheel(x)
	time.sleep(0.04)

lcd.backlight = 0xFFFF00

#lcd.contrast = 128
#time.sleep(1)
#lcd.contrast = 0
#time.sleep(1)

for x in range(0,13):
	lcd.move(x,2)
	lcd.write("Toto")
	time.sleep(.5)
