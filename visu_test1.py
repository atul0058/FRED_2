from tkinter import *
my_window= Tk()

label  = [[0 for i in range(4)] for i in range(12)]
for i in range(12):
    for j in range(4):
    	label[i][j] = Label(my_window, width = '10', height = '3', bg = 'blue')


img1=PhotoImage(file="rack.png")
rack=[]
for i in range(4):
    rack.append('Label(my_window,image=img1)')

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
            print("The store has been cleared")

#putting racks
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
def show_image(location,color):
    if color=="red":
        img=PhotoImage(file="Dose_schwarz.png")
        #add location 
    if color=="silver":
        img=PhotoImage(file="Dose_silber.png")
    if color=="black_wkp":
        img=PhotoImage(file="Dose_schwarz,png")
    if color=="trans_wkp":
        img=PhotoImage(file="Dose_transparent.png")

def remove_wkp(location):
    #make locaiton as i and j
    label[i][j].grid_forget()



















 
