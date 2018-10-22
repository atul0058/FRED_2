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

client = ModbusClient(host = '192.168.178.10',port  = 502)          ##Modbus connection establish 
client.connect()                                                    ##Open COnnection

## find a way to make a database here itself from python 

x=input("How long to wait between each reading? (in seconds)= ")

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

db = MySQLdb.connect(host="localhost", user="raspi", passwd="raspberry", db="test1")
cur = db.cursor()

##infinite loop for status updation
while True:
    ## Update Status where Current_TIMESTAMP >= Target_Time;
    ##Query = "Select Location from <Table> WHERE Status = 1"
    list = execute query
    # ##UNSTORING LOOP 
    # for i in list:
    # send_location = i[0]
    # s_row_place = send_location%100%10
    # s_row = send_location//10%10
    # s_shelf = send_location//100
    # client.write_registers(0, [9]*10)
    # client.write_register(0,s_shelf)
    # client.write_register(1,s_row)
    # client.write_register(2,s_row_Place) 
    # sleep for the time taken to unstore a workpiece
    # check for unstore 
    # if unstore_var ==1 


    time.sleep(5)




while True:
    try:
        while True:
            '''
            bus=smbus.SMBus(1)
            bus.write_i2c_block_data(0x44, 0x2c, [0x06])
            time.sleep(0.5)
            data = bus.read_i2c_block_data(0x44, 0x00, 6)
            temp=data[0] * 256 + data[1]
            cTemp = -45 + (175*temp/65535.0)
            '''
            d1= (time.strftime("%Y-%m-%d ") + time.strftime("%H:%M:%S"))
            ## Add a logic for trigger for recieving location
            z=input("What is the initial temperature= ")
            sql = ("""INSERT INTO test1(Date_and_Time,Temp,Target_Time,Status,Location) VALUES (%s,%s,%s,%s,%s)""",(d1,z,target_time(z),status(),rcv_location()))
            
            try:
                cur.execute(*sql)
                db.commit() 
            except:
                db.rollback()
            break
        
        print "Written to database.To stop press CTRL+C"
        time.sleep(x)
        print ("Executing...")

    except KeyboardInterrupt:
        print ("Keyboard Interruption. Exiting.")
        cur.close()
        db.close()
        exit()

