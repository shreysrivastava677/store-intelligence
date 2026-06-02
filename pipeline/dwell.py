from datetime import datetime


class DwellTracker:

    def __init__(self):

        self.entry_times = {}

    def get_dwell_time(
        self,
        visitor_id
    ):

        visitor_id = str(
            visitor_id
        )

        if visitor_id not in self.entry_times:

            self.entry_times[
                visitor_id
            ] = datetime.utcnow()

        dwell = (
            datetime.utcnow()
            - self.entry_times[
                visitor_id
            ]
        )

        return int(
            dwell.total_seconds()
        )