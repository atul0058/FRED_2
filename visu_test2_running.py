try:#python3
   from tkinter import *

except:#python2
    from Tkinter import * 

import Adafruit_DHT as dht
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
import numpy as np  
import matplotlib.pyplot as plt
import math
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
#==============================Threading==============================================================
import threading 

class App(threading.Thread):

    def __init__(self,tk_root):
        self.root = tk_root
        threading.Thread.__init__(self)
        self.start()

    def run(self):
        print "Starting...."

        
my_window = Tk()

 


#================================================================
label  = [[0 for i in range(12)] for i in range(12)]
for i in range(12):
    for j in range(12):
        label[i][j] = Label( my_window, width = '10', height = '3', bg = 'white')

#==================================DATABASE INFO and cooling curve===============================

label[0][4]=Label(my_window,width = '20', height = '3',text="Initial Temp (deg C)",bd=10,bg = 'white',anchor='w')
label[1][4]=Label(my_window,width = '20', height = '3',text="Target Temp (deg C)",bd=10,bg = 'white',anchor='w')
label[2][4]=Label(my_window,width = '20', height = '3',text="Entry Time",bd=10,bg = 'white',anchor='w')
label[3][4]=Label(my_window,width = '20', height = '3',text="Target Time",bd=10,bg = 'white',anchor='w')
label[4][4]=Label(my_window,width = '20', height = '3',text="Time Remaining(sec)",bd=10,bg = 'white',anchor='w')
label[5][4]=Label(my_window,width = '20', height = '3',text="Current Temp (deg C)",bd=10,bg = 'white',anchor='w')

label[0][4].grid(row=0,column=4)
label[1][4].grid(row=1,column=4)
label[2][4].grid(row=2,column=4)
label[3][4].grid(row=3,column=4)
label[4][4].grid(row=4,column=4)
label[5][4].grid(row=5,column=4)

text_Input=StringVar()
label[0][5]=Label(my_window,width = '20', height = '3',text="Press wkp icon", bd=10,bg = 'white',anchor='w')
label[1][5]=Label(my_window,width = '20', height = '3',text="12", bd=10,bg = 'white',anchor='w')
label[2][5]=Label(my_window,width = '20', height = '3',text="Press wkp icon", bd=10,bg = 'white',anchor='w')
label[3][5]=Label(my_window,width = '20', height = '3',text="Press wkp icon", bd=10,bg = 'white',anchor='w')
label[4][5]=Label(my_window,width = '20', height = '3',text="Press wkp icon", bd=10,bg = 'white',anchor='w')
label[5][5]=Label(my_window,width = '20', height = '3',text="Press wkp icon", bd=10,bg = 'white',anchor='w')

label[0][5].grid(row=0,column=5)
label[1][5].grid(row=1,column=5)
label[2][5].grid(row=2,column=5)
label[3][5].grid(row=3,column=5)
label[4][5].grid(row=4,column=5)
label[5][5].grid(row=5,column=5)

# label_21=Label(my_window,width = '10', height = '3',text="Cooling curve", bd=10)
# label_21.grid(row=6,column=6,rowspan=6,columnspan=2)

#======================================Cooling elements info and trigger AM2302 and SHT31-D==========================
def Ambient_temp():
    h, t = dht.read_retry(dht.DHT22, 21)
    label[11][5]=Label(my_window,width = '10', height = '3',text=float(t), bd=10,bg = 'white',anchor='w')
    label[11][5].grid(row=11,column=5)

def wkp_temp():   
    #Get I2C bus
    bus=smbus.SMBus(1)
    #SHT31 address, 0x45(68)
    bus.write_i2c_block_data(0x44, 0x2c, [0x06])
    time.sleep(0.5)
    #SHT31 adress, 0x44(68)
    #Read data back from 0x00(00), 6 bytes
    #Temp MSB, temp LSB, Temp CRC, Humidity MSB, Humidity LSB , Humidity CRC
    data = bus.read_i2c_block_data(0x44, 0x00, 6)
    #Convert the data
    temp=data[0] * 256 + data[1]
    cTemp = -45 + (175*temp/65535.0)
    fTemp= -49 + (315 * temp / 65535.0)
    humidity = 100*(data[3]*256 + data[4])/65535.0
    label[10][5]=Label(my_window,width = '10', height = '3',text=float(cTemp),bd=10,bg = 'white',anchor='w')
    label[10][5].grid(row=10,column=5)


