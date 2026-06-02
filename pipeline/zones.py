import cv2

ZONE_BOUNDARIES = {

    "SKINCARE_ZONE": (
        0,
        0,
        600,
        1080
    ),

    "DERMA_ZONE": (
        600,
        0,
        1920,
        1080
    )
}


def draw_zones(frame):

    x1, y1, x2, y2 = (
        ZONE_BOUNDARIES[
            "SKINCARE_ZONE"
        ]
    )

    cv2.rectangle(
        frame,
        (x1, y1),
        (x2, y2),
        (0, 255, 255),
        2
    )

    cv2.putText(
        frame,
        "SKINCARE ZONE",
        (20, 50),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 255),
        3
    )

    x1, y1, x2, y2 = (
        ZONE_BOUNDARIES[
            "DERMA_ZONE"
        ]
    )

    cv2.rectangle(
        frame,
        (x1, y1),
        (x2, y2),
        (255, 0, 0),
        2
    )

    cv2.putText(
        frame,
        "DERMA ZONE",
        (620, 50),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (255, 0, 0),
        3
    )

    return frame


def get_zone(
    x,
    y
):

    for zone_name, (
        x1,
        y1,
        x2,
        y2
    ) in ZONE_BOUNDARIES.items():

        if (
            x1 <= x <= x2
            and
            y1 <= y <= y2
        ):

            return zone_name

    return None