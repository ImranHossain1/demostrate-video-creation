import os
import cv2
import json

# Specify the paths for input video, JSON file, and output video
input_video_path = 'input_folder/input_video.MOV'
json_file_path = 'input_folder/cam1_735.json'
output_video_path = 'output_folder/output_video.mp4'

# Create the output folder if it doesn't exist
output_folder = os.path.dirname(output_video_path)
os.makedirs(output_folder, exist_ok=True)

# Read the JSON file containing object detection results
with open(json_file_path, 'r') as file:
    detection_data = json.load(file)

# Load the input video
cap = cv2.VideoCapture(input_video_path)

# Get the video's properties
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = cap.get(cv2.CAP_PROP_FPS)

# Create an output video writer
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(output_video_path, fourcc, fps, (frame_width, frame_height))

# Iterate over each frame in the video
for frame_name, frame_data in detection_data.items():
    # Extract the object detection results for the current frame
    timestamp = frame_data['timestamp']
    objects = frame_data.copy()
    del objects['timestamp']

    # Read the frame from the input video
    ret, frame = cap.read()

    if not ret:
        break

    # Draw bounding boxes and labels on the frame to visualize the detected objects
    for obj_id, obj_data in objects.items():
        label = obj_data['type']
        x1 = int(obj_data['x1'])
        y1 = int(obj_data['y1'])
        x2 = int(obj_data['x2'])
        y2 = int(obj_data['y2'])

        # Draw the bounding box
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

        # Add label text
        label_text = f'{label} (ID: {obj_id})'
        cv2.putText(frame, label_text, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    # Write the modified frame to the output video
    out.write(frame)

# Release resources
cap.release()
out.release()

# Print a message indicating the completion of the video creation
print('Video creation complete!')
