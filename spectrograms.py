import numpy as np
import librosa
import os, re
 
TIMESTEP_LEN = 0
FEATURE_LEN = 514

emotions = {
    'n': '01',
    'ca': '02',
    'h': '03',
    'sa': '04',
    'a': '05',
    'f': '06',
    'd': '07',
    'su': '08',
}

def generate_spectrograms(in_folder, out_folder, regex, prefix=0):
    os.makedirs(out_folder, exist_ok=True)
    for actor_folder in os.listdir(in_folder):
        in_path = os.path.join(in_folder, actor_folder)

        for in_file in os.listdir(in_path):
            if regex.match(in_file):
                print(os.path.join(in_path, in_file))

                signal, sr = librosa.load(os.path.join(in_path, in_file), sr =44100)
                spectrogram = librosa.stft(signal, n_fft=512, hop_length=256)
                spectrogram = np.concatenate((spectrogram.real, spectrogram.imag), axis=0)

                # pad to longest audio
                spectrogram = np.pad(spectrogram, ((0, FEATURE_LEN-spectrogram.shape[0]), (0, TIMESTEP_LEN-spectrogram.shape[1])), 'constant').transpose()

                filename = in_file.split('.')[0]    # ravdess
                if(prefix):     # savee
                    symbol = re.match(r'[a-z][a-z]?', in_file.split('.')[0]).group(0)
                    filename = actor_folder + "-" + filename + "-" + emotions[symbol]
                
                np.save(os.path.join(out_folder, filename + '.npy'), spectrogram)

def max_len(datasets):
    for dataset in datasets:
        for actor_folder in os.listdir(dataset):
            in_path = os.path.join(dataset, actor_folder)
            for in_file in os.listdir(in_path):
                signal, sr = librosa.load(os.path.join(in_path, in_file), sr =44100)
                spectrogram = librosa.stft(signal, n_fft=512, hop_length=256)

                # finding with max length
                global TIMESTEP_LEN
                if(TIMESTEP_LEN < spectrogram.shape[1]):
                    TIMESTEP_LEN = spectrogram.shape[1]

    # timesteps and frequencies padded to multiple of 64
    TIMESTEP_LEN += 64-(TIMESTEP_LEN % 64)
    global FEATURE_LEN
    FEATURE_LEN += 64-(FEATURE_LEN % 64)

def ravdess():
     in_folder = 'ravdess-emotional-speech-audio'
     out_folder = 'spectrograms/ravdess'
     regex = re.compile('.+.wav')
     generate_spectrograms(in_folder, out_folder, regex)
 
def savee():
    in_folder = 'AudioData'
    out_folder = 'spectrograms/savee'
    regex = re.compile('[a-z]+0[1-3].wav')
    generate_spectrograms(in_folder, out_folder, regex, 1)
 
def main():
    datasets = ['ravdess-emotional-speech-audio', 'AudioData']
    max_len(datasets)
    ravdess()
    savee()

if __name__=='__main__':
    main()
