"""
This script is intended to make the database for the project FRED. It shows the initial temp of the workpiece, time of entry, 
time at which it will get cooled, it's status(whether it has reached it's desired temp or not), and it's location.
"""

import os
import time
import datetime
import glob
import MySQLdb
from time import strftime
import math
import smbus
import time

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
    time=(-1/b)*math.log(2/(Ti-10)) #in seconds
    
    return time

def target_time(Ti):
    d1= datetime.datetime.now()
    delta_t=cooling_time(Ti)
    new_time=d1 + datetime.timedelta(0,delta_t)
    
    return new_time

def status():
    return 0

db = MySQLdb.connect(host="localhost", user="raspi", passwd="raspberry", db="t1")
cur = db.cursor()

while True:
    try:
        while True:
            bus=smbus.SMBus(1)
            bus.write_i2c_block_data(0x44, 0x2c, [0x06])
            time.sleep(0.5)
            data = bus.read_i2c_block_data(0x44, 0x00, 6)
            temp=data[0] * 256 + data[1]
            cTemp = -45 + (175*temp/65535.0)
            d1= (time.strftime("%Y-%m-%d ") + time.strftime("%H:%M:%S"))
            
            sql = ("""INSERT INTO t2(Date_and_Time,Temperature,Target_Time,Status,Location) VALUES (%s,%s,%s,%s,%s)""",(d1,cTemp,target_time(cTemp),status(),location()))
            try:
                cur.execute(*sql)
                db.commit()
            except:
                db.rollback()
            break
        
        print "Written to database.To stop press CTRL+C" 
        print ("Executing...")

    except KeyboardInterrupt:
        print ("Keyboard Interruption. Exiting.")
        cur.close()
        db.close()
        exit()

