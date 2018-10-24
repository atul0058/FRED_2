# Import all the needed modules

import os
import time
import datetime
import glob
import MySQLdb
from time import strftime
import math
import smbus
import time
from pymodbus.client.sync import ModbusTcpClient as ModbusClient

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

def target_time(Ti):
    d1= datetime.datetime.now()
    delta_t=cooling_time(Ti)
    new_time=d1 + datetime.timedelta(0,delta_t)+2400
    #FRED takes 2400 seconds to reach the desired temp
    return new_time

def read_register(reg_no):
    reg = client.read_input_registers(reg_no,1)
    val = reg.getRegister(0)
    return val

def rcv_location():
    shelf = read_register(0)
    row = read_register(1)
    row_place = read_register(2)
    location = (shelf*100) + (row*10)+ row_place
    return location

def sensor_read():
    bus=smbus.SMBus(1)
        bus.write_i2c_block_data(0x44, 0x2c, [0x06])
        time.sleep(0.5)
        data = bus.read_i2c_block_data(0x44, 0x00, 6)
        temp=data[0] * 256 + data[1]
        cTemp = -45 + (175*temp/65535.0)
    return cTemp

# Connect with DB
db = MySQLdb.connect(host="localhost", user="raspi", passwd="raspberry", db="test1")
cursor = db.cursor()

#Create the Table. These settings are temp 
table = 'create table(Id mediumint auto_increment not null, Date_and_Time datetime not null, Temp float(5,2) not null, Target_Time datetime not null, Status boolean not null, Location int not null, Primary key(Id))'
cursor.execute(table) ##verify 

def add_row(temp, location): verify this query 
    query = 'insert into test1(Date_and_Time, Temp, Target_Time, Status, Location) values (%s,%d,%s,%d,%d)'% (current_date_and_time, temp,Target_Time(temp),0,location())
    return cursor.execute(query)

#Modbus Connection initialise 
client = ModbusClient(host = '192.168.178.10',port  = 502)          ##Modbus connection establish 
client.connect() 
client.write_registers(0, [9]*10)                                                  ##Open COnnection

#mode :Store = 0, Unstore = 1

while True:
    mode = read_register(x)
    if mode == 0:          
        while True:
            xRecognise = read_register(y)
            if xRecognise == 1:
                break
        temp = sensor_read() ##this too
        add_row(temp)  ##make sure this runs
        
    if mode ==1:
        update() ##this too
        a = list1[0]
        outLocation = a[0]
        s_row_place = send_location%100%10
        s_row = send_location//10%10
        s_shelf = send_location//100         
        client.write_register(0,s_shelf)
        client.write_register(1,s_row)
        client.write_register(2,s_row_Place)
        while True:
            xDone = read_register(z)
            if xDone == 1:
                break
        remove(##only the first element with status == 1 and has been removed already from cpps)##this is the last query
