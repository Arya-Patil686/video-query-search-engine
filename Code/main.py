import json
import sys
import pickle

import numpy as np
from scipy.io.wavfile import read
import os
from dotenv import load_dotenv
from set_db import create_constellation
from file_matching import print_match, open_video_player, print_k_matches, find_matches
from scenedetect import detect, AdaptiveDetector
from find_min_distance import find_min_distance_index
from pixel_difference import match_frame_colors

load_dotenv()

audio_audio_db_path = os.getenv('AUDIO_DB_PATH')
shot_audio_db_path = os.getenv('SHOT_DB_PATH')

def extract_fourth_element(tuples_list):
    return [item[3] for item in tuples_list]

# Example usage:
if __name__ == "__main__":
    # Load the scenes from binary files
    with open(shot_audio_db_path, 'rb') as f:
        split_scenes = pickle.load(f)

    query_video = input("Enter query video (.mp4) path ") if len(sys.argv) < 3 else sys.argv[1]
    song_path = input("Enter query audio (.wav) path ") if len(sys.argv) < 3 else sys.argv[2]
    query_scene_list = detect(query_video, AdaptiveDetector(min_scene_len=15, luma_only=True))
    with open(audio_audio_db_path, 'r') as file:
        audio_db = json.load(file)
    Fs, song = read(song_path)
    song = np.transpose(np.transpose(song)[0])
    input = create_constellation(song, Fs)

    i = 0
    new_input = {}
    for index, value in enumerate(input):
        new_input[i] = []
        if input.get(i, None) is not None:
            new_input[i] = input[i]
        i += 1
    input = new_input


    if len(query_scene_list) < 3:
        print(f'Query video has no scene detected, using audio fingerprinting')
        # match using audio fingerprinting
        # matched_audios = print_k_matches(song_path, input, audio_db, k=int(os.getenv("K_AUDIO_MATCHES")))
        matched_audios = find_matches(audio_db, song_path, input, None, k = int(os.getenv("K_AUDIO_MATCHES")))
        # match using dominant colors
        print("Checking color distribution")
        matched_videos = match_frame_colors(matched_audios, query_video, k = 3)
        sorted_matched_videos = sorted(matched_videos)
        print("**************************************")
        print(f"FINAL MATCH: {sorted_matched_videos[0][2]} frame: {sorted_matched_videos[0][1]}")
        print("**************************************")
        open_video_player(sorted_matched_videos[0][2], sorted_matched_videos[0][1])
    else:
        print(f'Query video has scene detected. Finding videos with matching scene lengths')
        query_shot_lengths = []
        first_scene_frame = query_scene_list[1][0].get_frames()
        for scene in query_scene_list[1:-1]: # skip the first and last scene since the query might not start and end exactly at a scene cut
            query_shot_lengths.append(scene[1].get_frames() - scene[0].get_frames())
        print(f'There are {len(query_shot_lengths)} scene cuts in the query video')
        frame_old = query_scene_list[0][1].get_frames() - 1
        frame_new = query_scene_list[0][1].get_frames()
        closest_matches = []

        for video, shots in split_scenes.items():
            shot_lengths = extract_fourth_element(shots)
            idx = find_min_distance_index(shot_lengths, query_shot_lengths)
            if idx != -1:
                frame = shots[idx][2] - frame_old - 1
                if frame >= 0:
                    closest_matches.append((video.split(".")[0] + ".wav", shots[idx], frame))
                    print(f'Scene-detection filtering match: {video} with frame {frame}')
        # if len(closest_matches) > 0: # audio fingerprinting
        if len(closest_matches)==0:
            audio_matches = find_matches(audio_db, song_path, input, None, k = max(1, int(len(closest_matches) / 2)))
        else:
            audio_matches = find_matches(audio_db, song_path, input, [name for name, _, _ in closest_matches ], k = max(1, int(len(closest_matches) / 2)), matched_audios={match[0]: max(0, match[2] / int(os.getenv("VIDEO_FRAMERATE")) - 10) for match in closest_matches})
        if len(audio_matches) > 0: # match using dominant colors
            print("Matching using color distribution")
            matched_videos = match_frame_colors(audio_matches, query_video, k = 3)
            sorted_matched_videos = sorted(matched_videos)
            print("**************************************")
            print(f"FINAL MATCH: {sorted_matched_videos[0][2]} frame: {sorted_matched_videos[0][1]}")
            print("**************************************")
            open_video_player(sorted_matched_videos[0][2], sorted_matched_videos[0][1])
