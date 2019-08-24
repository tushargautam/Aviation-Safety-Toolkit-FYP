import pandas as pd
import geopy.distance
import folium
import math


class Flights(object):
    flight_list=[]
    data=None
    df=None
    point=None
    points2=None
    meanLat=None
    meanLongi=None
    selected_icao=None
    alerts=None
    analyzed=None
    current=None
    def __init__(self, data,selected_icao):
        self.flight_list=[]
        self.data=data
        latit = []
        longitude = []
        # df=pd.DataFrame(columns=['icao', 'lat', 'long','alt', 'spd', 'angle','verticalSpd','color'])
        for i in range(0, len(self.data["Lat"])):
            latit.append(self.data.loc[i, "Lat"])
            longitude.append(self.data.loc[i, "Long"])
        self.selected_icao=selected_icao
        self.setMeanCoords(selected_icao)


    def getTotalRecs(self):
        return len(self.data)

    def getFilteredRecs(self):
        return len(self.df)

    def setMeanCoords(self,icao):
        for i in range(0, len(self.data["Lat"])):
            if (self.data.loc[i, "Icao"] == self.selected_icao):
                self.meanLat=self.data.loc[i, "Lat"]
                self.meanLongi=self.data.loc[i, "Long"]

    def getDataFrame(self):
        return self.df

    def get_flight_data(self):
        _list = []
        alert_list=[]
        analyzed=[]
        current = []
        for i in range(0, len(self.data["Lat"])):
            icao = self.data.loc[i, "Icao"]
            lat = self.data.loc[i, "Lat"]
            longit = self.data.loc[i, "Long"]
            alt = self.data.loc[i, "Alt"]
            spd = self.data.loc[i, "Spd"]
            # posTime=[]
            # for i in range(0,len(data["Lat"])):
            #         posTime.append(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(data.loc[i,"PosTime"])))
            angle = self.data.loc[i, "Trak"]
            verticalSpd = self.data.loc[i, "Vsi"]
            reg=self.data.loc[i, "Reg"]
            flg=0
            include_flg=1

            if (self.data.loc[i, "Icao"]==self.selected_icao):
                color = "black"
            else:
                color = self.getColor(lat, longit,self.meanLat,self.meanLongi)


            if(not(math.isnan(spd)) and not(math.isnan(angle))):
                nextCoord= self.get_next_point(spd, angle, lat, longit)

            else:
                nextCoord = [0, 0]

            arrow=[]
            arrow.append([lat,longit])
            arrow.append(nextCoord)
            row = {
                "Icao": icao,
                "Lat": lat,
                "Long": longit,
                "Alt": alt,
                "Spd": spd,
                "Angle": angle,
                "Vertical_Speed": verticalSpd,
                "Color": color,
                "Reg": reg,
                "arrow":arrow
            }


            self.flight_list.append(icao)
            _list.append(row)
            if (self.data.loc[i, "Icao"]==self.selected_icao):
                current.append(row)
            else:
                if (row["Color"]=="red"):
                    alert_list.append(row)
                else:
                    analyzed.append(row)

        self.df = pd.DataFrame(_list)
        self.alerts=pd.DataFrame(alert_list)
        self.analyzed=pd.DataFrame(analyzed)
        self.current=pd.DataFrame(current)
        self.points = []
        self.points2 = []

        for i in range(0, len(self.data["Lat"])):
            self.points2.append([self.df.loc[i, "Lat"], self.df.loc[i, "Long"]])
            self.points.append(tuple([self.df.loc[i, "Lat"], self.df.loc[i, "Long"]]))
        return self.flight_list
    def get_alert_list(self):
        return self.alerts

    def get_analyzed_list(self):
        return self.analyzed
    def get_current(self):
        return self.current

    def getColor(self,lat1,long1,lat2,long2):
        coords_1 = (lat1,long1)
        coords_2 = (lat2,long2)
        dist= geopy.distance.distance(coords_1, coords_2).miles
        if dist<20*1.1508:
            return 'red'
        else:
            return 'green'



    def get_next_point(self, speed, angle, currentLat,currentLong):
        miles_in_1_min = speed*1.15078
        latitude = currentLat + (miles_in_1_min/3963) * math.cos(math.radians(angle))
        longitude = currentLong + (miles_in_1_min/3963) * (math.sin(math.radians(angle))/math.cos(math.radians(currentLat)))
        return [latitude, longitude]

    def plot_flights(self):

        mapit = folium.Map(location=[self.meanLat, self.meanLongi], zoom_start=11, tiles='Stamen Terrain', prefer_canvas=True)
        i = 0
        folium.Circle(location=[self.meanLat, self.meanLongi], radius=25000,  fill_color='#D1FF33',
                      fill_opacity=0.2).add_to(mapit)
        folium.Circle(location=[self.meanLat, self.meanLongi], radius=18000,  fill_color='#FFC300  ',
                      fill_opacity=0.5).add_to(mapit)
        folium.Circle(location=[self.meanLat, self.meanLongi], radius=10000, fill_color='#FA8072',
                      fill_opacity=0.6).add_to(mapit)

        for position in self.points2:
            icon=folium.Icon(color=self.df.loc[i, "Color"], icon='plane',angle=self.df.loc[i, "Angle"], prefix='fa')
            folium.Marker(location=[position[0], position[1]], popup=str(self.df.loc[i, "Icao"]),
                          tooltip=str("Alt:"+str(self.df.loc[i, "Alt"])), icon=icon).add_to(mapit)
            print(self.df.loc[i, "arrow"])
            print(self.df.loc[i, "Angle"],self.df.loc[i, "Spd"])
            folium.PolyLine(self.df.loc[i, "arrow"], color='gray', weight=2, opacity=1).add_to(mapit)
            folium.RegularPolygonMarker(location=(self.df.loc[i, "arrow"][1][0], self.df.loc[i, "arrow"][1][1]), fill_color='blue', number_of_sides=3,
                                        radius=2, rotation=math.radians(self.df.loc[i, "Angle"])).add_to(mapit)
            i = i + 1
        mapit.save('templates/map2.html')

