import pandas as pd
from mapclassify import NaturalBreaks
import geopandas as gpd
import numpy as np
from eu_countries import eu_country_names


class DataManagement():

    def __init__(self, filtered_data):
        print('Data management...')

        self.filtered_data = filtered_data

        self.get_data()
        self.initiate_grouping_and_pivoting()
        self.NUTS2_name_df()
        self.initiate_tourism_per_capita()
        self.classify_tourism_degree()
        self.merge_all_tourism_data_with_nuts2_polygons()

    def get_data(self):
        
        self.nuts2_polygons = self.filtered_data.nuts2_polygons
        self.population_data = self.filtered_data.population_data
        self.nights_spent_data = self.filtered_data.nights_spent_data
        self.bed_places_data = self.filtered_data.bed_places_data
        self.GDP_data = self.filtered_data.GDP_data
        self.tourist_industry = self.filtered_data.tourist_industry


    def initiate_grouping_and_pivoting(self):

        self.tourist_industry_pivoted = self.groupby_geo_and_timeperiod(self.tourist_industry, 'number_of_employed', 'tourist_industry')
        self.population_data_pivoted = self.groupby_geo_and_timeperiod(self.population_data, 'population', 'population')
        self.bed_places_data_pivoted = self.groupby_geo_and_timeperiod(self.bed_places_data, 'bed_places', 'beds')
        

    def groupby_geo_and_timeperiod(self, df, value, col_name):
        df = df[df['TIME_PERIOD'].isin([2017, 2018, 2019])].reset_index(drop=True)
        df = df.groupby(['geo', 'TIME_PERIOD'])[value].sum().reset_index()

        pivoted = df.pivot(index='geo', columns='TIME_PERIOD', values=value)
        new_column_names = {2017: f'2017_{col_name}',
                            2018: f'2018_{col_name}',
                            2019: f'2019_{col_name}',
                            2020: f'2020_{col_name}'}

        pivoted.rename(columns=new_column_names, inplace=True)
        pivoted.fillna(0, inplace=True)
        pivoted.reset_index(drop=False, inplace=True)
        print(pivoted)

        return pivoted

    def NUTS2_name_df(self):

        self.geo_name = self.population_data_pivoted.copy()
        self.geo_name = self.geo_name[['geo']]
    
    def initiate_tourism_per_capita(self):

        self.average_tourist_industry_employed = self.tourism_per_capita(self.tourist_industry_pivoted, 'tourist_industry')
        self.average_beds = self.tourism_per_capita(self.bed_places_data_pivoted, 'beds')


    def tourism_per_capita(self, df, value):

        self.tourism_df = self.geo_name.copy()
        for year in range(2017, 2020):
            if value == 'beds':
                self.tourism_df[f'{year}_{value}/per_capita'] = round(df[f'{year}_{value}'] / self.population_data_pivoted[f'{year}_population'], 2)
            else:
                self.tourism_df[f'{year}_{value}/per_capita'] = round(df[f'{year}_{value}'] / self.population_data_pivoted[f'{year}_population'] * 100, 2)
        
        self.tourism_df[f'{value}/average_per_capita'] = round(self.tourism_df[[f'{year}_{value}/per_capita' for year in range(2017, 2020)]].mean(axis=1), 2)
        self.tourism_df = self.tourism_df[['geo', f'{value}/average_per_capita']]

        return self.tourism_df
    
    def classify_tourism_degree(self):

        self.average_tourist_industry_employed.replace([np.inf, -np.inf], np.nan, inplace=True)
        self.average_tourist_industry_employed.dropna(inplace=True)

        print(self.average_tourist_industry_employed)

        values = self.average_tourist_industry_employed['tourist_industry/average_per_capita']
        classifier = NaturalBreaks(values, k=3)
        self.average_tourist_industry_employed['Degree_of_tourism'] = classifier.yb
        print(self.average_tourist_industry_employed)

        thresholds = classifier.bins
        print("Thresholds for each category:")
        for i, threshold in enumerate(thresholds):
            print(f"Category {i}: {threshold:.2f}")

    def merge_all_tourism_data_with_nuts2_polygons(self):
        self.tourism_data = pd.merge(self.average_tourist_industry_employed, self.average_beds, on='geo')
        self.tourism_data = pd.merge(self.tourism_data, self.nuts2_polygons, on='geo')
        print(self.tourism_data)

        self.tourism_data_gdf = gpd.GeoDataFrame(self.tourism_data, geometry='geometry')

        self.tourism_data_gdf.to_file('output/tourism_data.shp', driver='ESRI Shapefile')


        
