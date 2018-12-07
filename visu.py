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
import matplotlib
import matplotlib.pyplot as plt
import math
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

##################################################3
client = ModbusClient(host = '192.168.178.10', port  = 502)
##################################################


#==============================Threading==============================================================
import threading 


Tamb = 10

Re = 5000
Pr = 0.71
Nu = 0.3 + ((0.62*(Re**0.5)*(Pr**(1/3)))/(1+(0.4*Pr**(2/3)))**0.25)+(1+(Re/282000)**5/8)**(4/5)
k = 0.17       #W.m^-1.k^-1
d = 0.04       #m
h = Nu*k/d     #W.m^2.k^-1
Tamb = 10
#Target Temp : 17      #k
a_conv = 5.38*10**(-3) #m^2
v =  2.87*10**(-5)     #m^3
d = 1070               #kg.m^-3
c = 1432.512           #J.k^-1
b=h*a_conv/(d*v*c) #seconds


class App(threading.Thread):

    def __init__(self,tk_root):
        self.root = tk_root
        threading.Thread.__init__(self)
        self.start()

    def run(self):
        print "Starting...."
        
my_window = Tk()

#================================================================
label  = [[0 for i in range(13)] for i in range(13)]
for i in range(12):
    for j in range(12):
        label[i][j] = Label( my_window, width = '10', height = '3', bg = 'white')

#==================================DATABASE INFO and cooling curve===============================

label[1][5]=Entry(my_window)


Target_Temp=17


label[0][4]=Label(my_window,width = '20', height = '3',text="Initial Temp (deg C)",bd=10,bg = 'white',anchor='w')
label[1][4]=Label(my_window,width = '20', height = '3',text="Target Temp (deg C)",bd=10,bg = 'white',anchor='w')
label[2][4]=Label(my_window,width = '20', height = '3',text="Entry Time",bd=10,bg = 'white',anchor='w')
label[3][4]=Label(my_window,width = '20', height = '3',text="Target Time",bd=10,bg = 'white',anchor='w')
label[4][4]=Label(my_window,width = '20', height = '3',text="Update Cooling Time(in sec)",bd=10,bg = 'white',anchor='w')


label[0][4].grid(row=0,column=4)
label[1][4].grid(row=1,column=4)
label[2][4].grid(row=2,column=4)
label[3][4].grid(row=3,column=4)
label[4][4].grid(row=4,column=4)



label[0][5]=Label(my_window,width = '20', height = '3',text="Press wkp icon", bd=10,bg = 'white',anchor='w')
label[1][5]=Label(my_window,width = '20', height = '3',text="17", bd=10,bg = 'white',anchor='w')
label[2][5]=Label(my_window,width = '20', height = '3',text="Press wkp icon", bd=10,bg = 'white',anchor='w')
label[3][5]=Label(my_window,width = '20', height = '3',text="Press wkp icon", bd=10,bg = 'white',anchor='w')
label[4][5]=Entry(my_window)


label[0][5].grid(row=0,column=5)
label[1][5].grid(row=1,column=5)
label[2][5].grid(row=2,column=5)
label[3][5].grid(row=3,column=5)
label[4][5].grid(row=4,column=5)



#======================================Cooling elements info and trigger AM2302 and SHT31-D==========================
def Ambient_temp():
    h, t = dht.read_retry(dht.DHT22, 21)
    t=int(t)
    label[11][5]=Label(my_window,width = '10', height = '3',text=round(t,2), bd=10,bg = 'white',anchor='w')
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
    cTemp=int(cTemp)
    label[10][5]=Label(my_window,width = '10', height = '3',text=round(cTemp,2),bd=10,bg = 'white',anchor='w')
    label[10][5].grid(row=10,column=5)


label[5][4]=Label(my_window,width = '20', height = '3',text="Update Current (A)",bd=10,bg = 'white',anchor='w')
label[6][4]=Label(my_window,width = '20', height = '3',text="Optimal Current",bd=10,bg = 'white',anchor='w')
label[7][4]=Label(my_window,width = '20', height = '3',text="Voltage (V)",bd=10,bg = 'white',anchor='w')
label[8][4]=Label(my_window,width = '20', height = '3',text="Hot side temp (deg C)", bd=10,bg = 'white',anchor='w')
label[9][4]=Label(my_window,width = '20', height = '3',text="Cold side temp (deg C)", bd=10,bg = 'white',anchor='w')
label[10][4]=Button(my_window,width = '20', height = '3',text="Final Temp (deg C)", bd=10,bg = 'white',anchor='w',command=wkp_temp)
label[11][4]=Button(my_window,width = '20', height = '3',text="Ambient Temp (deg C)", bd=10,bg = 'white',anchor='w',command=Ambient_temp)

