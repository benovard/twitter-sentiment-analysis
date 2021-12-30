This work involves analyzing the sentiment of various topics on Twitter. The sentiment is analyzed to look for trends between topics and over time. A package called textblob is used to evaluate the sentiment of tweets containing certain keywords related to clean energy. A neural network is then used to predict the future sentiment of keywords based on the past history of that word and other words.

The main data pulling from Twitter is done in main.py.

predict_multiple.py and predict_series.py do the prediction using a neural network.

The files with the id's of the tweets I pulled were too big to be uploaded to Github, but can be downloaded
from this site: https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/5QCCUU

Any script that references 'climate_id.txt' through 'climate_id4.txt' is referencing these files.

index.html contains a UI for graphing and viewing the prediction data.

