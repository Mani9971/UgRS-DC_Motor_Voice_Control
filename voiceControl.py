import speech_recognition as sr
import time
import os, sys
import serial
import re
from subprocess import call

r = sr.Recognizer()
m = sr.Microphone()

#PORT = '/dev/ttyUSB0'#python3 -m serial.tools.list_ports //izlistanje svih mogucih portova
PORT = '/dev/ttyACM0'
SPEED = 9600#BAUDRATE

def say(text):
    call(['espeak','-v','hr', text])

#Funkcija dohvaća sve postotke u Stringu te uzima
# prvu vrijednost u rasponu od 0-100 i vraća ju bez znaka %.
def getValue(text):
    values = re.findall('\d*%', text)
    for value in values:
        if (value != '') & (value != '%'):
            if int(value[:-1]) in range(101):
                return f"<{value[:-1]}>"
    return False
#Serial communication setup
ser = serial.Serial(PORT, SPEED)#Brojevi se salju odvojeno npr. 23, prvo se posalje 2 pa onda 3

try:
    print("A moment of silence, please...")
    with m as source: r.adjust_for_ambient_noise(source)
    print("Set minimum energy threshold to {}".format(r.energy_threshold))
    while True:
        print("Say something!")
        with m as source: audio = r.listen(source)
        print("Got it! Now to recognize it...")
        try:
            # recognize speech using Google Speech Recognition
            text = r.recognize_google(audio, language="sr-SP")
            value = getValue(text)
            if value != False:
                try:
                    say(value)
                    ser.write(value.encode())
                except:
                    say("Nepoznata vrijednost")
            else:
                say("Nepoznata vrijednost")
        except sr.UnknownValueError:
            print("Oops! Didn't catch that")
        except sr.RequestError as e:
            print("Uh oh! Couldn't request results from Google Speech Recognition service; {0}".format(e))
        time.sleep(0.5) # sleep for a little bit
except KeyboardInterrupt:
    pass