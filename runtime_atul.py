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
    ##The system takes 40 minutes to reach the desiredd temperature
    return new_time

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

def add_row:
	date_and_time= (time.strftime("%Y-%m-%d ") + time.strftime("%H:%M:%S"))
	query = 'insert into test1(Date_and_Time, Temp, Target_Time, Status, Shelf, Row , Row_Place) values (%s,%s,%s,%s,%s,%s,%s)',(date_and_time, sensor_read(),Target_Time(),Status(),Shelf(),Row(),Row_Place())
	return cursor.execute(query)


def status():					##All statuses intialised to zero
	status='UPDATE Status=1 where Current_TIMESTAMP >= Target_Time'
	return cursor.execute(status)

	#how to run two while loops at the same time
	
	"""
	send_location='select location from test1 where status=1'
	cursor.execute(send_location)
	x=[]
	for i in cursor:
		x=x.append(i[0])
	#x is the list of all the locations which has to be sent to the PLC
	"""
def removefromdb():
	remove='DELETE TOP (1) FROM test1 WHERE status =1'    #I only want to remove the first element which ahs been unstored not all.
	return cursor.execute(remove)

	
#Create the Table. These settings are temp 
table = 'create table runtime Id mediumint primary key auto increment, Date_and_Time datetime, Temp float Target_Time datetime, Status BOOl, Shelf int, Row Int, Row_Place'
cursor.execute(table)

#Modbus Connection initialise 
	client = ModbusClient(host = '192.168.178.10',port  = 502)          ##Modbus connection establish 
	client.connect()                                                    ##Open COnnection

#Store = 0, Unstore = 1

temp_mode = client.read_input_registers(x,1)
mode = temp_mode.getRegister(0)

if mode ==0:
	while True:
		rec_reg = client.read_input_registers(y,1)
		xRec = rec_reg.getRegister(0)
		if xRec == 1:
			sensor_read()
			database.add_row()
		if mode ==1:Break()

if mode ==1:
	while True:
		list1 = cursor.execute(Update_status ==1)
		for a in list1:
			OutputLocation = a[0]
			s_row_place = send_location%100%10
    		s_row = send_location//10%10
    		s_shelf = send_location//100
        	client.write_registers(0, [9]*10)
    		client.write_register(0,s_shelf)
    		client.write_register(1,s_row)
    		client.write_register(2,s_row_Place)
    		if Unstore.done: continue()
			#Here we remove that element!
			
    	#break on mode change 

    Break on mode change 

#break on mode change 
