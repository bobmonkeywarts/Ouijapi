#!/usr/bin/env python3
# Requires PyAudio and PySpeech.

import speech_recognition as sr 
import os
import os.path
import sys

try:
    import apiai
except ImportError:
    sys.path.append(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir)
    )
    import apiai

from gpiozero import Button, LED, PWMLED

button = Button(17)
switch = Button(21)
led = PWMLED(18)
red = LED(26)

os.system("espeak \"Boo! I'm a ghost.\"")
while True:
	while button.is_pressed or switch.is_pressed:
		# Record Audio
		r = sr.Recognizer()
		with sr.Microphone() as source:
			red.off()
			led.pulse()
			print("Say something!")
   	 		audio = r.listen(source)
			led.off()
 
		speech = ""
		print("Audio recived. Now parsing.")
		# Speech recognition using Google Speech Recognition
		try:
   			 # for testing purposes, we're just using the default API key
   			 # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
			 # instead of `r.recognize_google(audio)`
	   		 speech = r.recognize_google(audio)
	 		 print("You said: " + speech)
		except sr.UnknownValueError:
		    	speech = "What? I didn't understand that."
	   		print("Google Speech Recognition could not understand audio")
			red.on()
		except sr.RequestError as e:
		    speech = "I'm having trouble connecting to the spirits right now. Check your internet connection."
		    print("Could not request results from Google Speech Recognition service; {0}".format(e))
	
		if ("goodbye" in speech):
			print("Goodbye!")
			os.system("espeak Goodbye")
			button.wait_for_press()
		if (speech != "What? I didn't understand that." and "goodbye" not in speech):
		
			print("sucessfuly recognised audio")
	
			CLIENT_ACCESS_TOKEN = '607802dbf3db4020bda8cc117d33ddbd'
			ai = apiai.ApiAI(CLIENT_ACCESS_TOKEN)
	
			request = ai.text_request()
			request.query = speech
			rawresponse = request.getresponse()
			response = rawresponse.read()
			parsed = response[response.index("\"speech\": \"")+11:]
			parsed = parsed[:parsed.index("\"")]
			parsed = parsed.replace("\u0027", "\'")
			print(parsed)
			print("Loading speech recognition...")
			os.system("espeak \"" + parsed + "\"")
