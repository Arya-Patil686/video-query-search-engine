import json
import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft, fftfreq
from scipy import fft, signal
import scipy
from scipy.io.wavfile import read
from collections import defaultdict
import csv
from dotenv import load_dotenv


load_dotenv()

def create_constellation(audio, Fs):
    # Parameters
    window_length_seconds = 2

    window_length_samples = int(window_length_seconds * Fs)
    window_length_samples += window_length_samples % 2
    num_peaks = 15
    # Pad the song to divide evenly into windows
    amount_to_pad = window_length_samples - audio.size % window_length_samples
    song_input = np.pad(audio, (0, amount_to_pad))
    # Perform a short time fourier transform
    frequencies, times, stft = signal.stft(
        song_input, Fs, nperseg=window_length_samples, nfft=window_length_samples, return_onesided=True
    )
    constellation_map = defaultdict(list)
    for time_idx, window in enumerate(stft.T):
        # Spectrum is by default complex.
        # We want real values only
        spectrum = abs(window)
        # Find peaks - these correspond to interesting features
        # Note the distance - want an even spread across the spectrum
        peaks, props = signal.find_peaks(spectrum, prominence=0, distance=200)
        # Only want the most prominent peaks
        # With a maximum of 15 per time slice
        n_peaks = min(num_peaks, len(peaks))
        # Get the n_peaks largest peaks from the prominences
        # This is an argpartition
        # Useful explanation: https://kanoki.org/2020/01/14/find-k-smallest-and-largest-values-and-its-indices-in-a-numpy-array/
        largest_peaks = np.argpartition(props["prominences"], -n_peaks)[-n_peaks:]
        for peak in peaks[largest_peaks]:
            frequency = frequencies[peak]
            constellation_map[time_idx].append(frequency)

    return constellation_map

def export_json(file_dir, output_file):
    maps = defaultdict(dict)

    for audioname in os.listdir(file_dir):
        if audioname == '.DS_Store':
            continue
        filename = file_dir + "/" + audioname
        print(filename)
        Fs, song = read(filename)
        song = np.transpose(np.transpose(song)[0])
        map = create_constellation(song, Fs)
        maps[audioname] = list(map.values())

    with open(output_file, 'w') as file:
        json.dump(maps, file)


if __name__ == "__main__":
    export_json(os.getenv('AUDIOS_PATH'), os.getenv('AUDIO_DB_PATH'))