label[6][4]=Label(my_window,width = '20', height = '3',text="Current (A)",bd=10,bg = 'white',anchor='w')
label[7][4]=Label(my_window,width = '20', height = '3',text="Voltage (V)",bd=10,bg = 'white',anchor='w')
label[8][4]=Label(my_window,width = '20', height = '3',text="Hot side temp (deg C)", bd=10,bg = 'white',anchor='w')
label[9][4]=Label(my_window,width = '20', height = '3',text="Cold side temp (deg C)", bd=10,bg = 'white',anchor='w')
label[10][4]=Button(my_window,width = '20', height = '3',text="Final Temp (deg C)", bd=10,bg = 'white',anchor='w',command=wkp_temp)
label[11][4]=Button(my_window,width = '20', height = '3',text="Ambient Temp (deg C)", bd=10,bg = 'white',anchor='w',command=Ambient_temp)



label[6][4].grid(row=6,column=4)
label[7][4].grid(row=7,column=4)
label[8][4].grid(row=8,column=4)
label[9][4].grid(row=9,column=4)
label[10][4].grid(row=10,column=4)
label[11][4].grid(row=11,column=4)

# label[6][5]=Label(my_window,width = '10', height = '3',text="upd", bd=10,bg = 'white',anchor='w')
# label[7][5]=Label(my_window,width = '10', height = '3',text="upd", bd=10,bg = 'white',anchor='w')
# label[8][5]=Label(my_window,width = '10', height = '3',text="upd", bd=10,bg = 'white',anchor='w')
# label[9][5]=Label(my_window,width = '10', height = '3',text="upd", bd=10,bg = 'white',anchor='w')
# label[10][5]=Label(my_window,width = '10', height = '3',text="upd", bd=10,bg = 'white',anchor='w')
# label[11][5]=Label(my_window,width = '10', height = '3',text="upd", bd=10,bg = 'white',anchor='w')

label[6][5].grid(row=6,column=5)
label[7][5].grid(row=7,column=5)
label[8][5].grid(row=8,column=5)
label[9][5].grid(row=9,column=5)
label[10][5].grid(row=10,column=5)
label[11][5].grid(row=11,column=5)


#======================================================================================================= 


db = MySQLdb.connect(host="localhost", user="raspi", passwd="raspberry", db="test1")



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


"""
def graph():  
    Ti=25
    Ti=int(Ti)
    z=int(cooling_time(Ti))
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
    x = [i for i in range(z)]  
    y = [2*math.exp(b*(z-i))+10 for i in x] 
    
    plt.title('Cooling curve')
    plt.xlabel('Time')
    plt.ylabel('Temp')
    # fig,ax=plt.subplots(nrows=1,ncols=1)
    # ax.plot(x,y)
    # fig.savefig('/home/pi/testImg.png')
    # plt.close(fig)
    # img=PhotoImage(file="testImg.png")
    # label[0][6]=Label(my_window,image=img)
    # label[0][6].grid(row=6,column=6,rowspan=6,columnspan=2)


    fig=Figure(figsize=(5,4),dpi=100)
    ax=fig.add_subplot(111).plot(x,y)
    fig.text(0.5, 0.04, 'Time', ha='center', va='center')
    fig.text(0.06, 0.5, 'Temp', ha='center', va='center', rotation='vertical')
    
    #ax.set_title('Cooling curve')
    canvas=FigureCanvasTkAgg(fig,master=my_window)
    canvas.draw()
    canvas.get_tk_widget().grid(row=2,column=6,rowspan=6)
"""

