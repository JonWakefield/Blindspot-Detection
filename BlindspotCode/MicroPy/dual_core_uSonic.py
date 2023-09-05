from machine import UART, Pin
from time import sleep
import _thread


# Set-up Each UART channel:
uart_0 = UART(0, baudrate=9600, tx=Pin(0), rx=Pin(1))

uart_1 = UART(1, baudrate=9600, tx=Pin(4), rx=Pin(5))


# Returns a new lock object. Provides a semaphore lock to both threads
sLock = _thread.allocate_lock()


def core0(uart_0):
    '''
    '''
    def status_check():
        pass
    
    def check_threshold0(distance):
        ''''''
        pass
    
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
            
            print(f"Distance Corner Angle: {distance} cm")
        
        except Exception as e:
            print(e)
            
    
    while True:
        read_sensor1(uart_1)
        sleep(0.2)




_thread.start_new_thread(core0, ([uart_0]))
core1(uart_1)
