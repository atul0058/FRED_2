#Script to measure temp using contactless temp sensor SHT31-D 


import smbus
import time

#Get I2C bus
bus=smbus.SMBus(1)

#SHT31 address, 0x45(68)
bus.write_i2c_block_data(0x45, 0x2c, [0x06])

time.sleep(0.5)

#SHT31 adress, 0x44(68)
#Read data back from 0x00(00), 6 bytes
#Temp MSB, temp LSB, Temp CRC, Humidity MSB, Humidity LSB , Humidity CRC
data = bus.read_i2c_block_data(0x45, 0x00, 6)


#Convert the data
temp=data[0] * 256 + data[1]
cTemp = -45 + (175*temp/65535.0)
fTemp= -49 + (315 * temp / 65535.0)
humidity = 100*(data[3]*256 + data[4])/65535.0

print "Temperature in Celcius is : %.2f C" %cTemp
