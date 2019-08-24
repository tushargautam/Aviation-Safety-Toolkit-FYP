
import geopy.distance

class Distance(object):
    def getDistMiles(self ,lat1 ,long1 ,lat2 ,long2):
        coords_1 = (lat1 ,long1)
        coords_2 = (lat2 ,long2)
        dist= geopy.distance.distance(coords_1, coords_2).miles
        return dist
    def getDistKM(self ,lat1 ,long1 ,lat2 ,long2):
        coords_1 = (lat1 ,long1)
        coords_2 = (lat2 ,long2)
        dist= geopy.distance.distance(coords_1, coords_2).kilometers
        return dist
    def getDistM(self ,lat1 ,long1 ,lat2 ,long2):
        coords_1 = (lat1 ,long1)
        coords_2 = (lat2 ,long2)
        dist= geopy.distance.distance(coords_1, coords_2).m
        return dist
    def getDistFeet(self ,lat1 ,long1 ,lat2 ,long2):
        coords_1 = (lat1 ,long1)
        coords_2 = (lat2 ,long2)
        dist= geopy.distance.distance(coords_1, coords_2).feet
        return dist
    def heightDist(self,alt1,alt2):
        return abs(alt1-alt2)