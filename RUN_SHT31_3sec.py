import smbus
import time

#Get I2C bus
bus=smbus.SMBus(1)

while True:
    bus.write_i2c_block_data(0x44, 0x2C, [0x06])
    time.sleep(0.5)
    shtdata = bus.read_i2c_block_data(0x44, 0x00, 6)
    temp=shtdata[0]*256 + data[1]
    cTemp = -45 + (175*temp/65535.0)
    print "Temperature in Celcius is : %.2f C" %cTemp
    time.sleep(3)
    
    
    
    
    