import sounddevice as sd
import librosa
import pyaudio
from src.feature_engineer import FeatureEngineer
import os
import warnings
import pickle 
from src.majority_voter import MajorityVoter
from src.baby_cry_predictor import BabyCryPredictor
import numpy as np
sr = 44100

duration = 10  # seconds
print("recordings")
myrecording = sd.rec(int(duration * sr), samplerate=sr, channels=1)
sd.wait()

play_list = list()

myrecording = myrecording.flatten()
sd.play(myrecording,samplerate=sr)
sd.wait()

for offset in range(5):
    audio_data = myrecording[offset * sr: (offset + 1)* sr]
    print("real data", audio_data.min(), audio_data.max(), audio_data.dtype, audio_data.ndim)
    play_list.append(audio_data)

engineer = FeatureEngineer()

play_list_processed = list()

for signal in play_list:
    tmp = engineer.feature_engineer(signal)
    play_list_processed.append(tmp)

with warnings.catch_warnings():
      warnings.simplefilter("ignore", category=UserWarning)

      with open((os.path.join('./data/audio_model/model.pkl')), 'rb') as fp:
          model = pickle.load(fp)

predictor = BabyCryPredictor(model)

predictions = list()

for signal in play_list_processed:
    tmp = predictor.classify(signal)
    print("snippet babycry:", tmp)
    predictions.append(tmp)
# MAJORITY VOTE

majority_voter = MajorityVoter(predictions)
majority_vote = majority_voter.vote()


print(majority_vote, "<---  majority vote")