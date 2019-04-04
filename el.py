import numpy as np
import sounddevice as sd

duration = 3 #in seconds
volume_list=[]

def audio_callback(indata, frames, time, status):
   volume_norm = np.linalg.norm(indata) * 10
   volume_list.append(int(volume_norm))
   return ("-" * int(volume_norm))
   
   


stream = sd.InputStream(callback=audio_callback)
with stream:
   sd.sleep(duration * 1000)
   #print(sum(volume_list)/len(volume_list))
   print(max(volume_list))
   print(min(volume_list))
    
