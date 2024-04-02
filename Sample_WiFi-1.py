# This is a sample code that demonstrates wireless communication.
# You are expected to use this code and modify it to suit your project needs.

# ------------------------------------------------------------------------
# In this project, a red LED is connected to GP14.
# The red LED is controlled based on the value of a light sensor's output.
# The light sensor output is connected to GP26 (ADC pin).
# The red LED status and the value of the red LED pin (GP14) are communicated wirelessly to a server.
# The status and value are displayed on the webpage. In addition, the user interface has
# a circle indicating the LED turns color depending upon the status of the physical LED. 
# ------------------------------------------------------------------------


# -----------------------------------------------------------------------
# The following list of libraries are required. Do not remove any. 
import machine
import network
import usocket as socket
import utime as time
import _thread
import json
# -------------------------------------------------------------------------

# -------------------------------------------------------------------------

# The below portion of the code is to be tweaked based on your needs. 

# Configure GP14 as output and define it as redLED_pin 
LED_num = 14
greenLED_pin = machine.Pin(LED_num, machine.Pin.OUT)
greenLED_status = "Off" # Define a variable called redLED_status and set it to "Off"

# Define a function to get the red LED status
def get_greenLED_status():
    return "On" if greenLED_pin.value() == 1 else "Off"
# Note that the function returns the status.

# Define a function to periodically check the ADC pin and control the red LED pin.
def check_adc_and_control_greenLED():
    global greenLED_status  # Declare redLED_status as global. 
    adc = machine.ADC(26) # Configure GP26 as ADC pin.
    while True:
        LightSensor_value = adc.read_u16() # read the value of the ADC pin and save it in a variable.
        print("ADC Value:", LightSensor_value)

        if LightSensor_value > 4000: # the threshold value must be tuned based on test environment. 
            print("Mobile light off; turning on the red LED")
            redLED_pin.on() # set the GP14 pin to high (value = 1). 
        else:
            print("Mobile light on; turning off the red LED")
            redLED_pin.off() # set the GP14 pin to low (value = 0).

        redLED_status = get_redLED_status()  # Update redLED_status
        print("Red LED Status:", redLED_status)
        time.sleep(1) # wait for 1 second. 
# --------------------------------------------------------------------------

# --------------------------------------------------------------------------
# Below given code should not be modified (except for the name of ssid and password). 
# Create a network connection
ssid = 'RPI_PICO_AP'       #Set access point name 
password = '12345678'      #Set your access point password
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
    redLED_status = get_redLED_status()
    LED_color = "red" if redLED_status == "On" else "gray"
    greenLED = "green" if redLED_status == "Off" else "black"
    
# Modify the html portion appropriately.
# Style section below can be changed.
# In the Script section some changes would be needed (mostly updating variable names and adding lines for extra elements). 

    html = """<html lang="en">
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
        
        .switch:nth-child(1) {
            top: 50px; /* Set the top position of the second object */
            left: 0px; /* Set the left position of the second object */
        }
        .switch:nth-child(2) {
            top: 50px; /* Set the top position of the second object */
            left: 0px; /* Set the left position of the second object */
        }
        .switch:nth-child(3) {
            top: 50px; /* Set the top position of the second object */
            left: 0px; /* Set the left position of the second object */
        }


        /* Code for Switches from lab code given */
        .switch {
            position: relative;
            display: inline-block;
            width: 60px;
            height: 34px;
            
        }
        .switch input {
            opacity: 0;
            width: 0;
            height: 0;
        }
        .slider {
            position: absolute; top: 0; left: 0; right: 0; bottom: 0;
            border-radius: 34px;
            cursor: pointer;
            background-color: #ccc;
            -webkit-transition: .4s; transition: .4s;
        }
        .slider:before {
            position: absolute; height: 26px; width: 26px; left: 4px; bottom: 4px;
            content: "";
            border-radius: 50%;
            background-color: white;
            -webkit-transition: .4s; transition: .4s;
        }
        input:checked + .slider {
            background-color: #2196F3;
        }
        input:checked + .slider:before {
            -webkit-transform: translateX(26px);
            -ms-transform: translateX(26px);
            transform: translateX(26px);
        }

    </style>
</head>

<script>
    function updateStatus() {
        var xhr = new XMLHttpRequest();
        xhr.onreadystatechange = function() {
            if (xhr.readyState == 4 && xhr.status == 200) {
                var data = JSON.parse(xhr.responseText);
               
                document.getElementById("RedLEDStatus").innerHTML = data.RedLEDStatus;
                var buzzerColor = data.RedLEDStatus === "On" ? "red" : "gray";
                document.getElementById("buzzerIndicator").style.backgroundColor = buzzerColor;
                var greenLED = data.RedLEDStatus === "Off" ? "green" : "black";
                document.getElementById("greenLED").style.backgroundColor = greenLED;
            }
        };
        xhr.open("GET", "/status", true);
        xhr.send();
    }
    setInterval(updateStatus, 1000); // Refresh every 1 second
</script>

    <!--background colour to green-->
    <body style="background-color:rgb(82, 188, 117);">
    <h1 class = "title"> Garden Monitor</h1>


    <!--Infoboxes container-->
    <span class = "infoboxes">
    <div class="box">
        <h2>Temperature (C):</h2>
        <h3>25</h3>
        <label class="switch"> <!--Where you see switch is the actuator relating to that particular infobox-->
            <input type="checkbox">
            <span class="slider round"></span>
            <p>Fan</p>
            </label>
      </div>
      <div class="box">
        <h2>Soil Temperature (C):</h2>
        <h3>19</h3>
        <label class="switch">
            <input type="checkbox">
            <span class="slider round"></span>
            <p>Irrigation</p>
            </label>
      </div>
      <div class="box">
        <h2>Brightness:</h2>
        <h3>Sunny</h3>
        <label class="switch">
            <input type="checkbox">
            <span class="slider round"></span>
            <p>Lights</p>
            </label>
      </div>
    </span>

    <p>RedLED Status: <strong id="RedLEDStatus">""" + redLED_status + """</strong>
        <div class="circle" id="buzzerIndicator" style="background-color: """ + LED_color + """;"></div></p>
        <div class="circle" id="greenLED" style="background-color: """ + greenLED + """;"></div></p>  
        
</body>
</html>"""
    return html
# --------------------------------------------------------------------
# This section could be tweaked to return status of multiple sensors or actuators.

# Define a function to get the status of the red LED.
# The function retuns status. 
def get_status():
    status = {
        "RedLEDStatus": redLED_status,
        # You will add lines of code if status of more sensors is needed.
    }
    return json.dumps(status)
# ------------------------------------------------------------------------

# -------------------------------------------------------------------------
# This portion of the code remains as it is.

# Start the ADC monitoring function in a separate thread
_thread.start_new_thread(check_adc_and_control_redLED, ())

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



