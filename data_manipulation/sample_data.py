import pandas as pd
import sys
import csv

"""This script interpolates the sentiment at one hour intervals so that all keywords
    have matching timestamps. To be run before pivot_data.py"""

df = pd.read_csv('../tweet_data/sentiment_data.csv', header=0)
df['date'] = pd.to_datetime(df['date'])
df = df.sort_values(by='date')

df = df.drop(['polarity'], axis=1)

# get first week of data
df = df[:88349]

# separate by keyword
climate = df[df.keyword == 'climate change']
warming = df[df.keyword == 'warming']
coal = df[df.keyword == 'coal']
solar = df[df.keyword == 'solar']
renewable = df[df.keyword == 'renewable']
oil = df[df.keyword == 'oil']
natural_gas = df[df.keyword == 'natural gas']
nuclear = df[df.keyword == 'nuclear']
wind = df[df.keyword == 'wind']


for frame in [coal, solar, climate, warming, renewable, oil, natural_gas, nuclear, wind]:
    frame = frame.sort_values(by='date')
    keyword = frame.iloc[0]['keyword']
    frame = frame.drop(['keyword'], axis=1)

    # re-sample and interpolate to 1 hour intervals
    frame.index = frame['date']
    frame = frame.resample('60T').mean()
    frame['sentiment'] = frame['sentiment'].interpolate()
    frame['date_col'] = frame.index
    frame['keyword'] = keyword

    frame.to_csv('../tweet_data/interpolated_data2.csv', mode='a', index=None, header=False)
