import socket
import time
import numpy as np

IP = '127.0.0.1'
PORT = 5700

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

counter = 0

buttonPressed = 0
x=0.0
y=0.0
z=0.0
numberOfValues = 100
timeIndex = 0
xTime = np.linspace(0,31,numberOfValues,endpoint=False)
sine_wave_1 = np.sin( 0.2* xTime +1)
sine_wave_2 = 2*np.sin( 0.5* xTime +2)+2
sine_wave_3 = 2*np.sin( 0.7* xTime)
sine_wave_4 = 0.2*np.sin( 6* xTime)

while True:

    buttonWave = sine_wave_1[timeIndex] * sine_wave_2[timeIndex] * sine_wave_3[timeIndex] + sine_wave_4[timeIndex]
    xWave = sine_wave_1[timeIndex] + sine_wave_2[timeIndex] * sine_wave_3[timeIndex] + sine_wave_4[timeIndex]
    yWave = sine_wave_1[timeIndex] * (sine_wave_2[timeIndex]-5) + sine_wave_3[timeIndex] + sine_wave_4[timeIndex]
    zWave = sine_wave_1[timeIndex] * (sine_wave_2[timeIndex]+3) * sine_wave_3[timeIndex] * sine_wave_4[timeIndex]
    


    if(buttonWave >= 1):
        buttonPressed = 1
    else:
        buttonPressed = 0

    message = '{"button_1": '+str(buttonPressed)+', "accelerometer": { "x": '+str(xWave)+', "y": '+str(yWave)+', "z": '+str(zWave)+' }}'
    
    print(message)

    sock.sendto(message.encode(), (IP, PORT))
        
    

    if (timeIndex >= 100):
        timeIndex = 0;
    else: 
        timeIndex +=1
    counter += 1
    time.sleep(1)


    #TODO
    #Cleanup code
    #Add comments
    #PEP8 complient
    #virtual environment and a requirements.txt