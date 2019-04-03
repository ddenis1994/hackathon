import speech_recognition as sr
r=sr.Recognizer()
with sr.Microphone() as source:
    print("SPELL A");
    audio=r.listen(source)
    print("TIME OVER, THANKS")

try:
    print("You Said: "+r.recognize_google(audio))
    if(r.recognize_google(audio)=='hey'):
        print("good job!")
    else:
        print("not good!");



    #print("TEXT: "+r.recognize_google(audio));
except:
    pass;
          
