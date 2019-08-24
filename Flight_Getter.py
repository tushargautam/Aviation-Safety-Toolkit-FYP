import pandas as pd
import os

class Flight_Getter(object):
    basePath = os.path.dirname(os.path.abspath(__file__))
    data = pd.read_json(basePath + '/data_file.json', orient='columns')
    icao = []
    size=0
    def __init__(self):
        for i in range(0, len(self.data["Lat"])):
            self.icao.append(self.data.loc[i, "Icao"])
            self.size= len(self.data["Lat"])
    def get_icao_list(self):
        return self.icao
    def get_data_frame(self):
        return self.data
    def get_size(self):
        return self.size