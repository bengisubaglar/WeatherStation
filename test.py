
from flask import Flask, render_template, request, Response, jsonify, make_response
import numpy
import matplotlib.pyplot as plt
import Adafruit_DHT
import datetime
app = Flask(__name__, template_folder='templates')
import Adafruit_BMP.BMP085 as BMP085



@app.route("/")
def home():
    temp = []
    hum=[]
    now = datetime.datetime.now()
    timeString = now.strftime("%d-%m-%Y %H:%M")
    for i in range(0,7) :
        
        t,humidity=read_sensor()
        
        temp.append(t)
        hum.append(humidity)
        
        fig, ax = plt.subplots()
        ax.plot(temp)
        ax.set_title("Temperature")
        plt.xlabel("Unit Time")
        plt.ylabel("C")
        plt.savefig("static/temp15.jpeg")
            
        fig, bx = plt.subplots()
        bx.plot(hum)
        bx.set_title("Humidity")
        plt.xlabel("Unit Time")
        plt.ylabel("%")
        plt.savefig("static/hum15.jpeg")
    
    sensor = BMP085.BMP085()
    pressure = sensor.read_pressure()
    altitude = sensor.read_altitude()
    sealevel_pressure = sensor.read_sealevel_pressure()
    pres = '{0:0.2f} Pa'.format(pressure)
    alti = '{0:0.2f} m'.format(altitude)
    sealvl = '{0:0.2f} Pa'.format(sealevel_pressure)
    temp2 = sensor.read_temperature()
    
    #calculating weather forecast
    
    h = 0.0065*altitude
    
    p0 =  pressure * (1-(h / (temp2 + h + 273.15)))**(-5.257)
    p0 = p0/10
     
    
    z_init = 179 - ( (2*p0) / (129) )
    
    z = round(z_init)
    state = ""
    if(z >= 1 and z <= 3) :
        state = "Fine Weather"
    elif(z >= 4 and z <= 9):
        state = "Rainy Weather"
    elif(z >= 10 and z <= 13) :
        state = "Fine Wheather"
    elif(z >= 14 and z <= 18) :
        state = "Possible Rainy Weather"
    elif(z==19):
        state = "Stormy with possible rain"
    elif(z >= 20 and z <=25):
        state = "Fine Weather"
    elif(z >= 26 and z <= 29) :
        state = "Unsettled Weather with improving condition"
    elif(z >= 30 and z <= 32) :
        state = "Stormy Weather with Much Rain"
    else :
        state = "unpredictable"
    
    templateData = {
            'title' : 'Weather Station by Orange Corp.',
            'time' : timeString,
            'temp':t,
            'hum':humidity,
            'pressure':pres,
            'sealevel_pressure':sealvl,
            'state':state,
            'fig1':ax,
            'fig2':bx
            }

    return render_template('index.html', **templateData)



def read_sensor(*args):
     try:
         humidity, temperature = Adafruit_DHT.read_retry(11,4)


         print('Temp: {0:0.1f}* C Humidity: {1:0.1f} %'.format(temperature,humidity))
         t ='{0:0.1f}'.format(temperature)
         return t,humidity
     except Exception as e:
         print('error '+str(e))
         GPIO.cleanup()

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=80, debug=True)


