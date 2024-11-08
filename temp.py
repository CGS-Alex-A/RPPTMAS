from machine import ADC, PWM, Pin
from time import sleep
import math

adcpin = 26
thermistor = ADC(adcpin)

# Voltage Divider
Vin = 3.3
Ro = 10000  # 10k Resistor

# Steinhart Constants
A = 0.001129148
B = 0.000234125
C = 0.0000000876741

blue = PWM(Pin("GPIO0", Pin.OUT))
red = PWM(Pin("GPIO2", Pin.OUT))
green = PWM(Pin("GPIO1", Pin.OUT))
buzz = PWM(Pin("GPIO3", Pin.OUT))
sleepTime = 3
ledPulse = 3556
# Initialize button pin (assuming a pull-up configuration)
but = Pin("GPIO4", Pin.IN, Pin.PULL_UP)
temp = ADC(Pin(26))  # Connect wiper to GP26

blue.freq(1000)
red.freq(1000)
green.freq(1000)
buzz.freq(1000)

while True:

    # Get Voltage value from ADC   
    adc = thermistor.read_u16()
    Vout = (3.3/65535)*adc
    
    # Calculate Resistance
    Rt = (Vout * Ro) / (Vin - Vout) 
    # Rt = 10000  # Used for Testing. Setting Rt=10k should give TempC=25
    
    # Steinhart - Hart Equation
    TempK = 1 / (A + (B * math.log(Rt)) + C * math.pow(math.log(Rt), 3))

    # Convert from Kelvin to Celsius
    TempC = TempK - 273.15
    TempC =  round(TempC, 1)
    TempC = 10
    for i in range(10,30):

        TempC = TempC + 1
    
    if TempC > 25:
        red.duty_u16(62213)
        blue.duty_u16(0)
        buzz.duty_u16(65535)

    elif TempC < 20:
        red.duty_u16(0)
        blue.duty_u16(int(TempC*2185))
        buzz.duty_u16(30000)

    else:
        while TempC < 25 and TempC > 20:
            for i in range(1,ledPulse):
                green.duty_u16(ledPulse)
                ledPulse = ledPulse-1
                print(ledPulse)
            for i in range(1,ledPulse+3555):
                green.duty_u16(ledPulse)
                ledPulse = ledPulse+1
                
                print(ledPulse)
            sleep(2)
            

        blue.duty_u16(0)
        red.duty_u16(0)
        buzz.duty_u16(0)

    sleep(0.25)

    