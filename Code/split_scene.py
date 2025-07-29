import pickle
import cv2
from scenedetect import detect, AdaptiveDetector
import os
from dotenv import load_dotenv


load_dotenv()

video_root = os.getenv('VIDEOS_PATH')
NUM_VIDEOS = 20

# Initial the dictionary
split_scenes = {}
video_paths = []
for i in range(1, NUM_VIDEOS + 1):
    split_scenes[f'video{i}.mp4'] = []
    video_paths.append(video_root + f'video{i}.mp4')

# Get the scenes from the videos
for i, video_path in enumerate(video_paths):
    print(f"Processing video{i+1}...")
    scene_list = detect(video_path, AdaptiveDetector(min_scene_len=15, luma_only=True))
    cap = cv2.VideoCapture(video_path)
    # For all scene except the last one
    for scene in scene_list[:-1]:
        frame_old, frame_new = scene[1].get_frames()-1, scene[1].get_frames()
        split_scenes[video_path.split('/')[-1]].append((None, None, frame_old, scene[1].get_frames() - scene[0].get_frames()))



# Save the scenes to binary files
with open(os.getenv('SHOT_DB_PATH'), 'wb') as f:
    pickle.dump(split_scenes, f)
