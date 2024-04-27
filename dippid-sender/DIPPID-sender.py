import socket
import time
import numpy as np

IP = '127.0.0.1'
PORT = 5700

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

#Setup Variables
buttonPressed = 0
x=0.0
y=0.0
z=0.0
numberOfValues = 100
timeIndex = 0

#Construct the Sinus Waves
xTime = np.linspace(0,31,numberOfValues,endpoint=False)
sine_wave_1 = np.sin( 0.2* xTime +1)
sine_wave_2 = 2*np.sin( 0.5* xTime +2)+2
sine_wave_3 = 2*np.sin( 0.7* xTime)
sine_wave_4 = 0.2*np.sin( 6* xTime)

while True:

    #simulate the current input values
    xWave = sine_wave_1[timeIndex] + sine_wave_2[timeIndex] * sine_wave_3[timeIndex] + sine_wave_4[timeIndex]
    yWave = sine_wave_1[timeIndex] * (sine_wave_2[timeIndex]-5) + sine_wave_3[timeIndex] + sine_wave_4[timeIndex]
    zWave = sine_wave_1[timeIndex] * (sine_wave_2[timeIndex]+3) * sine_wave_3[timeIndex] * sine_wave_4[timeIndex]
    buttonWave = sine_wave_1[timeIndex] * sine_wave_2[timeIndex] * sine_wave_3[timeIndex] + sine_wave_4[timeIndex]

    #Check if buttonvalue reached Threshould to be pressed 
    if(buttonWave >= 1):
        buttonPressed = 1
    else:
        buttonPressed = 0

    #Construct and send DIPPID-Message
    message = '{"button_1": '+str(buttonPressed)+', "accelerometer": { "x": '+str(xWave)+', "y": '+str(yWave)+', "z": '+str(zWave)+' }}'
    print(message)
    sock.sendto(message.encode(), (IP, PORT))
        
    
    #loop through timeIndex
    if (timeIndex >= 99):
        timeIndex = 0
    else: 
        timeIndex +=1
        
    time.sleep(0.1)


    #TODO
    #Cleanup code
    #Add comments
    #PEP8 complient
    #LowerSleepTime -> les debugable but more realistic
    #virtual environment and a requirements.txt