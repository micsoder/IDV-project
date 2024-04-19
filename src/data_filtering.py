import pandas as pd
import geopandas as gpd


class DataFiltering():

    def __init__(self, data):
        self.data = data

        self.filter_nuts_polygons()
        self.filter_population()
        self.filter_nights_spent()
        self.filter_bed_places()
        self.filter_GDP()
        self.select_data_from_2020()
        self.select_data_from_2017_2019()
        self.calculate_mean_for_2017_2019()


    def filter_nuts_polygons(self):
        self.nuts_polygons_unfiltered = self.data.nuts_polygons
        self.nuts2_polygons = self.nuts_polygons_unfiltered[self.nuts_polygons_unfiltered['LEVL_CODE'] == 2]
        self.nuts2_polygons = self.nuts2_polygons.sort_values(by='NUTS_ID', ascending=True)
        self.nuts2_polygons.reset_index(drop=True, inplace=True)
        print('Polygons:')
        print(self.nuts2_polygons)


    def filter_population(self):
        self.population_unfiltered_data = self.data.population_data
        self.population_data = self.population_unfiltered_data[['geo', 'TIME_PERIOD', 'OBS_VALUE']].copy()
        self.population_data.rename(columns={'OBS_VALUE': 'population'}, inplace=True)
        print('Population:')
        print(self.population_data)
        

    def filter_nights_spent(self):
        self.nights_spent_unfiltered_data = self.data.nights_spent_tourist_data
        self.nights_spent_data = self.nights_spent_unfiltered_data[['geo', 'TIME_PERIOD', 'OBS_VALUE', 'c_resid']].copy()
        self.nights_spent_data.rename(columns={'OBS_VALUE': 'nights_spent'}, inplace=True)
        print('Nights spent:')
        print(self.nights_spent_data)


    def filter_bed_places(self):
        self.bed_places_unfiltered_data = self.data.bed_places_tourist_data
        self.bed_places_data = self.bed_places_unfiltered_data[['geo', 'TIME_PERIOD', 'OBS_VALUE', 'accomunit']].copy()
        self.bed_places_data.rename(columns={'OBS_VALUE': 'bed_places'}, inplace=True)
        print('Bed places:')
        print(self.bed_places_data)        


    def filter_GDP(self):
        self.GDP_unfiltered_data = self.data.GDP_data
        self.GDP_data = self.GDP_unfiltered_data[['geo', 'TIME_PERIOD', 'OBS_VALUE']].copy()
        self.GDP_data.rename(columns={'OBS_VALUE': 'GDP_per_capita'}, inplace=True)
        print('GDP:')
        print(self.GDP_data)
        
    def select_data_from_2020(self):
        
        self.population_data_2020 = self.population_data[self.population_data['TIME_PERIOD'] == 2020]
        self.nights_spent_data_2020 = self.nights_spent_data[self.nights_spent_data['TIME_PERIOD'] == 2020]
        self.bed_places_data_2020 = self.bed_places_data[self.bed_places_data['TIME_PERIOD'] == 2020]
        self.GDP_data_2020 = self.GDP_data[self.GDP_data['TIME_PERIOD'] == 2020]


    def select_data_from_2017_2019(self):
        
        self.population_data_2017_2019 = self.population_data[self.population_data['TIME_PERIOD'].isin([2017, 2018, 2019])]
        self.nights_spent_data_2017_2019 = self.nights_spent_data[self.nights_spent_data['TIME_PERIOD'].isin([2017, 2018, 2019])]
        self.bed_places_data_2017_2019 = self.bed_places_data[self.bed_places_data['TIME_PERIOD'].isin([2017, 2018, 2019])]
        self.GDP_data_2017_2019 = self.GDP_data[self.GDP_data['TIME_PERIOD'].isin([2017, 2018, 2019])]

        print(self.population_data_2017_2019)
    def calculate_mean_for_2017_2019(self):

        self.population_mean = self.population_data_2017_2019.groupby('geo')['population'].mean()
        self.nights_spent_mean = self.nights_spent_data_2017_2019.groupby('geo')['nights_spent'].mean()
        self.bed_places_mean = self.bed_places_data_2017_2019.groupby('geo')['bed_places'].mean()
        self.GDP_per_capita_mean = self.GDP_data_2017_2019.groupby('geo')['GDP_per_capita'].mean()

        print(self.population_mean)
        print(self.nights_spent_mean)
        print(self.bed_places_mean)
        print(self.GDP_per_capita_mean)