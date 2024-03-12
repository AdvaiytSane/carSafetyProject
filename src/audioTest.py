import time
from RiskAssessment import RiskAssessment
import sounddevice as sd
import audioAssesment

riskAss = RiskAssessment()

while True:                   
    startTime = time.time()    
    print(f"Running Audio Task at {startTime}")         
    print(f"started recording at {startTime}!!")
    audioSample = audioAssesment.recordSample()
    riskAss.updateAudioSample(audioSample)
    duration = time.time() - startTime
    print(f"finished recording and classification in {duration} sec.")
