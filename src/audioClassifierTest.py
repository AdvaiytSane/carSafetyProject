from baby_cry_predictor import BabyCryPredictor
import pickle
import os
import librosa
import audioAssesment

with open((os.path.join('./data/audio_model/model.pkl')), 'rb') as fp:
    model = pickle.load(fp)

test_data = [
     './data/babyCry/Louise_01.m4a_1.wav',
     'data/babyCry/margot.m4a_1.wav',
     'data/babyCry/margot.m4a_2.wav',
     'data/babyCry/margot.m4a_3.wav'
]

def read_audio_file(file_name):
        """
        Read audio file using librosa package. librosa allows resampling to desired sample rate and convertion to mono.

        :return:
        * play_list: a list of audio_data as numpy.ndarray. There are 5 overlapping signals, each one is 5-second long.
        """

        play_list = list()

        for offset in range(5):
            audio_data, sr = librosa.load(path=file_name, sr=44100, mono=True, offset=offset, duration=5.0)
            play_list.append(audio_data)

        return play_list, sr

for file_n in test_data:
     p, sr = read_audio_file(file_n)
     print(file_n)
     audioAssesment.classifyAudio(p)
