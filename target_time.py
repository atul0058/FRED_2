#We know the time at which the workpiece enters,and target time is the time at which the workpiece will reach the desired temp 

import datetime
import time
import math

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


print(target_time(50))