label[5][4].grid(row=5,column=4)
label[6][4].grid(row=6,column=4)
label[7][4].grid(row=7,column=4)
label[8][4].grid(row=8,column=4)
label[9][4].grid(row=9,column=4)
label[10][4].grid(row=10,column=4)
label[11][4].grid(row=11,column=4)
label[5][5]=Entry(my_window)


label[5][5].grid(row=5,column=5)
label[6][5].grid(row=6,column=5)
label[7][5].grid(row=7,column=5)
label[8][5].grid(row=8,column=5)
label[9][5].grid(row=9,column=5)
label[10][5].grid(row=10,column=5)
label[11][5].grid(row=11,column=5)


#======================================================================================================= 

db = MySQLdb.connect(host="localhost", user="raspi", passwd="raspberry", db="test1")

def cooling_time(Ti): 
    time=(1/b)*math.log((Ti-Tamb)/(Target_Temp-Tamb))+2400 #in seconds
    return time 

#will remove all the workpieces from the rack
def clearstore():#add modbus
    # c = db.cursor()
    # db.begin()
    # query=("delete from LastAdded")
    # c.execute(query)
    # c.close()
    client.connect()
    client.write_register(4,1)
    time.sleep(2)
    client.write_register(4,0)
    client.close()

    for i in range(12):
        for j in range(4):
            button[i][j].grid_forget()
            #print ("The store has been cleared")

clear_store_button=Button( my_window,text='clear store', bg='white',command=clearstore)
clear_store_button.grid(row=0,column=6) 

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
    
    label[0][5]=Label(my_window,width = '20', height = '3',text=Ti, bd=10,bg = 'white',anchor='w')
    label[2][5]=Label(my_window,width = '20', height = '3',text=entry_time, bd=10,bg = 'white',anchor='w')
    label[3][5]=Label(my_window,width = '20', height = '3',text=target_time, bd=10,bg = 'white',anchor='w')
    
    label[0][5].grid(row=0,column=5)
    label[2][5].grid(row=2,column=5)
    label[3][5].grid(row=3,column=5)
    
    label[5][5].grid(row=5,column=5)

    # label[3][5]=str(label[3][5])
    # label[2][5]=str(label[2][5])
    # label[3][5]=datetime.datetime.strptime(label[3][5], '%Y-%m-%d %H:%M:%S.%f')
    # label[2][5]=datetime.datetime.strptime(label[2][5], '%Y-%m-%d %H:%M:%S.%f')
    
    # z=int((label[3][5]-label[2][5]).total_seconds())
    z=cooling_time(Ti)
    #cooling time should come from the (entry time- target time)
    ls=[0,0.2*z,0.4*z,0.6*z,0.8*z,z]
    x = [p for p in ls]  
    y = [(Ti-Tamb)*math.exp(-b*p)+Tamb for p in x] 
    
    plt.title('Cooling curve')
    plt.xlabel('Time (sec)')
    plt.ylabel('Temp (deg C)')
    fig=Figure(figsize=(5,4),dpi=100)
    ax=fig.add_subplot(111).plot(x,y)
    fig.text(0.5, 0.03, 'Time (seconds)', ha='center', va='center')
    fig.text(0.04, 0.5, 'Temp (deg C)', ha='center', va='center', rotation='vertical')
    canvas=FigureCanvasTkAgg(fig,master=my_window)
    canvas.draw()
    canvas.get_tk_widget().grid(row=6,column=6,rowspan=6)

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



