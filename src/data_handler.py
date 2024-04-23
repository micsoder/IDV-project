from read_in_data import ReadData
from data_filtering import DataFiltering

class DataHandler():

    def __init__(self):

        self.load_in_data()
        self.filter_data()

    def load_in_data(self):

        self.data = ReadData()
        
    
    def filter_data(self):

        DataFiltering(self.data)