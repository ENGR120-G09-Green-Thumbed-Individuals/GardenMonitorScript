
# -----------------------------------------------------------------------
# The following list of libraries are required. Do not remove any. 
import machine
import network
import usocket as socket
import utime as time
import _thread
import json
import math
# -------------------------------------------------------------------------
adcpin = 27 
thermistor = machine.ADC(adcpin)
adcpin2 = 28
thermistor2 = machine.ADC(adcpin2)

#Initialize LED pin as output
led_pin = machine.Pin(15, machine.Pin.OUT)

# Initialize photoresistor pins
adcpin3 = 26
photoresistor = machine.ADC(adcpin3) 

# Threshold values for the led. 
threshold_sunny = 30000


def thermistorTemp(Vout):

    # Voltage Divider
    Vin = 3.3
    Ro = 10000  # 10k Resistor

    # Steinhart Constants
    A = 0.001129148 #Experimentally found by using Steinhart equation
    B = 0.000234125
    C = 0.0000000876741
    
    VoutVolts = (3.3/65535)*Vout
    # Calculate Resistance
    Rt = (VoutVolts * Ro) / (Vin - VoutVolts)
    
    # Steinhart - Hart Equation
    TempK = 1 / (A + (B * math.log(Rt)) + C * math.pow(math.log(Rt), 3))

    # Convert from Kelvin to Celsius
    TempC = round((TempK - 273.15 - 7), 1) #The Steinhardt equation is so close but it's off by about 9 degrees each time, therefore we subtract 9 from TempC

    print("Current Temperature is: " + str(TempC) + " C")

    return TempC

def check_brightness():
    
    global LEDstatus
    global weather
    global water_actuator_status
    global TempCSoil
    global fan_actuator_status
    global TempCAir
    
    while True:
        photoresistor_value = photoresistor.read_u16()
        
        if photoresistor_value <= threshold_sunny:
            print("It's bright enough, no need for lights")
            print (photoresistor_value)
            led_pin.off()
            LEDstatus = "Off"
            weather = "Sunny"
        else:
            print("Too dark, lights on!")
            print (photoresistor_value)
            led_pin.on()
            LEDstatus = "On"
            weather = "Dark"
        
        TempCSoil = thermistorTemp(thermistor.read_u16())
        if TempCSoil >= 20:
            print("Turn on Irrigation. Soil is dry")
            water_actuator_status = "On"
        else:
            print("Irrigation off")
            water_actuator_status = "Off"

        # Convert air thermistor resistance to temperature in celsius
        TempCAir = thermistorTemp(thermistor2.read_u16())
        if TempCAir >= 20:
            print("Turn on Fan. Air is too hot")
            fan_actuator_status = "On"
        else:
            print("Fan off")
            fan_actuator_status = "Off"

        time.sleep(3)
        print ("Current States:")
        print ("LED status:", LEDstatus)
        print ("Weather is: ", weather)
        print ("Irrigation is: ", water_actuator_status)
        print ("Soil Temperature is: ", str(TempCSoil))
        print ("Fans are :", fan_actuator_status)
        print ("Air Temperature is: ", str(TempCAir))
        time.sleep(3)

    

# --------------------------------------------------------------------------

# --------------------------------------------------------------------------
# Below given code should not be modified (except for the name of ssid and password). 
# Create a network connection
ssid = 'RPI_PICO_AP'       #Set access point name 
password = 'Passwerd'      #Set your access point password
ap = network.WLAN(network.AP_IF)
ap.config(essid=ssid, password=password)
ap.active(True)            #activating

while ap.active() == False:
  pass
print('Connection is successful')
print(ap.ifconfig())

# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# Below given code defines the web page response. Your html code must be used in this section.
# 
# Define HTTP response
def web_page():
    LED_color = "red" if LEDstatus == "On" else "gray"
    weather = "Dark" if LEDstatus == "On" else "Sunny"
    HTMLTempAir = TempCAir
    HTMLTempSoil = TempCSoil
    fan_LED_colour = "green" if fan_actuator_status == "On" else "grey"
    water_LED_color = "blue" if water_actuator_status == "On" else "grey"
    
