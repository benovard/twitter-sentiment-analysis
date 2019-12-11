import pandas as pd

# removes duplicate rows from index files. Only needs to be run once

file = '../id_data/climate_id4.txt'

df = pd.read_csv(file, sep='\n')
print(df.count())
df.drop_duplicates(inplace=True)
print(df.count())

df.to_csv(file, index=False)
