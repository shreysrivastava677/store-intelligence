from ultralytics import YOLO
import supervision as sv


class PersonDetector:

    def __init__(self):

        self.model = YOLO("yolov8n.pt")

    def detect(self, frame):

        result = self.model(
            frame,
            classes=[0],
            verbose=False
        )[0]

        detections = sv.Detections.from_ultralytics(
            result
        )

        return detections