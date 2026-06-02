from datetime import datetime

VISITOR_ZONES = {}


class EventGenerator:

    def process(
        self,
        tracker_id,
        zone_name
    ):

        if zone_name is None:
            return None

        key = str(tracker_id)

        if key not in VISITOR_ZONES:

            VISITOR_ZONES[key] = zone_name

            return {
                "visitor_id": key,
                "event_type": "ZONE_VISIT",
                "zone": zone_name,
                "timestamp": datetime.utcnow()
            }

        if VISITOR_ZONES[key] != zone_name:

            VISITOR_ZONES[key] = zone_name

            return {
                "visitor_id": key,
                "event_type": "ZONE_CHANGE",
                "zone": zone_name,
                "timestamp": datetime.utcnow()
            }

        return None