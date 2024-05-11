import pandas as pd
import geopandas as gpd


class ReadData():

    def __init__(self):

        self.read_in_polygon_data()
        self.read_in_population_data()
        self.read_in_nights_spent_tourist_data()
        self.read_in_bed_places_tourist_data()
        self.read_in_GDP_data()
        self.read_in_tourist_industry_data()
        self.read_in_unemployed_data()

    def read_in_polygon_data(self):
        fp = 'data/nuts_polygons.gpkg'

        self.nuts_polygons = gpd.read_file(fp)


    def read_in_population_data(self):
        fp = 'data/nuts2_broad_age_population.csv.gz'

        self.population_data = pd.read_csv(fp)


    def read_in_nights_spent_tourist_data(self):
        fp = 'data/nights_spent_at_tourist_accommodations_nuts2.gz'

        self.nights_spent_tourist_data = pd.read_csv(fp)


    def read_in_bed_places_tourist_data(self):
        fp = 'data/number_of_est_and_bed_places_nuts2.csv.gz'

        self.bed_places_tourist_data = pd.read_csv(fp)


    def read_in_GDP_data(self):
        fp = 'data/GDP_pps_per_capita_nuts2.csv.gz'

        self.GDP_data = pd.read_csv(fp)
    
    def read_in_tourist_industry_data(self):

        fp = 'data/employed_tourist_industry_per_nuts2.csv.gz'

        self.tourist_industry = pd.read_csv(fp)
    
    
    def read_in_unemployed_data(self):

        fp = 'data/unemployment_rate_nuts2_total_isced.csv.gz'

        self.unemployed_data = pd.read_csv(fp)




