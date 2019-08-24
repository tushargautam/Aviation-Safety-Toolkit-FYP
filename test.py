from flask import Flask, render_template
import pandas as pd
import os
from render_flights import Flights
from Flight_Getter import Flight_Getter
from Distance import Distance
from Coordinates import Coordinates

basePath = os.path.dirname(os.path.abspath(__file__))

fg = Flight_Getter()
list = fg.get_icao_list()
df = fg.get_data_frame()
size = fg.get_size()
selected_Icao=None
selected_Icao=list[0]

map = Flights(df,selected_Icao)
map.get_flight_data()
df=pd.DataFrame()
df = map.getDataFrame()
alert_df=map.get_alert_list()
analyzed_df=map.get_analyzed_list()
curr_df=map.get_current()
curr_df=curr_df[curr_df.columns.difference(['arrow'])]
alert_df=alert_df[alert_df.columns.difference(['arrow'])]
analyzed_df=analyzed_df[analyzed_df.columns.difference(['arrow'])]


nTotal = map.getTotalRecs()
nFiltered = map.getFilteredRecs()


di=Distance()
lat=curr_df.loc[0]["Lat"]
long=curr_df.loc[0]["Long"]
spd=curr_df.loc[0]["Spd"]
angle=curr_df.loc[0]["Angle"]
alt=curr_df.loc[0]["Alt"]
for i in range(0,len(alert_df)):
     alat = alert_df.loc[i]["Lat"]
     along = alert_df.loc[i]["Long"]
     aSpeed= alert_df.loc[i]["Spd"]
     aAngle=alert_df.loc[i]["Angle"]
     aAlt=alert_df.loc[i]["Alt"]
     d=di.getDistFeet(lat,long,alat,along)
     counter=0
     prevMainPlane=[lat,long]
     prevAlertPlane=[alat,along]
     newMainPlane=[]
     newAlertPlane=[]
     prevDistance=d
     newDistance=0
     altDiff=di.heightDist(alt, aAlt)
     c=Coordinates()
     diverging_flg = 0
     min_dist_flg = 0
     bad_alt_flg = 0
     msg=''
     if((altDiff)>1000):
          msg="Altitude difference ("+str(altDiff)+"ft) in safe zone, no current possibility of collision."
          bad_alt_flg=1
          continue
     else:
          while(1):
               newMainPlane = c.get_next_point(spd,angle,prevMainPlane[0],prevMainPlane[1])
               newAlertPlane= c.get_next_point(aSpeed,aAngle,prevAlertPlane[0],prevAlertPlane[1])
               newDistance = di.getDistFeet(newMainPlane[0],newMainPlane[1],newAlertPlane[0],newAlertPlane[1])
               print(newDistance)
               counter+=1
               if(newDistance>prevDistance):
                    diverging_flg=1
                    break;
               elif(newDistance<9260):
                    min_dist_flg=1
                    break;
               else:
                    prevMainPlane=newMainPlane
                    prevAlertPlane=newAlertPlane
          if(diverging_flg):
               msg= "Flight path not converging. No possibility of collision."
          elif(min_dist_flg):
               msg="Altitude in bad zone ("+str(altDiff)+"ft), flight path converge in "+str(counter)+"mins."
     alert_df['Warning']=msg