# Modify the html portion appropriately.
# Style section below can be changed.
# In the Script section some changes would be needed (mostly updating variable names and adding lines for extra elements). 

    html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GardenProject</title>
    <style>
        /*Title*/
        .title{
            text-align: center;
        }
        /* Here's the code for the info boxes which will have our temps and sunniness */
        .infoboxes {
            display: absolute;
            justify-content: space-between;
            align-items: flex-start;
            flex-wrap: wrap;  
        }

        .box {
            width: 30%; /* Set the width of each box */
            height: 150px; /* Set the height of each box */
            background-color: #f0f0f0; /* Set the background color of each box */
            border: 1px solid #ccc; /* Add border for each box */
            margin-right: 5px; /* Add margin between boxes */
            margin-left: 5px;
            margin-top: 100px;
            display: inline-block; /* Align boxes horizontally */
        }

         /*  Center text inside each box */
        .box h2,
        .box h3 {
            text-align: center;
        }

        /* Here's where the code for the switches are...*/
        
        .dot {
            position: relative;
            height: 25px;
            width: 25px;
            background-color: #bbb;
            border-radius: 50%;
            display: block; /* Change from inline-block to block */
            margin: 10px auto; /* Center the dots horizontally with some margin */
        }

        .dot-text {
            text-align: center; /* Center align the text */
            position: relative; /* Add some margin between the dot and the text */
            top: 25px;
        }
    </style>
    <script>
        function updateStatus() {
            var xhr = new XMLHttpRequest();
            xhr.onreadystatechange = function() {
                if (xhr.readyState == 4 && xhr.status == 200) {
                    var data = JSON.parse(xhr.responseText);
                    document.getElementById("LEDStatus").innerHTML = data.LEDStatus;
                    var LEDColour = data.LEDStatus === "On" ? "red" : "gray";
                    document.getElementById("LEDIndicator").style.backgroundColor = LEDColour;
                    document.getElementById("WeatherIndicator").innerHTML = data.WeatherIndicator;
                    document.getElementById("SoilTemp").innerHTML = data.SoilTemp;
                    document.getElementById("waterLEDStatus").innerHTML = data.waterLEDStatus;
                    var waterColour = data.waterLEDStatus === "On" ? "blue" : "gray";
                    document.getElementById("waterLEDIndicator").backgroundColor = waterColour;
                    document.getElementById("AirTemp").innerHTML = data.AirTemp;
                    document.getElementById("fanLEDStatus").innerHTML = data.fanLEDStatus;
                    var fanColour = data.fanLEDStatus === "On" ? "green" : "gray";
                    document.getElementById("fanLEDIndicator").backgroundColor = fanColour;
                    
                }
            };
            xhr.open("GET", "/status", true);
            xhr.send();
        }
        setInterval(updateStatus, 1000); 
    </script>
</head>
    <!--background colour to green-->
    <body style="background-color:rgb(82, 188, 117);">
    <h1 class = "title"> Garden Monitor</h1>


    <div class="infoboxes">
        <div class="box">
            <h2>Temperature (C):</h2>
            <h3 id = "AirTemp">""" + str(TempCAir) + """</h3>
                <p>Fan: <strong id="fanLEDStatus">""" + fan_actuator_status + """</strong><div class="dot" id="fanLEDIndicator" style="background-color: """ + fan_LED_colour + """; margin-top: -30px"></div></p>
        </div>
        <div class="box">
            <h2>Soil Temperature (C):</h2>
            <h3 id = "SoilTemp">""" + str(TempCSoil) + """</h3>
                <p>Irrigation: <strong id="waterLEDStatus">""" + water_actuator_status + """</strong><div class="dot" id="waterLEDIndicator" style="background-color: """ + water_LED_color + """; margin-top: -30px"></div></p>
        </div>
        <div class="box">
            <h2>Brightness:</h2>
            <h3 id="WeatherIndicator">""" + weather + """</h3>
            <p>LED Status: <strong id="LEDStatus">""" + LEDstatus + """</strong><div class="dot" id="LEDIndicator" style="background-color: """ + LED_color + """; margin-top: -30px"></div></p>
        </div>
    </div>

</body>
</html>"""
    return html
# --------------------------------------------------------------------
# This section could be tweaked to return status of multiple sensors or actuators.

# Define a function to get the status of the red LED.
# The function retuns status. 
def get_status():
    status = {
        "LEDStatus": LEDstatus,
        "WeatherIndicator": weather,
        "SoilTemp": TempCSoil,
        "AirTemp": TempCAir,
        "waterLEDStatus": water_actuator_status,
        "fanLEDStatus": fan_actuator_status 
    }
    return json.dumps(status)
# ------------------------------------------------------------------------

# -------------------------------------------------------------------------
# This portion of the code remains as it is.

# Start the ADC monitoring function in a separate thread
_thread.start_new_thread(check_brightness, ())

# Create a socket server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)

# --------------------------------------------------------------------------

# --------------------------------------------------------------------------

# This section of the code will have minimum changes. 
while True:
    conn, addr = s.accept()
    print('Got a connection from %s' % str(addr))
    request = conn.recv(1024)
    if request:
            request = str(request)
            print('Content = %s' % request)

# this part of the code remains as it is. 
    if request.find("/status") == 6:
        response = get_status()
        conn.send("HTTP/1.1 200 OK\n")
        conn.send("Content-Type: application/json\n")
        conn.send("Connection: close\n\n")
        conn.sendall(response)
    else:
        response = web_page()
        conn.send("HTTP/1.1 200 OK\n")
        conn.send("Content-Type: text/html\n")
        conn.send("Connection: close\n\n")
        conn.sendall(response)
    conn.close()


