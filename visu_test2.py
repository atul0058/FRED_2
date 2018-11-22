from tkinter import *

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




label  = [[0 for i in range(4)] for i in range(12)]
for i in range(12):
    for j in range(4):
    	label[i][j] = Label(my_window, width = '10', height = '3', bg = 'blue')



def putwkp(i,j):
    nw_rows=[1,3,5,7,9,11]
    other_rows=[0,2,4,6,8,10]
    if i in nw_rows:
        label[i][j].grid(row=i,column=j,sticky="nw")
    elif i==0 and j==0:
        label[0][0].grid(row=0,column=0,sticky="e")
    elif i in other_rows:
        label[i][j].grid(row=i,column=j)

def put_img(i,j,img):
    label[i][j]= Label(my_window,image=img)
    putwkp(i,j)
    label[i][j].photo = img
        

#think anout it. put_wkp should replace this
nw_rows=[1,3,5,7,9,11]
for i in nw_rows:
    for j in range(4):
    	label[i][j].grid(row=i,column=j,sticky="nw")

other_rows=[0,2,4,6,8,10]
for i in other_rows:
	for j in range(4):
		label[i][j].grid(row=i,column=j)


#exception
label[0][0].grid(row=0,column=0,sticky="e")

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
            print ("The store has been cleared")

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
    color=input("Enter color: ")#replace with SQL query
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

APP = App(my_window)
my_window.mainloop()




# while True:
#     show_image()
#     my_window.after(0,show_image)
#     my_window.mainloop()

# my_window.after(0,show_image)

# my_window.mainloop() 


















 
