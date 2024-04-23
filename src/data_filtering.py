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
        self.select_data_from_2020()
        self.merge_2020_values_to_df()
        self.select_data_from_2017_2019()
        self.calculate_mean_for_2017_2019()
        self.merge_2017_2019_mean_values_to_df()


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
        

    def filter_nights_spent(self):
        self.nights_spent_unfiltered_data = self.data.nights_spent_tourist_data
        self.nights_spent_data = self.nights_spent_unfiltered_data[['geo', 'TIME_PERIOD', 'OBS_VALUE']].copy()
        self.nights_spent_data = self.nights_spent_data[self.nights_spent_data['geo'].str[:-2].isin(eu_countries)]
        self.nights_spent_data.rename(columns={'OBS_VALUE': 'nights_spent'}, inplace=True)
        self.nights_spent_data.reset_index(drop=True, inplace=True)


    def filter_bed_places(self):
        self.bed_places_unfiltered_data = self.data.bed_places_tourist_data
        self.bed_places_data = self.bed_places_unfiltered_data[['geo', 'TIME_PERIOD', 'OBS_VALUE']].copy()
        self.bed_places_data = self.bed_places_data[self.bed_places_data['geo'].str[:-2].isin(eu_countries)]
        self.bed_places_data.rename(columns={'OBS_VALUE': 'bed_places'}, inplace=True)
        self.bed_places_data.reset_index(drop=True, inplace=True)      


    def filter_GDP(self):
        self.GDP_unfiltered_data = self.data.GDP_data
        self.GDP_data = self.GDP_unfiltered_data[['geo', 'TIME_PERIOD', 'OBS_VALUE']].copy()
        self.GDP_data = self.GDP_data[self.GDP_data['geo'].str[:-2].isin(eu_countries)]
        self.GDP_data.rename(columns={'OBS_VALUE': 'GDP_per_capita'}, inplace=True)
        self.GDP_data.reset_index(drop=True, inplace=True)

        
    def select_data_from_2020(self):
        
        self.population_data_2020 = self.population_data[self.population_data['TIME_PERIOD'] == 2020].reset_index(drop=True)
        self.nights_spent_data_2020 = self.nights_spent_data[self.nights_spent_data['TIME_PERIOD'] == 2020].reset_index(drop=True)
        self.bed_places_data_2020 = self.bed_places_data[self.bed_places_data['TIME_PERIOD'] == 2020].reset_index(drop=True)
        self.GDP_data_2020 = self.GDP_data[self.GDP_data['TIME_PERIOD'] == 2020].reset_index(drop=True)

        self.population_data_2020 = self.population_data_2020.drop(columns=['TIME_PERIOD'])
        self.nights_spent_data_2020 = self.nights_spent_data_2020.drop(columns=['TIME_PERIOD'])
        self.bed_places_data_2020 = self.bed_places_data_2020.drop(columns=['TIME_PERIOD'])
        self.GDP_data_2020 = self.GDP_data_2020.drop(columns=['TIME_PERIOD'])

        self.population_data_2020 = self.population_data_2020.groupby('geo').sum().reset_index()
        self.nights_spent_data_2020 = self.nights_spent_data_2020.groupby('geo').sum().reset_index()
        self.bed_places_data_2020 = self.bed_places_data_2020.groupby('geo').sum().reset_index()
        self.GDP_data_2020 = self.GDP_data_2020.groupby('geo').sum().reset_index()

    def merge_2020_values_to_df(self):

        self.merged_data_2020 = pd.merge(self.population_data_2020, self.nights_spent_data_2020, on='geo', how='outer')
        self.merged_data_2020 = pd.merge(self.merged_data_2020, self.bed_places_data_2020, on='geo', how='outer')
        self.merged_data_2020 = pd.merge(self.merged_data_2020, self.GDP_data_2020, on='geo', how='outer')
        
        self.merged_data_2020.fillna(0, inplace=True)

        self.merged_data_2020[['population', 'nights_spent', 'bed_places', 'GDP_per_capita']] = self.merged_data_2020[['population', 'nights_spent', 'bed_places', 'GDP_per_capita']].astype(int)
        self.merged_data_2020.rename(columns={'population': 'population_2020', 'nights_spent': 'nights_spent_2020', 
                                                'bed_places': 'bed_places_2020', 'GDP_per_capita': 'GDP_per_capita_2020' }, inplace=True)

        print('merged 2020 data:')
        print(self.merged_data_2020)

    def select_data_from_2017_2019(self):
        
        self.population_data_2017_2019 = self.population_data[self.population_data['TIME_PERIOD'].isin([2017, 2018, 2019])].reset_index(drop=True)
        self.nights_spent_data_2017_2019 = self.nights_spent_data[self.nights_spent_data['TIME_PERIOD'].isin([2017, 2018, 2019])].reset_index(drop=True)
        self.bed_places_data_2017_2019 = self.bed_places_data[self.bed_places_data['TIME_PERIOD'].isin([2017, 2018, 2019])].reset_index(drop=True)
        self.GDP_data_2017_2019 = self.GDP_data[self.GDP_data['TIME_PERIOD'].isin([2017, 2018, 2019])].reset_index(drop=True)

        print('ATTENTION 2017-2019')
        print(self.population_data_2017_2019)
        print(self.nights_spent_data_2017_2019)
        print(self.bed_places_data_2017_2019)
        print(self.GDP_data_2017_2019)

        self.population_avg_percent_diff_2017_2019 = self.avg_percentual_different_between_2017_2019(self.population_data_2017_2019, 'population')
        self.nights_avg_percent_diff_2017_2019 = self.avg_percentual_different_between_2017_2019(self.nights_spent_data_2017_2019, 'nights_spent')
        self.beds_avg_percent_diff_2017_2019 = self.avg_percentual_different_between_2017_2019(self.bed_places_data_2017_2019, 'bed_places')
        self.GDP_avg_percent_diff_2017_2019 = self.avg_percentual_different_between_2017_2019(self.GDP_data_2017_2019, 'GDP_per_capita')
    
        print(self.population_avg_percent_diff_2017_2019)
        print(self.nights_avg_percent_diff_2017_2019)
        print(self.beds_avg_percent_diff_2017_2019)
        print(self.GDP_avg_percent_diff_2017_2019)


    def avg_percentual_different_between_2017_2019(self, df, value):

        df = df.groupby(['geo', 'TIME_PERIOD'])[value].sum().reset_index()
        pivoted = df.pivot(index='geo', columns='TIME_PERIOD', values=value)

        column_name = f'{value}_avg_percent_diff'
        
        pivoted['percent_diff_17_18'] = (pivoted[2018] - pivoted[2017]) / pivoted[2017] * 100
        pivoted['percent_diff_18_19'] = (pivoted[2019] - pivoted[2018]) / pivoted[2018] * 100
        pivoted[column_name] = (pivoted['percent_diff_17_18'] + pivoted['percent_diff_18_19']) / 2

        new_df = pd.DataFrame({'geo': pivoted.index, column_name: pivoted[column_name]})
        new_df.reset_index(drop=True, inplace=True)

        return new_df


    def calculate_mean_for_2017_2019(self):

        self.population_mean = self.population_data_2017_2019.groupby('geo')['population'].sum().reset_index()
        self.population_mean['population'] /= 3
        self.population_mean['population'] = self.population_mean['population'].astype(int)

        self.nights_spent_mean = self.nights_spent_data_2017_2019.groupby('geo')['nights_spent'].sum().reset_index()
        self.nights_spent_mean['nights_spent'] /= 3
        self.nights_spent_mean['nights_spent'] = self.nights_spent_mean['nights_spent'].astype(int)

        self.bed_places_mean = self.bed_places_data_2017_2019.groupby('geo')['bed_places'].sum().reset_index()
        self.bed_places_mean['bed_places'] /= 3
        self.bed_places_mean['bed_places'] = self.bed_places_mean['bed_places'].astype(int)

        self.GDP_per_capita_mean = self.GDP_data_2017_2019.groupby('geo')['GDP_per_capita'].sum().reset_index()
        self.GDP_per_capita_mean['GDP_per_capita'] /= 3
        self.GDP_per_capita_mean['GDP_per_capita'] = self.GDP_per_capita_mean['GDP_per_capita'].astype(int)

    
    def merge_2017_2019_mean_values_to_df(self):

        self.merged_mean_data_2017_2019 = pd.merge(self.population_mean, self.nights_spent_mean, on='geo', how='outer')
        self.merged_mean_data_2017_2019 = pd.merge(self.merged_mean_data_2017_2019, self.bed_places_mean, on='geo', how='outer')
        self.merged_mean_data_2017_2019 = pd.merge(self.merged_mean_data_2017_2019, self.GDP_per_capita_mean, on='geo', how='outer')

        self.merged_mean_data_2017_2019.fillna(0, inplace=True)
        self.merged_mean_data_2017_2019[['population', 'nights_spent', 'bed_places', 'GDP_per_capita']] = self.merged_mean_data_2017_2019[['population', 'nights_spent', 'bed_places', 'GDP_per_capita']].astype(int)

        self.merged_mean_data_2017_2019.rename(columns={'population': 'population_avg_2017_2019', 'nights_spent': 'nights_spent_avg_2017_2019', 
                                                'bed_places': 'bed_places_avg_2017_2019', 'GDP_per_capita': 'GDP_per_capita_avg_2017_2019' }, inplace=True)

        #print('merged mean data 2017-2019')
        #print(self.merged_mean_data_2017_2019)