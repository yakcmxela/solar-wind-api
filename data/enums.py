import enum

class IncentiveType(enum.Enum):
    solar = "solar"
    wind = "wind"
    geothermal = "geothermal"
    ev = "electric vehicle"
    home = "home energy efficiency"
    other = "other"