#will remove all the workpieces from the rack
def clearstore():#add modbus
    # c = db.cursor()
    # db.begin()
    # query=("delete from LastAdded")
    # c.execute(query)
    # c.close()
    for i in range(12):
        for j in range(4):
            button[i][j].grid_forget()
            #print ("The store has been cleared")
"""
cooling_curve_button= Button( my_window,text='Press for cooling curve',bg='white',command=graph)
cooling_curve_button.grid(row=0,column=6)
"""
clear_store_button=Button( my_window,text='clear store', bg='white',command=clearstore)
clear_store_button.grid(row=0,column=6) 
"""
ambient_temp_button=Button(my_window,text='Press for ambient temp curve',bg='white',command=measure_ambient)
ambient_temp_button.grid(row=0,column=7)
"""


#==========================================================================================================


def button_click(i,j):
    shelf=6-int(i)/2
    row=int(j)+1
    location=shelf*100+row*10+1
    c = db.cursor()
    db.begin()
    query_0=("select Date_and_Time,Temperature,Target_Time from test1 where Location=%s",[location])
    c.execute(*query_0)
    result_0=c.fetchall()
    c.close()
    entry_time=result_0[0][0]
    Ti=result_0[0][1]
    target_time=result_0[0][2]
    time_left= 23
    current_temp=52
    label[0][5]=Label(my_window,width = '20', height = '3',text=Ti, bd=10,bg = 'white',anchor='w')
    label[2][5]=Label(my_window,width = '20', height = '3',text=entry_time, bd=10,bg = 'white',anchor='w')
    label[3][5]=Label(my_window,width = '20', height = '3',text=target_time, bd=10,bg = 'white',anchor='w')
    label[4][5]=Label(my_window,width = '20', height = '3',text=time_left, bd=10,bg = 'white',anchor='w')
    label[5][5]=Label(my_window,width = '20', height = '3',text=current_temp, bd=10,bg = 'white',anchor='w')
    label[0][5].grid(row=0,column=5)
    label[2][5].grid(row=2,column=5)
    label[3][5].grid(row=3,column=5)
    label[4][5].grid(row=4,column=5)
    label[5][5].grid(row=5,column=5)

    z=int(cooling_time(Ti))
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
    x = [i for i in range(z)]  
    y = [2*math.exp(b*(z-i))+10 for i in x] 
    
    plt.title('Cooling curve')
    plt.xlabel('Time (sec)')
    plt.ylabel('Temp (deg C)')
    fig=Figure(figsize=(5,4),dpi=100)
    ax=fig.add_subplot(111).plot(x,y)
    fig.text(0.5, 0.04, 'Time (sec)', ha='center', va='center')
    fig.text(0.06, 0.5, 'Temp (deg C)', ha='center', va='center', rotation='vertical')
    canvas=FigureCanvasTkAgg(fig,master=my_window)
    canvas.draw()
    canvas.get_tk_widget().grid(row=2,column=6,rowspan=6)

button=[[0 for i in range(4)] for i in range(12)]
for i in range(12):
    for j in range(4):
        button[i][j]=Button(my_window,bg='white')




def putwkp(i,j):
    nw_rows=[1,3,5,7,9,11]
    other_rows=[0,2,4,6,8,10]
    if i in nw_rows:
        button[i][j].grid(row=i,column=j,sticky="nw")
    elif i in other_rows:
        button[i][j].grid(row=i,column=j)

def put_img(i,j,img):
    button[i][j]= Button( my_window,image=img,bg='white',command=lambda: button_click(i,j))

    # button[i][j].bind("<Button-1>",button_click)
    putwkp(i,j)
    button[i][j].photo = img
        

#think anout it. put_wkp should replace this
nw_rows=[1,3,5,7,9,11]
for i in nw_rows:
    for j in range(4):
        label[i][j].grid(row=i,column=j,sticky="nw")

other_rows=[0,2,4,6,8,10]
for i in other_rows:
    for j in range(4):
        label[i][j].grid(row=i,column=j)

