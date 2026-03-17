from enum import Enum


class Role(str, Enum):
    DRIVER = "driver"
    MECHANIC = "mechanic"
    STRATEGIST = "strategist"
