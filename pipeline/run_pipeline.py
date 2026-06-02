import cv2
import supervision as sv

from pipeline.detector import PersonDetector
from pipeline.tracker import VisitorTracker
from pipeline.event_generator import EventGenerator
from pipeline.database_writer import DatabaseWriter
from pipeline.dwell import DwellTracker

from pipeline.zones import (
    draw_zones,
    get_zone
)

detector = PersonDetector()
tracker = VisitorTracker()
event_generator = EventGenerator()
database_writer = DatabaseWriter()
dwell_tracker = DwellTracker()

VIDEO_PATH = r"sample_data/videos/CAM 1.mp4"

SEEN_VISITORS = set()

cap = cv2.VideoCapture(VIDEO_PATH)

if not cap.isOpened():

    print(
        f"Failed to open video: {VIDEO_PATH}"
    )

    exit()

box_annotator = sv.BoxAnnotator()

while cap.isOpened():

    success, frame = cap.read()

    if not success:

        print(
            "Video completed."
        )

        break

    detections = detector.detect(
        frame
    )

    tracked_detections = tracker.update(
        detections
    )

    annotated_frame = box_annotator.annotate(
        scene=frame.copy(),
        detections=tracked_detections
    )

    current_visitors = len(
        tracked_detections
    )

    dwell_times = []

    if tracked_detections.tracker_id is not None:

        for i, tracker_id in enumerate(
            tracked_detections.tracker_id
        ):

            tracker_id = int(
                tracker_id
            )

            SEEN_VISITORS.add(
                tracker_id
            )

            x1, y1, x2, y2 = map(
                int,
                tracked_detections.xyxy[i]
            )

            center_x = int(
                (x1 + x2) / 2
            )

            center_y = int(
                (y1 + y2) / 2
            )

            zone = get_zone(
                center_x,
                center_y
            )

            dwell_time = dwell_tracker.get_dwell_time(
                tracker_id
            )

            dwell_times.append(
                dwell_time
            )

            event = event_generator.process(
                tracker_id,
                zone
            )

            if event:

                print(
                    f"EVENT GENERATED: {event}"
                )

                database_writer.save_event(
                    visitor_id=event[
                        "visitor_id"
                    ],
                    zone=event[
                        "zone"
                    ],
                    event_type=event[
                        "event_type"
                    ]
                )

            label = (
                f"ID:{tracker_id}"
            )

            if zone:

                label = (
                    f"ID:{tracker_id} | "
                    f"{zone} | "
                    f"{dwell_time}s"
                )

            cv2.putText(
                annotated_frame,
                label,
                (x1, y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 255, 0),
                2
            )

    annotated_frame = draw_zones(
        annotated_frame
    )

    avg_dwell = 0

    if dwell_times:

        avg_dwell = int(
            sum(dwell_times)
            / len(dwell_times)
        )

    height, width = annotated_frame.shape[:2]

    # Analytics Panel

    cv2.rectangle(
        annotated_frame,
        (width - 380, 10),
        (width - 10, 220),
        (0, 0, 0),
        -1
    )

    cv2.rectangle(
        annotated_frame,
        (width - 380, 10),
        (width - 10, 220),
        (0, 255, 0),
        2
    )

    cv2.putText(
        annotated_frame,
        "STORE ANALYTICS",
        (width - 360, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (0, 255, 0),
        2
    )

    cv2.putText(
        annotated_frame,
        f"Current Visitors: {current_visitors}",
        (width - 360, 80),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (255, 255, 255),
        2
    )

    cv2.putText(
        annotated_frame,
        f"Unique Visitors: {len(SEEN_VISITORS)}",
        (width - 360, 120),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (255, 255, 255),
        2
    )

    cv2.putText(
        annotated_frame,
        f"Avg Dwell: {avg_dwell}s",
        (width - 360, 160),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (255, 255, 255),
        2
    )

    cv2.putText(
        annotated_frame,
        "Zones Active: 2",
        (width - 360, 200),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (255, 255, 255),
        2
    )

    cv2.imshow(
        "Store Intelligence Tracking",
        annotated_frame
    )

    key = cv2.waitKey(1)

    if key == 27:

        print(
            "Stopped by user."
        )

        break

cap.release()
cv2.destroyAllWindows()