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
    new_time=d1 + datetime.timedelta(0,delta_t)
    ##Add 40 minutes to the final reading
    return new_time

def status():                                                       ##All statuses intialised to zero
    return 0

def shelf():
    rr_shelf = client.read_input_registers(0,1)   
    shelf=rr_shelf.getRegister(0)

    return shelf

def row():
    rr_row = client.read_input_registers(0,1)   
    row = rr_row.getRegister(0)
    return row

def row_place():
    rr_rowplace = client.read_input_registers(0,1)   
    row_place =  rr_rowplace.getRegister(0)
    return row_place 

def rcv_location():
    location = (shelf()*100) + (row()*10)+ row_place()
    return location

def read_register(reg_no):
    reg = client.read_input_registers(reg_no,1)
    val = reg.getRegister(0)
    return val

# Connect with DB
db = MySQLdb.connect(host="localhost", user="raspi", passwd="raspberry", db="test1")
cursor = db.cursor()

#Create the Table. These settings are temp 
table = 'create table runtime Id mediumint primary key auto increment, Date_and_Time datetime, Temp float Target_Time datetime, Status BOOl, Shelf int, Row Int, Row_Place'
cursor.execute(table)

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
        sensor()
        add_row()
    if mode ==1:
        update()
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
        remove()
