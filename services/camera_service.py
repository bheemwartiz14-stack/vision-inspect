import cv2
import threading

class CameraStream:
    def __init__(self, source):
        if isinstance(source, int):
            self.cap = cv2.VideoCapture(source, cv2.CAP_DSHOW)
        else:
            self.cap = cv2.VideoCapture(source)

        self.frame = None
        self.ret = False
        self.running = True

        threading.Thread(target=self.update, daemon=True).start()

    def update(self):
        while self.running:
            if self.cap.isOpened():
                self.ret, self.frame = self.cap.read()

    def get_frame(self):
        return self.ret, self.frame

    def release(self):
        self.running = False
        if self.cap.isOpened():
            self.cap.release()


class CameraService:
    def __init__(self, config):
        self.cameras = {}
        for cam in config:
            self.cameras[cam["name"]] = CameraStream(cam["source"])

    def get_frame(self, name):
        return self.cameras[name].get_frame()

    def release_all(self):
        for cam in self.cameras.values():
            cam.release()