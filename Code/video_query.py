import pickle
import cv2

from scenedetect import detect, ContentDetector
from motion_vector import compute_motion_vector

# Load the scenes from binary files
with open('./Data/split_scenes.pkl', 'rb') as f:
    split_scenes = pickle.load(f)

# Compare for all query videos
query_video_path = './Data/Queries/video{}_1.mp4'
for i in range(1, 12):
    query_video = query_video_path.format(i)
    query_scene_list = detect(query_video, ContentDetector(min_scene_len=15))
    if len(query_scene_list) == 0:
        print(f'Query video{i}_1 has no scene detected')
        continue
    frame_old = query_scene_list[0][1].get_frames() - 1
    frame_new = query_scene_list[0][1].get_frames()
    cap = cv2.VideoCapture(query_video)
    motion_vector = compute_motion_vector(cap, frame_old, frame_new)
    motion_vector2 = compute_motion_vector(cap, frame_old-4, frame_new)
    for video, shots in split_scenes.items():
        for shot in shots:
            diff = None
            diff2 = None
            if motion_vector.shape == shot[0].shape:
                diff = motion_vector - shot[0]
            if motion_vector2.shape == shot[1].shape:
                diff2 = motion_vector2 - shot[1]
            if diff is None or diff2 is None:
                continue
            if (diff < 0.00001).all() and (diff2 < 0.00001).all():
                print(f'Query video{i}_1 is from {video} with frame {shot[2]-frame_old-1}')