def UserInput_coolingTime():
    new_time=label[2][5]['text']
    new_time=datetime.datetime.strptime(new_time, '%Y-%m-%d %H:%M:%S')
    new_time1=new_time+datetime.timedelta(0,int(label[4][5].get()))
    label[3][5]=Label(my_window,width = '20', height = '3',text=new_time1, bd=10,bg = 'white',anchor='w')
    label[3][5].grid(row=3,column=5)
    c = db.cursor()

    query_4=("update test1 set Target_Time=%s where Date_and_Time=%s",(new_time1,new_time))
    c.execute(*query_4)
    c.close()
    db.commit()

    temp=label[0][5]["text"]

    z=int(label[4][5].get())
    ls=[0,0.2*z,0.4*z,0.6*z,0.8*z,z]
    x = [i for i in ls] 
    y = [(temp-Tamb)*math.exp(-b*(i))+Tamb for i in x] 
    plt.title('Cooling curve')
    plt.xlabel('Time (sec)')
    plt.ylabel('Temp (deg C)')
    fig=Figure(figsize=(5,4),dpi=100)
    ax=fig.add_subplot(111).plot(x,y)
    fig.text(0.5, 0.03, 'Time (sec)', ha='center', va='center')
    fig.text(0.03, 0.5, 'Temp (deg C)', ha='center', va='center', rotation='vertical')
    canvas=FigureCanvasTkAgg(fig,master=my_window)
    canvas.draw()
    canvas.get_tk_widget().grid(row=6,column=6,rowspan=6)
    
def UserInput_current():
    newcurrent=label[5][5].cget("text")
    newcurrent=float(newcurrent)
    #put in that python script
    

    

user_input_button=Button( my_window,text='Submit New Cooling Time', bg='white',command=UserInput_coolingTime)
user_input_button.grid(row=1,column=6)

user_input_button=Button( my_window,text='Submit New Current', bg='white',command=UserInput_current)
user_input_button.grid(row=2,column=6)





def refresh_button():
    query3=("select Current, Voltage, Hot_Side_Temp, Cold_Side_Temp from peltier_power order by Id desc limit 1")
    query4=("select Hot_Side_Temp from peltier_power")
    query5=("select Cold_Side_Temp from peltier_power")
    queries=[query3,query4,query5]
    c = db.cursor()

    for x in queries:
        if x==query3:
            try:
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
            except Exception:
                pass

        elif x==query4:
            try:
                db.begin()
                c.execute(query4)
                result4=c.fetchall()
                ls=[]
                for i in result4:
                    ls.append(round(float(i[0]),1))
                y=len(ls)
                x_axis=[i for i in range(y)]
                y_axis=[i for i in ls]
                fig=Figure(figsize=(5,4),dpi=100)
                ax=fig.add_subplot(111).plot(x_axis,y_axis)
                fig.text(0.5, 0.02, ' ', ha='center', va='center')
                fig.text(0.02, 0.5, 'Avg Hot Side Temp (deg C)', ha='center', va='center', rotation='vertical')
                canvas=FigureCanvasTkAgg(fig,master=my_window)
                canvas.draw()
                canvas.get_tk_widget().grid(row=0,column=15,rowspan=6,columnspan=8)
                db.commit()

            except Exception:
                pass

        elif x==query5:
            try:  
                db.begin()
                c.execute(query5)
                result5=c.fetchall()
                ls=[]
                for i in result5:
                    ls.append(round(float(i[0]),1))
                y=len(ls)
                x_axis=[i for i in range(y)]
                y_axis=[i for i in ls]
                fig=Figure(figsize=(5,4),dpi=100)
                ax=fig.add_subplot(111).plot(x_axis,y_axis)
                fig.text(0.5, 0.02, ' ', ha='center', va='center')
                fig.text(0.02, 0.5, 'Avg Cold Side Temp (deg C)', ha='center', va='center', rotation='vertical')
                canvas=FigureCanvasTkAgg(fig,master=my_window)
                canvas.draw()
                canvas.get_tk_widget().grid(row=6,column=15,rowspan=6,columnspan=8)
                db.commit()
            except Exception:
                pass


refresh_button=Button( my_window,text='Refresh', bg='white',command=refresh_button)
refresh_button.grid(row=3,column=6)

#input is location and color, will put the wkp in the locaiton
def show_image():
    #try except statement here, on clicking the clear store button, the programme shows an error.
    query1=("select Location,Colour from LastAdded order by Id desc limit 1")
    query2=("select Location from LastRemoved order by Id desc limit 1")
    queries=[query2,query1]
    c = db.cursor()
    for x in queries:
        if x==query2:
            try:
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
                #print result2
            except Exception:
                pass
        elif x==query1:
            try:
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
                #print result1
                db.commit()
            except Exception:
                pass
    my_window.after(1000,show_image)

APP = App(my_window)
my_window.after(1000,show_image)
my_window.geometry("1800x800+0+0")
my_window.title("FRED")
my_window['bg']='white'
my_window.mainloop()
