import machine
import utime
import math

adcpin = 15 
thermistor = machine.ADC(adcpin)
adcpin2 = 26
thermistor2 = machine.ADC(adcpin2)

#Initialize LED pin as output
led = machine.Pin(25, machine.Pin.OUT)

# Initialize photoresistor pins
adcpin = 15
photoresistor = machine.ADC(adcpin) 

# Threshold values for the led. 
threshold_sunny = 10000
threshold_cloudy = 35000
threshold_night = 5000

# While loop that controls when the led turns on and off. If the the photoresistor reads a value greater than the sunny value, led will turn off.
while True:
    sensor_value = sensor_pin.read()
    sleep(5)

    if sensor_value >= threshold_sunny or sensor_value <= threshold_night :
        led.off()

    else:
        led.on()


    sleep(1)

while True:
    adc = thermistor.read_u16() #Temperature
    Vout = (3.3/65535)*adc #This line converts the thermistor voltage value from a range from 0-65535 to a range 0 - 3.3
    adc2 = thermistor2.read_u16() #Moisture
    Vout2 = (3.3/65535)*adc2 #This line converts the thermistor2 value from a range from 0-65535 to a range 0 - 3.3

    Moisture = -5*(thermistor2.thermistorTemp(Vout2)) + 105 #This value gives an approximate conversion of soil temperature to soil moisture 

    TempC = thermistor.thermistorTemp(Vout)

    print(round(TempC, 1))
   
    print(round(Moisture, 1), "%")

    sleep(5)


def thermistorTemp(Vout):

    # Voltage Divider
    Vin = 3.3
    Ro = 10000  # 10k Resistor

    # Steinhart Constants
    A = 0.001129148 #Experimentally found by using Steinhart equation
    B = 0.000234125
    C = 0.0000000876741

    # Calculate Resistance
    Rt = (Vout * Ro) / (Vin - Vout) 
    
    # Steinhart - Hart Equation
    TempK = 1 / (A + (B * math.log(Rt)) + C * math.pow(math.log(Rt), 3))

    # Convert from Kelvin to Celsius
    TempC = TempK - 273.15

    return TempC