#workpiece images
# red_wkp=PhotoImage(file="Dose_schwarz.png")
# silver_wkp=PhotoImage(file="Dose_silber.png")
# black_wkp=PhotoImage(file="Dose_schwarz,png")
# trans_wkp=PhotoImage(file="Dose_transparent.png")





#putting racks


img1=PhotoImage(file="rack.png")
label_1=Label(my_window,image=img1)
label_2=Label(my_window,image=img1)
label_3=Label(my_window,image=img1)
label_4=Label(my_window,image=img1)
label_5=Label(my_window,image=img1)
label_6=Label(my_window,image=img1)

label_1.grid(row=0,column=0,columnspan=4, rowspan=2)
label_2.grid(row=2,column=0,columnspan=4, rowspan=2)
label_3.grid(row=4,column=0,columnspan=4, rowspan=2)
label_4.grid(row=6,column=0,columnspan=4, rowspan=2)
label_5.grid(row=8,column=0,columnspan=4, rowspan=2)
label_6.grid(row=10,column=0,columnspan=4, rowspan=2)

#input is location and color, will put the wkp in the locaiton
def show_image():
    #try except statement here, on clicking the clear store button, the programme shows an error.
    query1=("select Location,Colour from LastAdded order by Id desc limit 1")
    query2=("select Location from LastRemoved order by Id desc limit 1")
    query3=("select Current, Voltage, Hot_Side_Temp, Cold_Side_Temp from peltier_power order by Id desc limit 1")

    queries=[query3,query2,query1]
    c = db.cursor()
    

    for x in queries:
        if x==query2:
            db.begin()
            c.execute(query2)
            result2=c.fetchall()
            
            location_remove = int(result2[0][0])
            shelf=location_remove//100
            row=(location_remove%100)//10
            i=12-2*shelf
            j=row-1
            button[i][j].grid_forget()
            db.commit()
            print result2

        elif x==query3:
            db.begin()
            c.execute(query3)
            result3=c.fetchall()
            # print result3
            current= result3[0][0]
            voltage = result3[0][1]
            Th = result3[0][2]
            Tc = result3[0][3]
            label[6][5]=Label(my_window,width = '20', height = '3',text=current,bd=10,bg = 'white',anchor='w')
            label[7][5]=Label(my_window,width = '20', height = '3',text=voltage,bd=10,bg = 'white',anchor='w')
            label[8][5]=Label(my_window,width = '20', height = '3',text=Th,bd=10,bg = 'white',anchor='w')
            label[9][5]=Label(my_window,width = '20', height = '3',text=Tc,bd=10,bg = 'white',anchor='w')
            label[6][5].grid(row=6,column=5)
            label[7][5].grid(row=7,column=5)
            label[8][5].grid(row=8,column=5)
            label[9][5].grid(row=9,column=5)
            print result3
            db.commit()


        elif x==query1:
            db.begin()
            c.execute(x)
            result1=c.fetchall()
            
            location=int(result1[0][0])
            color=str(result1[0][1])
            shelf=location//100
            row=(location%100)//10
            i=12-2*shelf
            j=row-1
            if color=="Red":
                img=PhotoImage(file="Dose_rot.png")
                button[i][j].grid_forget()
                put_img(i,j,img)
                #my_window.after(1000,show_image)
            elif color=="Silver":
                img=PhotoImage(file="Dose_silber.png")
                button[i][j].grid_forget()
                put_img(i,j,img)
                #my_window.after(1000,show_image)
            elif color=="Black":
                img=PhotoImage(file="Dose_schwarz,png")
                button[i][j].grid_forget()
                put_img(i,j,img)
                #my_window.after(1000,show_image)
            elif color=="Transparent":
                img=PhotoImage(file="Dose_transparent.png")
                button[i][j].grid_forget()
                put_img(i,j,img)
            print result1
            db.commit()

        
            

    my_window.after(1000,show_image)





