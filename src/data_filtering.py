import pandas as pd
import geopandas as gpd
from eu_countries import eu_countries


class DataFiltering():

    def __init__(self, data):
        self.data = data

        self.filter_nuts_polygons()
        self.filter_population()
        self.filter_nights_spent()
        self.filter_bed_places()
        self.filter_GDP()
        self.filter_tourist_industry()

    def filter_nuts_polygons(self):
        self.nuts_polygons_unfiltered = self.data.nuts_polygons
        self.nuts2_polygons = self.nuts_polygons_unfiltered[self.nuts_polygons_unfiltered['LEVL_CODE'] == 2]
        self.nuts2_polygons = self.nuts2_polygons.sort_values(by='NUTS_ID', ascending=True)
        self.nuts2_polygons.reset_index(drop=True, inplace=True)


    def filter_population(self):
        self.population_unfiltered_data = self.data.population_data
        self.population_data = self.population_unfiltered_data[['geo', 'TIME_PERIOD', 'OBS_VALUE']].copy()
        self.population_data = self.population_data[self.population_data['geo'].str[:-2].isin(eu_countries)]
        self.population_data.rename(columns={'OBS_VALUE': 'population'}, inplace=True)
        self.population_data.reset_index(drop=True, inplace=True)
        self.population_data.to_csv('output/population_data.csv')
        

    def filter_nights_spent(self):
        self.nights_spent_unfiltered_data = self.data.nights_spent_tourist_data
        self.nights_spent_data = self.nights_spent_unfiltered_data[['geo', 'TIME_PERIOD', 'OBS_VALUE']].copy()
        self.nights_spent_data = self.nights_spent_data[self.nights_spent_data['geo'].str[:-2].isin(eu_countries)]
        self.nights_spent_data.rename(columns={'OBS_VALUE': 'nights_spent'}, inplace=True)
        self.nights_spent_data.reset_index(drop=True, inplace=True)
        self.nights_spent_data.to_csv('output/nights_spent_data.csv')

    def filter_bed_places(self):
        self.bed_places_unfiltered_data = self.data.bed_places_tourist_data
        self.bed_places_data = self.bed_places_unfiltered_data[['geo', 'TIME_PERIOD', 'OBS_VALUE']].copy()
        self.bed_places_data = self.bed_places_data[self.bed_places_data['geo'].str[:-2].isin(eu_countries)]
        self.bed_places_data.rename(columns={'OBS_VALUE': 'bed_places'}, inplace=True)
        self.bed_places_data.reset_index(drop=True, inplace=True)      
        self.bed_places_data.to_csv('output/bed_places_data.csv')

    def filter_GDP(self):
        self.GDP_unfiltered_data = self.data.GDP_data
        self.GDP_data = self.GDP_unfiltered_data[['geo', 'TIME_PERIOD', 'OBS_VALUE']].copy()
        self.GDP_data = self.GDP_data[self.GDP_data['geo'].str[:-2].isin(eu_countries)]
        self.GDP_data.rename(columns={'OBS_VALUE': 'GDP_per_capita'}, inplace=True)
        self.GDP_data.reset_index(drop=True, inplace=True)
        self.GDP_data.to_csv('output/GDP_data.csv')

    def filter_tourist_industry(self):

        self.tourist_industry_unfiltered_data = self.data.tourist_industry
        self.tourist_industry = self.tourist_industry_unfiltered_data[['geo', 'TIME_PERIOD', 'OBS_VALUE', 'nace_r2']].copy()
        self.tourist_industry = self.tourist_industry[self.tourist_industry['geo'].str[:-2].isin(eu_countries)]
        self.tourist_industry.rename(columns={'OBS_VALUE': 'number_of_employed'}, inplace=True)
        self.tourist_industry.reset_index(drop=True, inplace=True)
        self.tourist_industry.to_csv('output/tourist_industry.csv')
