# Twitter and Mastodon Investigation<br>(a sentiment analysis, SIR contagion analysis, and time series forcasting study)
In this study, we analyzed and investigated the aftereffect of Twitter acquisition. We used three models: the sentiment analysis model, the SIR compartmental model, and the Long Short-Term Memory(LSTM) model to investigate why people leave Twitter, analyze Mastodon's user number increase, and predict Mastodon's future user growth using the latter two models.


### Sample Data
sample_data directory is the csvs used for sentiment analysis under the twitter directory, the used mastodon data contains the csvs used for our SIR and LSTM models

### Get Tweets
get_Tweets.py is sentiment analysis script

### Mastodon Data and SIR Model
SIR_result.ipynb is the visualization of Mastodon Data used for our SIR and LSTM Models, as well as our implementation of the SIR model

### LSTM Model
lstm_result.py is the script for our lstm model for forecasting user counts of Mastodon
