import machine
import utime
import math

adcpin = 26
thermistor = machine.ADC(adcpin)

while true:
    adc = thermistor.read_u16()
    Vout = (3.3/65535)*adc #This line converts the adc value from a range from 0-65535 to a range 0 - 3.3

    Moisture = -5*(thermistor.thermistorTemp(Vout)) + 105

    print(round(Moisture, 1), "%")

    sleep(5)

# Voltage Divider
Vin = 3.3
Ro = 10000  # 10k Resistor

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