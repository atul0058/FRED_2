try:
   from tkinter import *

except:
    from Tkinter import * 


import time
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
        while True:
            show_image()
my_window = Tk()
 


#================================================================
label  = [[0 for i in range(12)] for i in range(12)]
for i in range(12):
    for j in range(12):
        label[i][j] = Label( my_window, width = '10', height = '3', bg = 'white')

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
    button[i][j]= Button( my_window,image=img,bg='white')
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

#will remove all the workpieces from the rack
def clearstore():#add modbus
    for i in range(12):
        for j in range(4):
            label[i][j].grid_forget()
            #print ("The store has been cleared")



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
    location=input("Enter location: ")#replace with SQL query
    color="red"#replace with SQL query
    location=int(location)
    shelf=location//100
    row=(location%100)//10
    i=12-2*shelf
    j=row-1
    if color=="red":
        img=PhotoImage(file="Dose_rot.png")
        put_img(i,j,img)
        #my_window.after(1000,show_image)
    if color=="silver":
        img=PhotoImage(file="Dose_silber.png")
        put_img(i,j,img)
        #my_window.after(1000,show_image)
    if color=="black":
        img=PhotoImage(file="Dose_schwarz,png")
        put_img(i,j,img)
        #my_window.after(1000,show_image)
    if color=="transparent":
        img=PhotoImage(file="Dose_transparent.png")
        put_img(i,j,img)
        #my_window.after(1000,show_image)

def remove_wkp():
    location=input("Enter location: ")#replace with SQL query
    location=int(location)
    shelf=location//100
    row=(location%100)//10
    i=12-2*shelf
    j=row-1
    label[i][j].grid_forget()

#==================================DATABASE INFO and cooling curve===============================

label[0][4]=Label(my_window,width = '10', height = '3',text="Initial Temp",fg="Steel Blue",bd=10,anchor='w')
label[1][4]=Label(my_window,width = '10', height = '3',text="Target Temp",fg="Steel Blue",bd=10,anchor='w')
label[2][4]=Label(my_window,width = '10', height = '3',text="Entry Time",fg="Steel Blue",bd=10,anchor='w')
label[3][4]=Label(my_window,width = '10', height = '3',text="Target Time",fg="Steel Blue",bd=10,anchor='w')
label[4][4]=Label(my_window,width = '10', height = '3',text="Time Remaining",fg="Steel Blue",bd=10,anchor='w')
label[5][4]=Label(my_window,width = '10', height = '3',text="Current Temp",fg="Steel Blue",bd=10,anchor='w')

label[0][4].grid(row=0,column=4)
label[1][4].grid(row=1,column=4)
label[2][4].grid(row=2,column=4)
label[3][4].grid(row=3,column=4)
label[4][4].grid(row=4,column=4)
label[5][4].grid(row=5,column=4)

text_Input=StringVar()
label[0][5]=Label(my_window,width = '10', height = '3',text="Press wkp icon",fg="Steel Blue",bd=10,anchor='w')
label[1][5]=Label(my_window,width = '10', height = '3',text="Press wkp icon",fg="Steel Blue",bd=10,anchor='w')
label[2][5]=Label(my_window,width = '10', height = '3',text="Press wkp icon",fg="Steel Blue",bd=10,anchor='w')
label[3][5]=Label(my_window,width = '10', height = '3',text="Press wkp icon",fg="Steel Blue",bd=10,anchor='w')
label[4][5]=Label(my_window,width = '10', height = '3',text="Press wkp icon",fg="Steel Blue",bd=10,anchor='w')
label[5][5]=Label(my_window,width = '10', height = '3',text="Press wkp icon",fg="Steel Blue",bd=10,anchor='w')

label[0][5].grid(row=0,column=5)
label[1][5].grid(row=1,column=5)
label[2][5].grid(row=2,column=5)
label[3][5].grid(row=3,column=5)
label[4][5].grid(row=4,column=5)
label[5][5].grid(row=5,column=5)

