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

with open((os.path.join('./data/audio_model/model.pkl')), 'rb') as fp:
    model = pickle.load(fp)

def recordSample():
    duration = 10  # seconds
    print("recordings")
    myrecording = sd.rec(int(duration * sr), samplerate=sr, channels=1)
    sd.wait()
    return myrecording.flatten()


def offsetSample(myrecording):
    play_list = list()
    for offset in range(5):
        audio_data = myrecording[offset * sr: (offset + 1)* sr]
        print("real data", audio_data.min(), audio_data.max(), audio_data.dtype, audio_data.ndim)
        play_list.append(audio_data)

    return play_list

def classifyAudio(play_list):

    engineer = FeatureEngineer()

    play_list_processed = list()

    for signal in play_list:
        tmp = engineer.feature_engineer(signal)
        play_list_processed.append(tmp)

    

    predictor = BabyCryPredictor(model)

    # predictions = list()

    for signal in play_list_processed:
        tmp = predictor.classify(signal)
        if tmp > 0: 
            return 1
        # predictions.append(tmp)


    # majority_voter = MajorityVoter(predictions)
    # majority_vote = majority_voter.vote()


    return 0