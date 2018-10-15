#This file contains the equation to find the cooling time of the workpiece.


import math

def cooling_time(Ti):
    Re = 5000      #Reynolds number
    Pr = 0.71      
    Nu = 0.3 + ((0.62*(Re**0.5)*(Pr**(1/3)))/(1+(0.4*Pr**(2/3)))**0.25)+(1+(Re/282000)**5/8)**(4/5)
    k = 0.17       #Thermal Conductivity (W.m^-1.k^-1)
    d = 0.04       #m
    h = Nu*k/d     #W.m^2.k^-1
    Tamb = 10      #Ambient temperature (k)
    
    a_conv = 5.38*10**(-3) #Area (m^2)
    v =  2.87*10**(-5)     #Volume (m^3)
    d = 1070               #density(kg.m^-3)
    c = 1432.512           #specific heat(J.k^-1)
    b=h*a_conv/(d*v*c)
    
    time=(-1/b)*math.log(2/(Ti-10)) #cooling time in seconds
    
    return time


x=cooling_time(20.5)

print(x)


