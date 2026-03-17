from enum import Enum


class MissionType(str, Enum):
    DELIVERY = "delivery"
    RESCUE = "rescue"
    REPAIR = "repair"
