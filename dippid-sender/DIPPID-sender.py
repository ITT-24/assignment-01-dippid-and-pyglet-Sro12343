import socket
import time
import numpy as np

IP = '127.0.0.1'
PORT = 5700

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

counter = 0

flipflop = 1
x=0.0
y=0.0
z=0.0



while True:
    #'{"capabilities" : ["accelerometer","gyroscope"] , "accelerometer data:" {"x": -0.010006348 , "y":0.01952458 , "z":1.0057904}}'
    
    #message = '{ "capabilities": ["accelerometer", "button_1"], "button_1":1,"accelerometer": { "x": -0.010006348, "y": 0.01952458, "z": 1.0057904 }}'

    
    
    
    #TODO
    #Simulate ButtonPress
    #Simulate Accelerometer
    #Cleanup code
    #Add comments
    
    

    if(flipflop == 1):
        flipflop = 0
    else:
        flipflop = 1

    message = '{"button_1": '+str(flipflop)+', "accelerometer": { "x": -0.010006348, "y": 0.01952458, "z": 1.0057904 }}'
    
    print(message)

    sock.sendto(message.encode(), (IP, PORT))
        
    


    counter += 1
    time.sleep(1)


