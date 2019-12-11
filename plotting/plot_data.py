import pandas as pd
import matplotlib.pyplot as plt
import sys

"""Plots the history of the sentiment of keywords"""

df = pd.read_csv('../tweet_data/sentiment_data.csv', header=0)
df['date'] = pd.to_datetime(df['date'])
df = df.sort_values(by='date')

df = df.drop(['polarity'], axis=1)

df = df[:52500]


climate = df[df.keyword == 'climate change']
warming = df[df.keyword == 'warming']
coal = df[df.keyword == 'coal']
solar = df[df.keyword == 'solar']


for frame in [coal, solar, climate, warming]:
    frame = frame.sort_values(by='date')
    frame = frame.drop(['keyword'], axis=1)

    # re-sample and interpolate to 1 hour intervals
    frame.index = frame['date']
    frame = frame.resample('60T').mean()
    frame['sentiment'] = frame['sentiment'].interpolate()
    frame['date_col'] = frame.index
    # get daily averages
    frame['date_col'] = pd.to_datetime(frame['date_col']).dt.date
    frame = frame.groupby('date_col')['sentiment'].mean()
    frame = frame.reset_index()

    plt.plot(frame['date_col'], frame['sentiment'])

plt.legend(labels=['coal', 'solar', 'climate change', 'warming'])
plt.axhline(color='black')
plt.xlabel('Time')
plt.ylabel('Sentiment')
plt.show()
