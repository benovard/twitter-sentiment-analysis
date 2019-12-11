import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from ipywidgets import widgets, interactive

"""Creates a simple interactive matplotlib plot"""

df = pd.read_csv('../tweet_data/matrix_data.csv', header=0)

select1 = widgets.Dropdown(
    options=list(df.columns),
    description='first keyword'
)

select2 = widgets.Dropdown(
    options=list(df.columns),
    description='second keyword'
)


def plot(select1, select2):

    df.plot(kind='line', x='date', y=select1)
    df.plot(kind='line', x='date', y=select2)
    plt.axhline(color='black')
    plt.show()


interactive(plot, select1=select1, select2=select2)

ax = plt.gca()
df.plot(kind='line', x='date', y='wind', ax=ax)
df.plot(kind='line', x='date', y='solar', ax=ax)
plt.axhline(color='black')
plt.ylim((-1.5, 1.5))
plt.show()