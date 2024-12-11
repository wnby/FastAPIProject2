# backend/enums.py
from enum import Enum

class ModeEnum(str, Enum):
    COOLING = "Cooling"
    HEATING = "Heating"

class WindSpeedEnum(str, Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
