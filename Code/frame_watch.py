import cv2

def display_frame(video_path, frame_number):
    # Open the video file
    cap = cv2.VideoCapture(video_path)
    
    # Check if the video file was successfully opened
    if not cap.isOpened():
        print("Error: Unable to open video file.")
        return
    
    # Set the frame number to read
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
    
    # Read the frame
    ret, frame = cap.read()
    
    # Check if the frame was successfully read
    if not ret:
        print(f"Error: Unable to read frame {frame_number}.")
        return
    
    # Display the frame
    cv2.imshow("Frame", frame)
    cv2.waitKey(0)  # Wait for a key press to exit
    # cv2.destroyAllWindows()

def display_frame_cap(frame):
    # Open the video file
    # cap = cv2.VideoCapture(video_path)
    
    # # Check if the video file was successfully opened
    # if not cap.isOpened():
    #     print("Error: Unable to open video file.")
    #     return
    
    # # Set the frame number to read
    # cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
    
    # # Read the frame
    # ret, frame = cap.read()
    
    # # Check if the frame was successfully read
    # if not ret:
    #     print(f"Error: Unable to read frame {frame_number}.")
    #     return
    
    # Display the frame
    cv2.imshow("Frame", frame)
    cv2.waitKey(0)  # Wait for a key press to exit
# Example usage:
# video_path = "C:/Users/meena/CSCI576-Multimedia-Project/Data/Queries/output1.mp4"
# frame_number = 12  # Change this to the frame number you want to display
# display_frame(video_path, frame_number)
# # display_frame(video_path = 'C:/Users/meena/CSCI576-Multimedia-Project/Data/Queries/video2_1.mp4', frame_number=200)
