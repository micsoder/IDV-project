import pandas as pd
print('hello')

fp = 'data/NUTS2_population_count.csv.gz'

df = pd.read_csv(fp)
print(df)