import cv2
from ultralytics import YOLO
from PIL import ImageGrab#screen shot

# Load the YOLOv8 model
model = YOLO("yolov8n-seg.pt")

# Open the video file
video_path = "../../../../杂项/元首的愤怒.mp4"
#cap = cv2.VideoCapture(video_path)
cap = cv2.VideoCapture(0)

# Loop through the video frames
while cap.isOpened():
    # Read a frame from the video
    #success, frame = cap.read()
    
    success=1
    frame = ImageGrab.grab()
    #元组里的元素分别是：（距离图片左边界距离x， 距离图片上边界距离y，距离图片左边界距离+裁剪框宽度x+w，距离图片上边界距离+裁剪框高度y+h）
    #frame = frame.crop((50,320,960,960))
    frame = frame.crop((480,320,1440,960))

    if success:
        # Run YOLOv8 inference on the frame
        results = model(frame)

        # Visualize the results on the frame
        annotated_frame = results[0].plot()

        # Display the annotated frame
        cv2.imshow("YOLOv8 Inference", annotated_frame)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    else:
        # Break the loop if the end of the video is reached
        break

# Release the video capture object and close the display window
cap.release()
cv2.destroyAllWindows()
