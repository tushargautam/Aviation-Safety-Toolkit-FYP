from flask import Flask, render_template, request
import pandas as pd
import os
from render_flights import Flights
from Flight_Getter import Flight_Getter
from Distance import Distance
from Coordinates import Coordinates


app = Flask(__name__)
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


map.plot_flights()
nTotal = map.getTotalRecs()
nFiltered = map.getFilteredRecs()

print(len(analyzed_df))
print(len(curr_df))
print(len(alert_df))


@app.route('/')
def index():
   return render_template('dashboard.html')

@app.route('/aircraft_details')
def aircraft_details():
   return render_template('aircraft_details.html')


@app.route('/dashboard')
def dashboard():
    global size
    global list
    global selected_Icao
    return render_template('dashboard.html', size=size,list=list, selected_Icao=selected_Icao)




# @app.route('/map')
# def map():
#     global selected_Icao
#     return render_template('map.html',list=list,selected_Icao=selected_Icao)
#


@app.route('/map')
def map():
    global selected_Icao
    return render_template('map.html',selected_Icao=selected_Icao)


@app.route('/tables')
def table():
    global df
    global selected_Icao
    return render_template('tables.html',selected_Icao=selected_Icao,curr_df=[curr_df.to_html(classes='data table table-hover table-condensed thead-dark table-striped')],alert_df=[alert_df.to_html(classes='data table table-hover table-condensed thead-dark table-striped')],analyzed_df=[analyzed_df.to_html(classes='data table table-hover table-condensed thead-dark table-striped')])





@app.route('/notifications')
def notifications():
    di = Distance()
    lat = curr_df.loc[0]["Lat"]
    long = curr_df.loc[0]["Long"]
    spd = curr_df.loc[0]["Spd"]
    angle = curr_df.loc[0]["Angle"]
    alt = curr_df.loc[0]["Alt"]
    for i in range(0, len(alert_df)):
        alat = alert_df.loc[i]["Lat"]
        along = alert_df.loc[i]["Long"]
        aSpeed = alert_df.loc[i]["Spd"]
        aAngle = alert_df.loc[i]["Angle"]
        aAlt = alert_df.loc[i]["Alt"]
        d = di.getDistFeet(lat, long, alat, along)
        counter = 0
        prevMainPlane = [lat, long]
        prevAlertPlane = [alat, along]
        newMainPlane = []
        newAlertPlane = []
        prevDistance = d
        newDistance = 0
        altDiff = di.heightDist(alt, aAlt)
        c = Coordinates()
        diverging_flg = 0
        min_dist_flg = 0
        bad_alt_flg = 0
        msg = ''
        if (altDiff > 1000):
            msg = "Altitude difference (" + str(altDiff) + "ft) in safe zone, no current possibility of collision."
            bad_alt_flg = 1

        else:
            while (1):
                newMainPlane = c.get_next_point(spd, angle, prevMainPlane[0], prevMainPlane[1])
                newAlertPlane = c.get_next_point(aSpeed, aAngle, prevAlertPlane[0], prevAlertPlane[1])
                newDistance = di.getDistFeet(newMainPlane[0], newMainPlane[1], newAlertPlane[0], newAlertPlane[1])
                print(newDistance)
                counter += 1
                if (newDistance > prevDistance):
                    diverging_flg = 1
                    break;
                elif (newDistance < 9260):
                    min_dist_flg = 1
                    break;
                else:
                    prevMainPlane = newMainPlane
                    prevAlertPlane = newAlertPlane

            if (diverging_flg):
                msg = "Flight path not intersecting. No possibility of collision."
            elif (min_dist_flg):
                msg = "Altitude in bad zone (" + str(altDiff) + "ft),  flight paths intersect in " + str(counter) + "mins."
            elif(bad_alt_flg):
                msg="Altitude difference (" + str(altDiff) + "ft) in safe zone, no current possibility of collision."
        alert_df['Warning'] = msg
    current=curr_df.to_dict(orient='records')
    alerts=alert_df.to_dict(orient='records')
    global selected_Icao
    return render_template('notifications.html',current=current,alerts=alerts,selected_Icao=selected_Icao)



if __name__ == "__main__":
    app.run(debug=True)
