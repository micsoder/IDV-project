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
        self.save_line_graf_data()
        #self.initiate_tourism_per_capita()
        #self.classify_tourism_degree()
        #self.merge_all_tourism_data_with_nuts2_polygons()

    def get_data(self):
        
        self.nuts2_polygons = self.filtered_data.nuts2_polygons
        self.population_data = self.filtered_data.population_data
        self.nights_spent_data = self.filtered_data.nights_spent_data
        self.bed_places_data = self.filtered_data.bed_places_data
        self.GDP_data = self.filtered_data.GDP_data
        self.tourist_industry = self.filtered_data.tourist_industry
        self.unemployment_data = self.filtered_data.unemployment_data


    def initiate_grouping_and_pivoting(self):
        
        self.population_data_pivoted = self.groupby_geo_and_timeperiod(self.population_data, 'population', 'population')
        #self.tourist_industry_pivoted = self.groupby_geo_and_timeperiod(self.tourist_industry, 'number_of_employed', 'tourist_industry')
        #self.bed_places_data_pivoted = self.groupby_geo_and_timeperiod(self.bed_places_data, 'bed_places', 'beds')
        self.nights_spent_data_pivoted = self.groupby_geo_and_timeperiod(self.nights_spent_data, 'nights_spent', 'nights')
        self.GDP_data_pivoted = self.groupby_geo_and_timeperiod(self.GDP_data, 'GDP_per_capita', 'GDP')
        self.unemployment_data_pivoted = self.groupby_geo_and_timeperiod(self.unemployment_data, 'unemployed', 'unemployed')
        

    def groupby_geo_and_timeperiod(self, df, value, col_name):
        df = df[df['TIME_PERIOD'].isin([2017, 2018, 2019, 2020])].reset_index(drop=True)
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
    
    def save_line_graf_data(self):

        self.nights_spent_data_pivoted.to_csv('output/nights_spent_line_graf_data.csv', index=False)
        self.GDP_data_pivoted.to_csv('output/GDP_line_graf_data.csv', index=False )
        self.unemployment_data_pivoted.to_csv('output/Unemployed_line_graf_data.csv', index=False)

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

        quantiles = self.average_tourist_industry_employed['tourist_industry/average_per_capita'].quantile([0, 0.2, 0.4, 0.6, 0.8, 1.0])

        self.average_tourist_industry_employed['Degree_of_tourism'] = pd.cut(self.average_tourist_industry_employed['tourist_industry/average_per_capita'], bins=quantiles, labels=False)
        print(self.average_tourist_industry_employed)
 

    def merge_all_tourism_data_with_nuts2_polygons(self):
        self.tourism_data = pd.merge(self.average_tourist_industry_employed, self.average_beds, on='geo')
        self.tourism_data = pd.merge(self.tourism_data, self.nuts2_polygons, on='geo')
        print(self.tourism_data)

        self.tourism_data_gdf = gpd.GeoDataFrame(self.tourism_data, geometry='geometry')

        self.tourism_data_gdf.to_file('output/tourism_data.shp', driver='ESRI Shapefile')


        
