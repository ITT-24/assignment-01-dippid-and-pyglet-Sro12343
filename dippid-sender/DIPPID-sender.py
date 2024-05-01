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
number_of_values = 100
time_index = 0

#The basis for how to calculate a sinus wave with linespace is based on ChatGPT: The Prompt was: how do i calculate a sinus wave using import time and import numpy

#Construct the Sinus Waves
xTime = np.linspace(0,31,number_of_values,endpoint=False)
sine_wave_1 = np.sin( 0.2* xTime +1)
sine_wave_2 = 2*np.sin( 0.5* xTime +2)+2
sine_wave_3 = 2*np.sin( 0.7* xTime)
sine_wave_4 = 0.2*np.sin( 6* xTime)

while True:

    #What sin waves to use and their combination were designed with an online plotter https://www.desmos.com/calculator/w9jrdpvsmk?lang=de
    #simulate the current input values
    xWave = sine_wave_1[time_index] + sine_wave_2[time_index] * sine_wave_3[time_index] + sine_wave_4[time_index]
    yWave = sine_wave_1[time_index] * (sine_wave_2[time_index]-5) + sine_wave_3[time_index] + sine_wave_4[time_index]
    zWave = sine_wave_1[time_index] * (sine_wave_2[time_index]+3) * sine_wave_3[time_index] * sine_wave_4[time_index]
    buttonWave = sine_wave_1[time_index] * sine_wave_2[time_index] * sine_wave_3[time_index] + sine_wave_4[time_index]

    #Check if buttonvalue reached Threshould to be pressed 
    if(buttonWave >= 1):
        buttonPressed = 1
    else:
        buttonPressed = 0

    #Construct and send DIPPID-Message
    message = '{"button_1": '+str(buttonPressed)+', "gyroscope": { "x": '+str(xWave)+', "y": '+str(yWave)+', "z": '+str(zWave)+' }}'
    print(message)
    sock.sendto(message.encode(), (IP, PORT))
        
    
    #loop through time_index
    if (time_index >= 99):
        time_index = 0
    else: 
        time_index +=1
        
    time.sleep(1/24)
