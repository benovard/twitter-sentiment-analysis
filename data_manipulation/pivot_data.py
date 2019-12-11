import csv
import pandas as pd

"""This script converts individual rows of data into a matrix with each keyword as a column
    and matching sentiment values by timestamp"""

df = pd.read_csv('../tweet_data/interpolated_data.csv', header=0)

df = df.pivot_table(index=['date_col'], columns='keyword', values='sentiment').fillna(0)

print(df.head())

df.to_csv('../tweet_data/matrix_data.csv', header=True)