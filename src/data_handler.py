from read_in_data import ReadData
from data_filtering import DataFiltering
from data_processing import DataProcessing

class DataHandler():

    def __init__(self):

        self.load_in_data()
        self.filter_data()
        self.process_data()

    def load_in_data(self):

        self.data = ReadData()

    
    def filter_data(self):

        self.filtered_data = DataFiltering(self.data)
    
    def process_data(self):

        DataProcessing(self.filtered_data)