'''
    Author: Jon Wakefield
    Date: 03/26/2023
    
    Description: Pi Pico Blindspot detection with ultrasonic sensors.
                 Sensors: https://www.sparkfun.com/products/11309
                 Ultrasonic measurements read through UART.
                 UltraSonic sensor 1 - Core 0, Rx = 1, Tx = 0
                 UltraSonic Sensor 2 - Core 1, Rx = 5, Tx = 4
                 
                 Data transmitted back to heads up display computer (RPi 4b)
                 Through I2C communication (Pi Pico slave).
                 
'''
import utime
from time import sleep
from machine import mem32, UART, Pin
import led
from i2cslave import i2c_slave
import _thread


### --- check pico power on --- ###
led.led_power_on()

### --- pico connect i2c as slave --- ###
#s_i2c = i2c_slave(1, sda=18, scl=19, slaveAddress=0x41)

# set of gpio pin to idicate if object detected.
right_angle_gpio = Pin(18, Pin.OUT)
angle_45_gpio = Pin(19, Pin.OUT)
right_angle_gpio.value(0)
angle_45_gpio.value(1)
print(right_angle_gpio.value())


# Set-up our UARTs objects:
uart_0 = UART(0, baudrate=9600, tx=Pin(0), rx=Pin(1))
uart_1 = UART(1, baudrate=9600, tx=Pin(4), rx=Pin(5))

# Returns a new lock object. Provides a semaphore lock to both threads
sLock = _thread.allocate_lock()


def transmit_i2c(distance):
    ''' Function transmits back to heads up display
        through i2c.
        Function is called when an object is detected (distance < threshold)
    '''
    
    try:
        #s_i2c.put(int(distance))
        #print("Right angle transmitted...")
        right_angle_gpio.value(1)
        print(right_angle_gpio.value())
    except Exception as e:
        print(e)


def core0(uart_0):
    '''
        Right angle UltraSonic UART distance sensor: 
    '''
    def status_check():
        pass
    
    def check_threshold0(distance):
        '''
            Check if distance is below threshold.
            THRESHOLD: < 400 cm
            IF true: transmit data back to HUD computer
        '''
        threshold = 40
        if (distance < threshold):
            # Transmit back
            print("Object detected")
            transmit_i2c(distance)
        else:    
            right_angle_gpio.value(0)
            print(right_angle_gpio.value())
            
    
    def read_sensor0(uart_0):
        '''
        '''
        try:
            distance_b = uart_0.readline()
            
            #Right angle distance
            distance_str = str(distance_b)
            distance_list = distance_str.rsplit("'R")
            distance_list = distance_list[1].rsplit("\\")
            # Convert distance to cm:
            distance = int(distance_list[0]) / 10
            check_threshold0(distance)
            
            print(f"Distance Right Angle: {distance} cm")
        
        except Exception as e:
            print(e)
            
    
    while True:
        read_sensor0(uart_0)
        sleep(0.2)
        status_check()



def core1(uart_1):
    '''
        45degree UltraSonic UART distance sensor. 
    '''
    
    def check_threshold1(distance):
        ''''''
        pass
    
    def read_sensor1(uart_1):
        '''
        '''
        try:
            distance_b = uart_1.readline()
            
            #Right angle distance
            distance_str = str(distance_b)
            distance_list = distance_str.rsplit("'R")
            distance_list = distance_list[1].rsplit("\\")
            # Convert distance to cm:
            distance = int(distance_list[0]) / 10
            check_threshold1(distance)
            
            #print(f"Distance Corner Angle: {distance} cm")
        
        except Exception as e:
            #print(e)
            pass
            
    
    while True:
        read_sensor1(uart_1)
        sleep(0.2)




_thread.start_new_thread(core0, ([uart_0]))
#core1(uart_1)




