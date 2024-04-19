import pandas as pd
import geopandas as gpd


class ReadData():

    def __init__(self):

        self.read_in_polygon_data()
        self.read_in_population_data()
        self.read_in_nights_spent_tourist_data()
        self.read_in_bed_places_tourist_data()
        self.read_in_gdp_data()

    def read_in_polygon_data(self):

        fp = 'data/nuts_polygons.gpkg'

        self.nuts_polygons = gpd.read_file(fp)
        print('Polygon:')
        print(self.nuts_polygons.head(10))

    def read_in_population_data(self):

        fp = 'data/NUTS2_population_count.csv.gz'

        self.population_data = pd.read_csv(fp)
        print('Population')
        print(self.population_data.head(20))

    def read_in_nights_spent_tourist_data(self):

        fp = 'data/nights_spent_at_tourist_accommodations_nuts2.gz'

        self.nights_spent_tourist_data = pd.read_csv(fp)
        print('Nights spent Tourist')
        print(self.nights_spent_tourist_data.head(20))


    def read_in_bed_places_tourist_data(self):

        fp = 'data/number_of_est_and_bed_places_nuts2.csv.gz'

        self.bed_places_tourist_data = pd.read_csv(fp)
        print('Bed places Tourist')
        print(self.bed_places_tourist_data.head(20))

    def read_in_gdp_data(self):

        fp = 'data/GDP_pps_per_capita_nuts2.csv.gz'

        self.gdp_data = pd.read_csv(fp)
        print('GDP')
        print(self.gdp_data.head(20))



