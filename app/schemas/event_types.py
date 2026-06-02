from enum import Enum


class EventType(str, Enum):

    ENTRY = "ENTRY"

    EXIT = "EXIT"

    ZONE_ENTER = "ZONE_ENTER"

    ZONE_EXIT = "ZONE_EXIT"

    QUEUE_JOIN = "QUEUE_JOIN"

    QUEUE_ABANDON = "QUEUE_ABANDON"

    PURCHASE = "PURCHASE"

    REENTRY = "REENTRY"

    STAFF_DETECTED = "STAFF_DETECTED"