# label_21=Label(my_window,width = '10', height = '3',text="Cooling curve",fg="Steel Blue",bd=10)
# label_21.grid(row=6,column=6,rowspan=6,columnspan=2)

#======================================Cooling elements info and trigger AM2302 and SHT31-D==========================

label[6][4]=Label(my_window,width = '10', height = '3',text="Current",fg="Steel Blue",bd=10,anchor='w')
label[7][4]=Label(my_window,width = '10', height = '3',text="Voltage",fg="Steel Blue",bd=10,anchor='w')
label[8][4]=Label(my_window,width = '10', height = '3',text="Hot side temp",fg="Steel Blue",bd=10,anchor='w')
label[9][4]=Label(my_window,width = '10', height = '3',text="Cold side temp",fg="Steel Blue",bd=10,anchor='w')
label[10][4]=Button(my_window,width = '10', height = '3',text="Final Temp",fg="Steel Blue",bd=10,anchor='w')
label[11][4]=Button(my_window,width = '10', height = '3',text="Ambient Temp",fg="Steel Blue",bd=10,anchor='w')
#
label[6][4].grid(row=6,column=4)
label[7][4].grid(row=7,column=4)
label[8][4].grid(row=8,column=4)
label[9][4].grid(row=9,column=4)
label[10][4].grid(row=10,column=4)
label[11][4].grid(row=11,column=4)

label[6][5]=Label(my_window,width = '10', height = '3',text="upd",fg="Steel Blue",bd=10,anchor='w')
label[7][5]=Label(my_window,width = '10', height = '3',text="upd",fg="Steel Blue",bd=10,anchor='w')
label[8][5]=Label(my_window,width = '10', height = '3',text="upd",fg="Steel Blue",bd=10,anchor='w')
label[9][5]=Label(my_window,width = '10', height = '3',text="upd",fg="Steel Blue",bd=10,anchor='w')
label[10][5]=Label(my_window,width = '10', height = '3',text="upd",fg="Steel Blue",bd=10,anchor='w')
label[11][5]=Label(my_window,width = '10', height = '3',text="upd",fg="Steel Blue",bd=10,anchor='w')

label[6][5].grid(row=6,column=5)
label[7][5].grid(row=7,column=5)
label[8][5].grid(row=8,column=5)
label[9][5].grid(row=9,column=5)
label[10][5].grid(row=10,column=5)
label[11][5].grid(row=11,column=5)

#==============================================entrybox for students====================================================

# label_19=Label(left4,width = '10', height = '3',text="Input HTC",fg="Steel Blue",bd=10,anchor='w')
# label_19.grid(row=0,column=0)
# entrybox_1=Entry(left4,width = '10', height = '3',textvariable=text_Input,bd=10,insertwidth=2,bg="powder blue",justify='right')
# entrybox_1.grid(row=0,column=1)

# label_20=Label(left4,width = '10', height = '3',text="Cooling Time",fg="Steel Blue",bd=10,anchor='w')
# label_20.grid(row=1,column=0)

# label_20_1=Label(left4,width = '10', height = '3',text="Enter value",fg="Steel Blue",bd=10,anchor='w')
# label_20_1.grid(row=1,column=1)

# button_3=Button(left4,width = '10', height = '3',text="Submit",fg="Steel Blue",bd=10,anchor='w')
# button_3.grid(row=2,column=0,columnspan=2)




#======================================================================================================= 






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
    fig.add_subplot(111).plot(x,y)
    canvas=FigureCanvasTkAgg(fig,master=my_window)
    canvas.draw()
    canvas.get_tk_widget().grid(row=2,column=6,rowspan=6)

cooling_curve_button= Button( my_window,text='Press for cooling curve',bg='white',command=graph)
cooling_curve_button.grid(row=0,column=6)

clear_store_button=Button( my_window,text='clear store', bg='white')
clear_store_button.grid(row=1,column=6) 





#==========================================================================================================


APP = App(my_window)
my_window.geometry("1600x800+0+0")
my_window.title("FRED")
my_window['bg']='white'
my_window.mainloop()
