from read_in_data import ReadData
from data_filtering import DataFiltering

class DataHandler():

    def __init__(self):

        self.load_in_data()
        self.filter_data()

    def load_in_data(self):

        self.data = ReadData()
        #self.nuts_polygons = data.nuts_polygons
        #self.population_data = data.population_data
        #self.nights_spent_tourist_data = data.nights_spent_tourist_data
        #self.bed_places_tourist_data = data.bed_places_tourist_data
        #self.GDP_data = data.GDP_data
    
    def filter_data(self):

        DataFiltering(self.data)