import pandas as pd
from mapclassify import NaturalBreaks
import geopandas as gpd


class DataProcessing():

    def __init__(self, filtered_data):

        self.filtered_data = filtered_data

        self.get_data()
        self.select_data_from_2020()
        self.merge_2020_values_to_df()
        self.select_data_from_2017_2019()
        self.merge_2017_2019_mean_percent_values_to_df()
        self.calculate_mean_for_2017_2019()
        self.merge_2017_2019_mean_values_to_df()
        self.percentual_difference_between_2020_and_mean_value_of_2017_2019()
        #self.categorize_percentual_diff_from_2017_2019_to_2020()
        #self.mean_number_of_employed_in_tourist_industry_2017_2019()

    def get_data(self):
        
        self.nuts2_polygons = self.filtered_data.nuts2_polygons
        self.population_data = self.filtered_data.population_data
        self.nights_spent_data = self.filtered_data.nights_spent_data
        self.bed_places_data = self.filtered_data.bed_places_data
        self.GDP_data = self.filtered_data.GDP_data
        self.tourist_industry = self.filtered_data.tourist_industry
        self.unemployment_data = self.filtered_data.unemployment_data
    

    def select_data_from_2020(self):
        
        self.population_data_2020 = self.population_data[self.population_data['TIME_PERIOD'] == 2020].reset_index(drop=True)
        self.nights_spent_data_2020 = self.nights_spent_data[self.nights_spent_data['TIME_PERIOD'] == 2020].reset_index(drop=True)
        self.bed_places_data_2020 = self.bed_places_data[self.bed_places_data['TIME_PERIOD'] == 2020].reset_index(drop=True)
        self.GDP_data_2020 = self.GDP_data[self.GDP_data['TIME_PERIOD'] == 2020].reset_index(drop=True)
        self.unemployment_data_2020 = self.unemployment_data[self.unemployment_data['TIME_PERIOD'] == 2020].reset_index(drop=True)

        self.population_data_2020 = self.population_data_2020.drop(columns=['TIME_PERIOD'])
        self.nights_spent_data_2020 = self.nights_spent_data_2020.drop(columns=['TIME_PERIOD'])
        self.bed_places_data_2020 = self.bed_places_data_2020.drop(columns=['TIME_PERIOD'])
        self.GDP_data_2020 = self.GDP_data_2020.drop(columns=['TIME_PERIOD'])
        self.unemployment_data_2020 = self.unemployment_data_2020.drop(columns=['TIME_PERIOD'])

        self.population_data_2020 = self.population_data_2020.groupby('geo').sum().reset_index()
        self.nights_spent_data_2020 = self.nights_spent_data_2020.groupby('geo').sum().reset_index()
        self.bed_places_data_2020 = self.bed_places_data_2020.groupby('geo').sum().reset_index()
        self.GDP_data_2020 = self.GDP_data_2020.groupby('geo').sum().reset_index()
        self.unemployment_data_2020 = self.unemployment_data_2020.groupby('geo').sum().reset_index()

    def merge_2020_values_to_df(self):

        self.merged_data_2020 = pd.merge(self.population_data_2020, self.nights_spent_data_2020, on='geo', how='outer')
        self.merged_data_2020 = pd.merge(self.merged_data_2020, self.bed_places_data_2020, on='geo', how='outer')
        self.merged_data_2020 = pd.merge(self.merged_data_2020, self.GDP_data_2020, on='geo', how='outer')
        self.merged_data_2020 = pd.merge(self.merged_data_2020, self.unemployment_data_2020, on='geo', how='outer')
        
        self.merged_data_2020.fillna(0, inplace=True)

        self.merged_data_2020[['population', 'nights_spent', 'bed_places', 'GDP_per_capita']] = self.merged_data_2020[['population', 'nights_spent', 'bed_places', 'GDP_per_capita']].astype(int)
        self.merged_data_2020.rename(columns={'population': 'population_2020', 'nights_spent': 'nights_spent_2020', 
                                                'bed_places': 'bed_places_2020', 'GDP_per_capita': 'GDP_per_capita_2020', 'unemployed': 'unemployed_2020' }, inplace=True)

        print('ATTENTION1 ')
        print(self.merged_data_2020)

    def select_data_from_2017_2019(self):
        
        self.population_data_2017_2019 = self.population_data[self.population_data['TIME_PERIOD'].isin([2017, 2018, 2019])].reset_index(drop=True)
        self.nights_spent_data_2017_2019 = self.nights_spent_data[self.nights_spent_data['TIME_PERIOD'].isin([2017, 2018, 2019])].reset_index(drop=True)
        self.bed_places_data_2017_2019 = self.bed_places_data[self.bed_places_data['TIME_PERIOD'].isin([2017, 2018, 2019])].reset_index(drop=True)
        self.GDP_data_2017_2019 = self.GDP_data[self.GDP_data['TIME_PERIOD'].isin([2017, 2018, 2019])].reset_index(drop=True)
        self.unemployment_data_2017_2019 = self.unemployment_data[self.unemployment_data['TIME_PERIOD'].isin([2017, 2018, 2019])].reset_index(drop=True)

        self.population_avg_percent_diff_2017_2019 = self.avg_percentual_different_between_2017_2019(self.population_data_2017_2019, 'population')
        self.nights_avg_percent_diff_2017_2019 = self.avg_percentual_different_between_2017_2019(self.nights_spent_data_2017_2019, 'nights_spent')
        self.beds_avg_percent_diff_2017_2019 = self.avg_percentual_different_between_2017_2019(self.bed_places_data_2017_2019, 'bed_places')
        self.GDP_avg_percent_diff_2017_2019 = self.avg_percentual_different_between_2017_2019(self.GDP_data_2017_2019, 'GDP_per_capita')
        self.unemployment_avg_percent_diff_2017_2019 = self.avg_percentual_different_between_2017_2019(self.unemployment_data_2017_2019, 'unemployed')


    def avg_percentual_different_between_2017_2019(self, df, value):

        df = df.groupby(['geo', 'TIME_PERIOD'])[value].sum().reset_index()
        pivoted = df.pivot(index='geo', columns='TIME_PERIOD', values=value)
        print('double attention')
        print(pivoted)


        column_name = f'{value}_avg_%_diff_2017_2019'
        
        pivoted['percent_diff_17_18'] = (pivoted[2018] - pivoted[2017]) / pivoted[2017] * 100
        pivoted['percent_diff_18_19'] = (pivoted[2019] - pivoted[2018]) / pivoted[2018] * 100
        pivoted[column_name] = round((pivoted['percent_diff_17_18'] + pivoted['percent_diff_18_19']) / 2, 2)

        new_df = pd.DataFrame({'geo': pivoted.index, column_name: pivoted[column_name]})
        new_df.reset_index(drop=True, inplace=True)

        return new_df

    def merge_2017_2019_mean_percent_values_to_df(self):

        self.merged_mean_percent_2017_2019 = pd.merge(self.population_avg_percent_diff_2017_2019, self.nights_avg_percent_diff_2017_2019, on='geo', how='outer')
        self.merged_mean_percent_2017_2019 = pd.merge(self.merged_mean_percent_2017_2019, self.beds_avg_percent_diff_2017_2019, on='geo', how='outer')
        self.merged_mean_percent_2017_2019 = pd.merge(self.merged_mean_percent_2017_2019, self.GDP_avg_percent_diff_2017_2019, on='geo', how='outer')
        self.merged_mean_percent_2017_2019 = pd.merge(self.merged_mean_percent_2017_2019, self.unemployment_avg_percent_diff_2017_2019, on='geo', how='outer')        

        self.merged_mean_percent_2017_2019.fillna(0, inplace=True)
        self.merged_mean_percent_2017_2019.drop(columns=['population_avg_%_diff_2017_2019', 'bed_places_avg_%_diff_2017_2019'], inplace=True)

        print('ATTENTION, mean percent merged:')
        print(self.merged_mean_percent_2017_2019.head())


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

        self.unemployment_mean = self.unemployment_data_2017_2019.groupby('geo')['unemployed'].sum().reset_index()
        self.unemployment_mean['unemployed'] /= 3
        self.unemployment_mean['unemployed'] = self.unemployment_mean['unemployed'].astype(int)
        print('ATTENTION MEAN UN')
        print(self.unemployment_mean)
    
    def merge_2017_2019_mean_values_to_df(self):

        self.merged_mean_data_2017_2019 = pd.merge(self.population_mean, self.nights_spent_mean, on='geo', how='outer')
        self.merged_mean_data_2017_2019 = pd.merge(self.merged_mean_data_2017_2019, self.bed_places_mean, on='geo', how='outer')
        self.merged_mean_data_2017_2019 = pd.merge(self.merged_mean_data_2017_2019, self.GDP_per_capita_mean, on='geo', how='outer')
        self.merged_mean_data_2017_2019 = pd.merge(self.merged_mean_data_2017_2019, self.unemployment_mean, on='geo', how='outer')

        self.merged_mean_data_2017_2019.fillna(0, inplace=True)
        self.merged_mean_data_2017_2019[['population', 'nights_spent', 'bed_places', 'GDP_per_capita']] = self.merged_mean_data_2017_2019[['population', 'nights_spent', 'bed_places', 'GDP_per_capita']].astype(int)

        self.merged_mean_data_2017_2019.rename(columns={'population': 'population_avg_2017_2019', 'nights_spent': 'nights_spent_avg_2017_2019', 
                                                'bed_places': 'bed_places_avg_2017_2019', 'GDP_per_capita': 'GDP_per_capita_avg_2017_2019', 'unemployed': 'unemployed_avg_2017_2019' }, inplace=True)

        print('ATTENTION 4')
        print(self.merged_mean_data_2017_2019)
    
    def percentual_difference_between_2020_and_mean_value_of_2017_2019(self):

        merged_df = pd.merge(self.merged_data_2020, self.merged_mean_data_2017_2019, on='geo')

        for column1, column2 in zip(self.merged_data_2020.columns[1:], self.merged_mean_data_2017_2019.columns[1:]):
            new_column_name = column1[:-5] + '_%_diff_from_avg_2017_2019_to_2020'
            if column1 == 'unemployed_2020':
                merged_df[new_column_name] = round(((merged_df[column1] - merged_df[column2]) / merged_df[column2]), 2)
            else:
                merged_df[new_column_name] = round(((merged_df[column1] - merged_df[column2]) / merged_df[column2]) * 100, 2)
            
        self.percentual_diff_between_2020_and_avg_2017_2019 = merged_df[['geo',  'nights_spent_%_diff_from_avg_2017_2019_to_2020', 'GDP_per_capita_%_diff_from_avg_2017_2019_to_2020', 'unemployed_%_diff_from_avg_2017_2019_to_2020']]

        print('ATTENTION 5')
        print(self.percentual_diff_between_2020_and_avg_2017_2019)

        self.percentual_diff_between_2020_and_avg_2017_2019.to_csv('output/diff_between_2020_and_avg_2017_2019.csv', index=False)
    
    def categorize_percentual_diff_from_2017_2019_to_2020(self):

        self.percentual_diff_between_2020_and_avg_2017_2019.dropna(inplace=True)

        values = self.percentual_diff_between_2020_and_avg_2017_2019['nights_spent_%_diff_from_avg_2017_2019_to_2020']
        classifier = NaturalBreaks(values, k=6)

        self.percentual_diff_between_2020_and_avg_2017_2019['impact_category'] = classifier.yb

        print(self.percentual_diff_between_2020_and_avg_2017_2019)
        self.percentual_diff_between_2020_and_avg_2017_2019.to_csv('output/night_spent_diff.csv')

        thresholds = classifier.bins
        print("Thresholds for each category:")
        for i, threshold in enumerate(thresholds):
            print(f"Category {i}: {threshold:.2f}")
        
        df = pd.merge(self.percentual_diff_between_2020_and_avg_2017_2019, self.nuts2_polygons, left_on='geo', right_on='NUTS_ID')
        df.drop(columns=['NUTS_ID', 'LEVL_CODE'], inplace=True)
        gdf = gpd.GeoDataFrame(df, geometry='geometry')
        print(gdf.head())
        gdf.to_file("output/night_spent_diff_with_geom.shp")



































    def mean_number_of_employed_in_tourist_industry_2017_2019(self):

        self.tourist_industry_2017_2019 = self.tourist_industry[self.tourist_industry['TIME_PERIOD'].isin([2017, 2018, 2019])].reset_index(drop=True)
        self.avg_tourist_industry_2017_2019 = self.tourist_industry_2017_2019.groupby(['geo', 'nace_r2'])['number_of_employed'].mean().reset_index()
        print(self.avg_tourist_industry_2017_2019)
        print(self.population_mean)