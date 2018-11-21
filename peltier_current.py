import time, serial, math
import glob
import time
from time import sleep
import RPi.GPIO as GPIO
sleeptime = 1
GPIO.setmode(GPIO.BCM)
GPIO.setup(4, GPIO.IN, pull_up_down=GPIO.PUD_UP)

ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=0,
            bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE)

x  = 1
print 'Initialising System...'


def TemperatureRead(device_folder):
    base_dir = '/sys/bus/w1/devices/28-00000'
    device_file = base_dir + device_folder + '/w1_slave'
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = TemperaturMessung()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        return temp_c

# 0 means top

sensor_id1 = 'a294445'
sensor_id2 = 'a2a4342'
sensor_id3 = 'a2a8f7c'
sensor_id4 = 'a2a8c45'
sensor_id5 = 'a2ab77b'
sensor_id6 = 'a291dd5'

def update_current():
    Th[0] = TemperatureRead(sensor_id1)
    Th[1] = TemperatureRead(sensor_id2)
    Th[2] = TemperatureRead(sensor_id3)


    Tc[0] = TemperatureRead(sensor_id4)
    Tc[1] = TemperatureRead(sensor_id5)
    Tc[2] = TemperatureRead(sensor_id6)

    TH = (Th[0] + Th[1] + Th[2])/3
    TC = (Tc[0] + Tc[1] + Tc[2])/3
    # Th = 35.00#float(input('Hot side temp'))
    # Tc = 15.00#float(input('Cold side temp'))


    deltaT = TH - TC 
    k = 1.394117647             #thermal conductance (W/K)
    Qc = 40#float(input('Cooling power'))                        #cooling power(W)
    R = 0.79946028             #electrical resistance(Ohms)
    alpha =0.051298701         #Seebecks coeff(V/K)
    b = (-2* alpha*Tc)/R
    c = (-Qc +k*deltaT)*2/R
    I1 = float((-b+math.sqrt(b**2 -4*c ))/2)
    # I2 = (-b-math.sqrt(b**2 -4*c ))/2
     
    #Qc = -(alpha*I*Tc) + (0.5*(I**2)*R) + k*(Th-Tc)
    print (I1)
    if len(str(int(I1))) == 1:
        current_str = 'CURR0' + str(int(I1*10)) + '\r'
    if len(str(int(I1))) ==2:
        current_str = 'CURR' + str(int(I1*10)) + '\r'

        

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
