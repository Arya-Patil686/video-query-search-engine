from collections import defaultdict
import csv
import math
import json
import os
import sys
import webbrowser

import librosa

import numpy as np
from scipy.fft import fft, fftfreq
from scipy import fft, signal
import scipy
from scipy.io.wavfile import read
import heapq
import matplotlib.pyplot as plt
import tempfile
from dotenv import load_dotenv

load_dotenv()

def open_video_player(video, frame):
    video = video[:-3] + 'mp4'
    videos_dir_path = os.getenv("ORIGINAL_VIDEOS_PATH")
    start_time_seconds = round(frame / 30)

    # Generate HTML content with the parameters embedded
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Video Player</title>
    </head>
    <body>
        <div id="video-player">
            <video id="myVideo" controls>
                <source src="{videos_dir_path}/{video}" type="video/mp4">
            </video>
        </div>
        <button onclick="resetVideo()">Reset Video</button>
        <script>
        let video = document.getElementById("myVideo");
        video.addEventListener('loadedmetadata', function () {{
            video.currentTime = {start_time_seconds};
        }});
        video.addEventListener('error', (e) => {{
            console.error('Error when attempting to load video: ' + e.message);
        }});
        function resetVideo() {{
        var video = document.getElementById("myVideo");
        video.currentTime = 0;
        }}
        </script>
    </body>
    </html>
    """

    with tempfile.NamedTemporaryFile('w', delete=False, suffix='.html') as f:
        f.write(html_content)
        temp_html_path = f.name

    webbrowser.open('file://' + temp_html_path)

def find_offset(within_file, find_file, window, load_offset = 0):
    sample_rate_for_matching = 8820
    y_within, sr_within = librosa.load(within_file, sr=sample_rate_for_matching, offset=load_offset)
    y_find, _ = librosa.load(find_file, sr=sr_within, duration = window)

    c = signal.correlate(y_within, y_find, mode='valid', method='fft')
    peak = np.argmax(c)
    offset = round(peak / sr_within, 2)

    return (load_offset + offset) * 30

def get_residual_clip(audio1, audio2):
    if len(audio1) != len(audio2):
        raise ValueError("Invalid comparison. Not same length")

    residual = 0
    for i in range(len(audio1)):
        for j in range(len(audio1[i])):
            residual += abs(audio1[i][j] - audio2[i][j])
    return residual

def get_residual_total(input, full):
    n, m = len(input), len(full)

    min_residual = math.inf
    min_index = 0
    for index in range(m - n + 1):
        residual = get_residual_clip(input, full[index : index + n])
        if residual < min_residual:
            min_residual = residual
            min_index = index
    return min_residual, min_index

def print_match(querypath, input, db):

    min_residual = math.inf
    match = None
    min_index = 0

    for file, full_audio in db.items():
        residual, index = get_residual_total(input, full_audio)
        if residual < min_residual:
            match = file
            min_residual = residual
            min_index = index


    print(match, min_residual, min_index)
    frame = find_offset('Data/Audio/Audios_DB_8/' + match, querypath, 5)
    print('frame: ' + str(int(frame)))
    # open_video_player(match, frame)

def print_k_matches(querypath, input, db, k=1):
    heap = []
    # min_residual = math.inf
    # match = None
    # min_index = 0

    for file, full_audio in db.items():
        residual, index = get_residual_total(input, full_audio)
        if (len(heap) < k):
            heapq.heappush(heap, (-residual, file, index))
            # print(heap[-1][0])
        else:
            if residual < -heap[0][0]:
                # match = file
                # min_residual = residual
                # min_index = index
                heapq.heappop(heap)
                heapq.heappush(heap, (-residual, file, index))

    heapq.heapify(heap)
    results_array = []
    for match in sorted(heap, reverse=True):
        print("Audio fingerprinting: ", match[1], -match[0], match[2])
        frame = find_offset('Data/Audio/Audios_DB_8/' + match[1], querypath, 5)
        print('frame: ' + str(int(frame)))
        results_array.append((match[1].split(".")[0] + ".mp4", int(frame)))
    return results_array
    # open_video_player(match, frame)

def find_matches(db, querypath, input, audio_list=None, k = 1, matched_audios = {}):
    heap = []
    for file, full_audio in db.items():
        if audio_list is not None and file not in audio_list:
            continue
        residual, index = get_residual_total(input, full_audio)
        if (len(heap) < k):
            heapq.heappush(heap, (-residual, file, index))
        else:
            if residual < -heap[0][0]:
                heapq.heappop(heap)
                heapq.heappush(heap, (-residual, file, index))
    heapq.heapify(heap)
    results = []
    db_path = 'Data/Audio/Audios_DB/'
    for match in sorted(heap, reverse=True):
        window_size = 8 # window size for matching audio
        if matched_audios.get(match[1], None) is None:
            frame = find_offset(db_path + match[1], querypath, window_size)
        else:
            start_offset = max(matched_audios[match[1]] - window_size, 0)
            frame = find_offset(db_path + match[1], querypath, window_size, start_offset)
        print('Audio fingerprinting: ' + match[1] + ' frame: ' + str(int(frame)))
        results.append((match[1].split(".")[0] + ".mp4", int(frame)))
    return results

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
