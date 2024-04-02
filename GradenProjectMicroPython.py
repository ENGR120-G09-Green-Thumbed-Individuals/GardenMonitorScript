import machine #Import machine library
import utime #Import time library
import math #Import python math library

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


# While loop that controls when the led turns on and off. If the the photoresistor reads a value greater than the sunny value, led will turn off.
while True:
    photoresistor_value = photoresistor.read_u16()
    print(photoresistor_value)
    utime.sleep(1)

    if photoresistor_value <= threshold_sunny:
        led_pin.off()
    else:
        led_pin.on()
    utime.sleep(1)

    adc = thermistor.read_u16() #Temperature
    Vout = (3.3/65535)*adc #This line converts the thermistor voltage value from a range from 0-65535 to a range 0 - 3.3
    adc2 = thermistor2.read_u16() #Moisture
    Vout2 = (3.3/65535)*adc2 #This line converts the thermistor2 value from a range from 0-65535 to a range 0 - 3.3

    Moisture = -3*(thermistorTemp(Vout2)) + 105 #This value gives an approximate conversion of soil temperature to soil moisture 

    TempC = thermistorTemp(Vout)

    print(round(TempC, 1))
   
    print(round(Moisture, 1), "%")

    utime.sleep(1)