"""
    c = db.cursor()
    db.begin()
    query1=("select Location,Colour from LastAdded order by Id desc limit 1")
    c.executemany(query1,LastAdded)
    result1=c.fetchall()
    #c.close()
    print result1
    location=int(result1[0][0])
    color=str(result1[0][1])
    shelf=location//100
    row=(location%100)//10
    i=12-2*shelf
    j=row-1
    if color=="Red":
        img=PhotoImage(file="Dose_rot.png")
        button[i][j].grid_forget()
        put_img(i,j,img)
        #my_window.after(1000,show_image)
    elif color=="Silver":
        img=PhotoImage(file="Dose_silber.png")
        button[i][j].grid_forget()
        put_img(i,j,img)
        #my_window.after(1000,show_image)
    elif color=="Black":
        img=PhotoImage(file="Dose_schwarz,png")
        button[i][j].grid_forget()
        put_img(i,j,img)
        #my_window.after(1000,show_image)
    elif color=="Transparent":
        img=PhotoImage(file="Dose_transparent.png")
        button[i][j].grid_forget()
        put_img(i,j,img)
    
        
    #Code for hiding the unstored wkpc
    # c = db.cursor()
    # db.begin()
    query2=("select Location from LastRemoved order by Id desc limit 1")
    c.executemany(query2,LastRemoved)
    result2=c.fetchall()
    #c.close()
    print result2
    location_remove = int(result2[0][0])
    shelf=location//100
    row=(location%100)//10
    i=12-2*shelf
    j=row-1
    button[i][j].grid_forget()
    ##Code for Current updation Goes here
    #c = db.cursor()
    #db.begin()
    query3=("select Current, Voltage, Hot_Side_Temp, Cold_Side_Temp from peltier_power order by Id desc limit 1")
    c.executemany(query3,peltier_power)
    result3=c.fetchall()
    c.close()
    # print result3
    current= result3[0][0]
    voltage = result3[0][1]
    Th = result3[0][2]
    Tc = result3[0][3]
    label[6][5]=Label(my_window,width = '10', height = '3',text=current,bd=10,bg = 'white',anchor='w')
    label[7][5]=Label(my_window,width = '10', height = '3',text=voltage,bd=10,bg = 'white',anchor='w')
    label[8][5]=Label(my_window,width = '10', height = '3',text=Th,bd=10,bg = 'white',anchor='w')
    label[9][5]=Label(my_window,width = '10', height = '3',text=Tc,bd=10,bg = 'white',anchor='w')
    label[6][5].grid(row=6,column=5)
    label[7][5].grid(row=7,column=5)
    label[8][5].grid(row=8,column=5)
    label[9][5].grid(row=9,column=5)
    print result3

    my_window.after(1000,show_image)


    # location=input("Enter location: ")#replace with SQL query
    # location=int(location)
    # shelf=location//100
    # row=(location%100)//10
    # i=12-2*shelf
    # j=row-1
    # label[i][j].grid_forget()



#==============================================entrybox for students====================================================

# label_19=Label(left4,width = '10', height = '3',text="Input HTC", bd=10,bg = 'white',anchor='w')
# label_19.grid(row=0,column=0)
# entrybox_1=Entry(left4,width = '10', height = '3',textvariable=text_Input,bd=10,insertwidth=2,bg="powder blue",justify='right')
# entrybox_1.grid(row=0,column=1)

# label_20=Label(left4,width = '10', height = '3',text="Cooling Time", bd=10,bg = 'white',anchor='w')
# label_20.grid(row=1,column=0)

# label_20_1=Label(left4,width = '10', height = '3',text="Enter value", bd=10,bg = 'white',anchor='w')
# label_20_1.grid(row=1,column=1)

# button_3=Button(left4,width = '10', height = '3',text="Submit", bd=10,bg = 'white',anchor='w')
# button_3.grid(row=2,column=0,columnspan=2)




"""
APP = App(my_window)
my_window.after(1000,show_image)
my_window.geometry("1400x800+0+0")
my_window.title("FRED")
my_window['bg']='white'
my_window.mainloop()
