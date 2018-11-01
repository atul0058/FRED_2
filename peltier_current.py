import time, serial, math

# def sensor_read(number):
#     bus=smbus.SMBus(number)
#     bus.write_i2c_block_data(0x44, 0x2c, [0x06])
#     time.sleep(0.5)
#     #SHT31 adress, 0x44(68)
#     #Read data back from 0x00(00), 6 bytes
#     #Temp MSB, temp LSB, Temp CRC, Humidity MSB, Humidity LSB , Humidity CRC
#     data = bus.read_i2c_block_data(0x44, 0x00, 6)
#     #Convert the data
#     temp=data[0] * 256 + data[1]
#     cTemp = -45 + (175*temp/65535.0)
#     return cTemp

# Th = sensor_read(1)
# Tc = sensor_read(2)

ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=0,
            bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE)

x  = 1




Th = 35.00#float(input('Hot side temp'))
Tc = 15.00#float(input('Cold side temp'))


deltaT = Th - Tc 
k = 1.394117647             #thermal conductance (W/K)
Qc = 40#float(input('Cooling power'))                        #cooling power(W)
R = 0.79946028             #electrical resistance(Ohms)
alpha =0.051298701         #Seebecks coeff(V/K)
b = (-2* alpha*Tc)/R
c = (-Qc +k*deltaT)*2/R
I1 = (-b+math.sqrt(b**2 -4*c ))/2
# I2 = (-b-math.sqrt(b**2 -4*c ))/2
 
#Qc = -(alpha*I*Tc) + (0.5*(I**2)*R) + k*(Th-Tc)
print (I1)
current_str = 'CURR' + str(I1*100) + '\r'



if ser.isOpen():  #exit if USB port is not open
    try:
        ser.flushInput() #flush input buffer, discarding all its contents
        ser.flushOutput() #flush output buffer, aborting current output

        while x:        
          ser.write("GETS\r")       # Get setting information
          time.sleep(0.5)
          response=ser.readline()
          if response == '':continue

          voltage=response[:3]  # PSU return string in format "100200", that means 10.0V, 2.00A,
          current=response[3:6] # then use first 3 data for voltage and next 3 data for current.
          print(voltage[:2]+'.'+voltage[2:]+'V')
          print(current[:1]+'.'+current[1:]+'A')    
                  break
        time.sleep(3)


        #Set PSU output to 2A
        print("Set PSU CURRENT OUTPUT to ") + str(I1)
        while x:
          ser.write(current_str)  # change Current setting
          time.sleep(0.5)
          response=ser.readline()
          if response == '':continue            
          print(response)
          break
        time.sleep(3)

        ser.close()

    except Exception, e1:
        print "Error communicating...: " + str(e1)


else:
    print "Cannot open serial port "
