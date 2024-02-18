import lcd_1602
import time

lcd_1602.init(0x27, 1)
try:
    while True: 
        lcd_1602.write(0,0, "wasgud fellas")
        lcd_1602.write(0,1, "dhungan")
except KeyboardInterrupt:
    lcd_1602.clear()
    print("Hrun dzat shiet baeck")