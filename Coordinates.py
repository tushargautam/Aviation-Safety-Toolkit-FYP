import math

class Coordinates(object):
    def get_next_point(self, speed, angle, currentLat,currentLong):
        miles_in_1_min = speed*1.15078/60
        latitude = currentLat + (miles_in_1_min/3963) * math.cos(math.radians(angle))
        longitude = currentLong + (miles_in_1_min/3963) * (math.sin(math.radians(angle))/math.cos(math.radians(currentLat)))
        return [latitude, longitude]