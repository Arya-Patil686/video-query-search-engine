import cv2
import numpy as np
import sys
import os
from frame_watch import display_frame_cap

def extract_frame(video_path, frame_number):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Error: Could not open video file")
        return None
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
    ret, frame = cap.read()
    cap.release()

    if not ret:
        print(f"Error: Could not read frame {frame_number} from the video")
        return None

    return frame

def compare_videos(video1_path, video2_path, frame1_number, frame2_number, comparison_algorithm, sum):

    frame1 = extract_frame(video1_path, frame1_number)
    # display_frame_cap(frame1)
    frame2 = extract_frame(video2_path, frame2_number)
    # display_frame_cap(frame2)
    comparison_result = comparison_algorithm(frame1, frame2)
    sum = comparison_result
 
    # combined_sum = sum[0]+sum[1]+sum[2]
    return sum



def pixel_difference(frame1, frame2):
    # Compute absolute difference between frames
    diff = cv2.absdiff(frame1, frame2)
    sq_diff = diff.flatten().astype(int) ** 2

    # Compute the sum of absolute differences separately for each channel
    sum_diff = np.sum(sq_diff)#, axis=(0, 1))

    return sum_diff


def match_frame_colors(given_list, query_video_path, query_frame = 0, k=0):
    error_list_main = []

    for item in given_list:
        video_path1 = os.getenv('VIDEOS_PATH') + item[0] # video
        video_path2 =  query_video_path #query video
        frame_number1 = item[1]
        frame_number2 = query_frame
        cap = cv2.VideoCapture(video_path1)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        cap.release()

        minimum_error = sys.maxsize
        if k==0:
            sum = [0,0,0]
            minimum_error = compare_videos(video_path1, video_path2, frame_number1, frame_number2, pixel_difference, sum)
            frame_number = frame_number1
        else:
            for i in range (frame_number1-k,frame_number1+k):
                if i<0: continue
                if i>total_frames: continue
                sum = [0,0,0]
                error = compare_videos(video_path1, video_path2, i, frame_number2, pixel_difference, sum)
                if error<minimum_error:
                    minimum_error = error
                    frame_number = i

        

        error_list_main.append([minimum_error,frame_number, item[0]])


    return error_list_main


if __name__ == "__main__":
    # This code block will execute only if this file is run directly
    query_video_path = 'C:/Users/meena/CSCI576-Multimedia-Project/Data/Queries/video1_1.mp4'
    list1 = [['C:/Users/meena/CSCI576-Multimedia-Project/Data/Queries/video1_1.mp4', 5], ['C:/Users/meena/CSCI576-Multimedia-Project/Data/Queries/video2_1.mp4',200]]
    error_list =initial(list1, query_video_path, k=30)
    print(error_list)