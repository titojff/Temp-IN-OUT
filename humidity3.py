#!/usr/bin/python3

#O calor húmido é muito mais quente que o calor seco,
#Modificado para 2 sensores SHT45 em 2 buses i2C por software
#sensor DS18B20 para a parede com one wire
import sys          
import time

import warnings

from datetime import datetime
from openpyxl import load_workbook
from openpyxl import Workbook

from adafruit_extended_bus import ExtendedI2C as I2C
import adafruit_sht4x

import DS18B20

import math


warnings.filterwarnings(
    "ignore",
    message="I2C frequency is not settable in python, ignoring!"
)



def calculate_humidex(temp_celsius, humidity_percent): #Só para temp acima de 27ºC
    # Step 1: Calculate vapor pressure (e)
    e = 6.11 * math.pow(10, (7.5 * temp_celsius) / (237.7 + temp_celsius)) * (humidity_percent / 100.0)
    
    # Step 2: Calculate Humidex
    humidex = temp_celsius + 0.5555 * (e - 10)
    
    return round(humidex, 1)

def apparent_temperature_indoor(temp_c, rh_percent): #Apparent Temperature (Steadman)
    """
    Indoor apparent temperature (Steadman-based)

    Parameters:
        temp_c (float): Air temperature in °C
        rh_percent (float): Relative humidity in %

    Returns:
        float: Apparent temperature in °C
    """

    # Saturation vapor pressure (hPa)
    es = 6.105 * math.exp((17.27 * temp_c) / (237.7 + temp_c))

    # Actual vapor pressure (hPa)
    e = (rh_percent / 100.0) * es

    # Apparent temperature (no wind indoors)
    at = temp_c + 0.33 * e - 4.0

    return round(at, 1)




wb = load_workbook('1.xlsx')
# grab the active worksheet
ws = wb.active

#flag=0
#buzzer=13
#GPIO.setup(buzzer,GPIO.OUT)
#pwm12 = GPIO.PWM(buzzer, 10000)
#pwm12.start(50)
#sleep(2)
#pwm12.stop()

# access the I2C port by bus number - SHT45 BUSES I2C 3 e 4
#IN initialization
i2c_in=I2C(3)
sht_in = adafruit_sht4x.SHT4x(i2c_in)
sht_in.mode = adafruit_sht4x.Mode.NOHEAT_HIGHPRECISION

#Out Initialization
i2c_out=I2C(4)
sht_out = adafruit_sht4x.SHT4x(i2c_out)
sht_out.mode = adafruit_sht4x.Mode.NOHEAT_HIGHPRECISION

a=[0,1,2]#para efeitos de dizer close now
#--------------------------------------
def move_right(lst):#para efeitos de dizer close now
    lstF=[0,0,0]
    lstF[2]=lst[1]
    lstF[1]=lst[0]

    return lstF
#print("Hora     Data       In   Wall Out  H-in H-out")


#----------------------------------------


print("   Hora   In  Out  H-in H-out        |  FLi  FLo")    

while True:

    temperaturei, humidityi = sht_in.measurements
    temperaturei=float("%0.1f" % temperaturei)
    humidityi=float("%0.1f" % humidityi)
    
    feels_likeI = apparent_temperature_indoor(temperaturei, humidityi)


    temperatureo, humidityo = sht_out.measurements
    temperatureo=float("%0.1f" % temperatureo)
    humidityo=float("%0.1f" % humidityo)
      
    feels_likeO = apparent_temperature_indoor(temperatureo, humidityo)
      
      
      
#para efeitos de dizer close now        
   #print (a)
    b=move_right(a)
    b[0]=temperaturei
   #print (b)
    c=0
    if b[0]>b[1]:
        c=c+1        
    if b[0]>b[2]:
        c=c+1    
    cw=0    
    if c==2:        
        cw=1
       # print ("CLOSE NOW")    
    a=b

  
    ss=(time.strftime('%d-%m-%y'))
    ss2=(time.strftime('%H:%M'))
    ss = datetime.strptime(ss, '%d-%m-%y').date()
    ss2 = datetime.strptime(ss2, '%H:%M').time()

    temperature_celsius, temperature_fahrenheit = DS18B20.read_temp()
    wall=float(f'{temperature_celsius:.1f} ')
    op="  CLOSE"
    open=temperaturei-temperatureo
    if open > 0:
        op="  OPEN "
        
    Delta=round((feels_likeI-feels_likeO), 1) 
    FLop="FL-CLOSE" 
    if Delta > 0:
        FLop="FL-OPEN"
    #feels_likeI Buffer to see if is increasing, then close warning
    
#    print("   Hora   In  Out  H-in H-out       |  FLi FLo")    
    print (ss2,temperaturei ,temperatureo,humidityi,humidityo, op,"|",feels_likeI, feels_likeO, FLop )
#    print ("FeelsLike-In",feels_likeI, "FeelsLike-Out",feels_likeO, "Delta(- > close)",Delta)    
      
#    print("Hora     Data       In   Wall Out  H-in H-out")    
#    print (ss2,ss,temperaturei, wall ,temperatureo,humidityi,humidityo, op)
#    print ("FeelsLike-In",feels_likeI, "FeelsLike-Out",feels_likeO, "Delta(- > close)",Delta)
    
    
    
    
    ws.append([ss, ss2 , temperaturei, wall , temperatureo , humidityi , humidityo])
    wb.save("1.xlsx")



    time.sleep(300)
