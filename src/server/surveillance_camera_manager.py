from server.server_pipeline import ServerPipeline

import cv2

class SurveillanceCameraManager:
    def __init__(self, cam_id, camera_url, server_pipeline: ServerPipeline):
        # camera_url为0表示笔记本内置摄像头，为文件路径或远程摄像头地址（http service）则表示外接摄像头
        self.server_pipeline = server_pipeline
        self.cam_id = cam_id
        self.cap = cv2.VideoCapture(camera_url)

    def run(self):
        while self.cap.isOpened():
            success, frame = self.cap.read()
            if success:
                self.server_pipeline.insert_new_data_from_img(frame, self.cam_id)
            else:
                break
