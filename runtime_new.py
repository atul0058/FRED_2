# Import all the needed modules
import os
import time
import smbus
import datetime
import glob
import MySQLdb
from time import strftime
import math
import smbus
from pymodbus.client.sync import ModbusTcpClient as ModbusClient
from datetime import timedelta
import sys


#All the Funtions are here 
def cooling_time(Ti):
    Re = 5000
    Pr = 0.71
    Nu = 0.3 + ((0.62*(Re**0.5)*(Pr**(1/3)))/(1+(0.4*Pr**(2/3)))**0.25)+(1+(Re/282000)**5/8)**(4/5)
    k = 0.17       #W.m^-1.k^-1
    d = 0.04       #m
    h = Nu*k/d     #W.m^2.k^-1
    Tamb = 10      #k
    
    a_conv = 5.38*10**(-3) #m^2
    v =  2.87*10**(-5)     #m^3
    d = 1070               #kg.m^-3
    c = 1432.512           #J.k^-1
    b=h*a_conv/(d*v*c)
    
    time=(1/b)*math.log((Ti-10)/2) #in seconds
    
    return time

def Target_Time(Ti):
    d1= datetime.datetime.now()
    delta_t=cooling_time(Ti)
    new_time=d1 + datetime.timedelta(0,delta_t)+datetime.timedelta(0,2400)
    #FRED takes 2400 seconds to reach the desired temperature
    return new_time

def read_register(reg_no):
    reg = client.read_input_registers(reg_no,1)
    val = reg.getRegister(0)
    return val

def rcv_location():
    shelf = read_register(0) + 1 
    row = read_register(1) + 1 
    row_place = read_register(2) + 1 
    location = (shelf*100) + (row*10)+ row_place
    return location
def sensor_read():
    bus=smbus.SMBus(1)
    bus.write_i2c_block_data(0x44, 0x2c, [0x06])
    time.sleep(0.5)
    #SHT31 adress, 0x44(68)
    #Read data back from 0x00(00), 6 bytes
    #Temp MSB, temp LSB, Temp CRC, Humidity MSB, Humidity LSB , Humidity CRC
    data = bus.read_i2c_block_data(0x44, 0x00, 6)
    #Convert the data
    temp=data[0] * 256 + data[1]
    cTemp = -45 + (175*temp/65535.0)
    return cTemp


# Connect with DB
db = MySQLdb.connect(host="localhost", user="raspi", passwd="raspberry", db="test1")
cursor = db.cursor()

def statusupdate():
    query='update test1 set Status=1 where Current_TIMESTAMP>=Target_Time'
    cursor.execute(query)
    db.commit()

def add_row(temp): 
    date_and_time=(time.strftime("%Y-%m-%d ") + time.strftime("%H:%M:%S"))    
    query = ("""insert into test1(Date_and_Time, Temperature, Target_Time, Status, Location, Colour) values (%s,%s,%s,%s,%s,%s)""", (date_and_time, temp,Target_Time(temp),0,rcv_location(),colour()))
    cursor.execute(*query)
    db.commit()

def colour():
    colour_data = read_register(5)
    if colour_data == 0: 
        colour = 'Red'
    if colour_data == 1: 
        colour = 'Black'
    if colour_data == 2: 
        colour = 'Silver'
    return colour
    
def visuAdd():
    query = ("""insert into LastAdded(Location, Colour) values (%s,%s)""", (rcv_location(),colour()))
    cursor.execute(*query)
    db.commit()

def visuRemove(Location):
    query = ("""insert into LastRemoved(Location) values (%s)""", [location])
    cursor.execute(*query)
    db.commit()

def removefromdb():
    remove='DELETE FROM test1 WHERE status =1 limit 1'   
    cursor.execute(remove)
    db.commit()

def update():
    query='select Location from test1 where Status=1'
    cursor.execute(query)
    res = cursor.fetchall()
    return res[0][0]

def mode_selection():
    query='select count(Location) from test1 where Status=1'
    cursor.execute(query)
    result = cursor.fetchall()
    if (result[0][0] != 0):
        mode = 1
    else:
        mode = 0
    return mode

def merge_rows():
    query1 ='SELECT Date_and_Time ,Location, Target_Time, Status, Colour  FROM test1 ORDER BY ID desc  LIMIT 1' 
    cursor.execute(query1)
    result1 = cursor.fetchall()
    merge_date = result1[0][0]
    merge_loc = result1[0][1]
    merge_target = result1[0][2]
    merge_status = result1[0][3]
    merge_colour = result1[0][4]

    query2 = 'select avg(Temperature) from test1 where Location ='  + str(merge_loc)
    cursor.execute(query2)
    result = cursor.fetchall()
    avg = result[0][0]
    
    query3 = 'delete from test1 where Location = ' + str(merge_loc)
    cursor.execute(query3)
    db.commit()

    query4 = query = ("""insert into test1(Date_and_Time, Temperature, Target_Time, Status, Location, Colour) values (%s,%s,%s,%s,%s,%s)""", (merge_date, avg ,merge_target,merge_status,merge_loc,merge_colour))
    cursor.execute(*query4)
    db.commit()


#Modbus Connection initialise 
client = ModbusClient(host = '192.168.178.10',port  = 502)          ##Modbus connection establish 
client.connect() 
client.write_registers(0, [0]*10)                                                  ##Open Connection

#mode :Store = 0, Unstore = 1
try:
    while True:
        mode = mode_selection()
        while True:
            #merge_rows()
            statusupdate()
            #mode = mode_selection()##result of the mode query
            print mode
            
            sys.stdout.flush()
            if mode == 0:          
                while True:
                    xStartRec = read_register(3)
                    if xStartRec == 0:
                        break
                temp = sensor_read()
                add_row(temp)
                visuAdd()
                merge_rows()

                break
                
            if mode ==1:
                time.sleep(45)
                send_location = update()
                s_row_Place = send_location%100%10
                s_row = send_location//10%10
                s_shelf = send_location//100
                s_shelf = s_shelf-1
                s_row = s_row - 1
                s_row_Place = s_row_Place - 1         
                client.write_register(0,s_shelf)
                client.write_register(1,s_row)
                client.write_register(2,s_row_Place)
                print 'Unstoring Item on '+ str(send_location)
                client.write_register(3,1)
                time.sleep(3)
                client.write_register(3,0)
                visuRemove(send_location)
                while True:
                    xStart = read_register(4)
                    if xStart == 0:
                        break
                removefromdb()
                break
except Exception, e1:
    print "Error communicating...: " + str(e1)
