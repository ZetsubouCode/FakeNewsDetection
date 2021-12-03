# -*- coding: utf-8 -*-
"""FakeNews.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1wwlYHotKhiQAM9r2NA482C6zIHMkZ0q5

Training Model
"""

import numpy as np
import pandas as pd
import itertools
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import PassiveAggressiveClassifier
from sklearn.metrics import accuracy_score, confusion_matrix



# Commented out IPython magic to ensure Python compatibility.
from google.colab import drive
drive.mount('/content/gdrive', force_remount=True)

# change to working directory on the drive
# %cd '/content/gdrive/My Drive/'

#Read the data
df=pd.read_csv('news.csv')
#Get shape and head
df.shape
df.head()

#DataFlair - Get the labels
labels=df.label
labels.head()

#DataFlair - Split the dataset
x_train,x_test,y_train,y_test=train_test_split(df['text'], labels, test_size=0.2, random_state=7)

#DataFlair - Initialize a TfidfVectorizer
tfidf_vectorizer=TfidfVectorizer(stop_words='english', max_df=0.7)
#DataFlair - Fit and transform train set, transform test set
tfidf_train=tfidf_vectorizer.fit_transform(x_train) 
tfidf_test=tfidf_vectorizer.transform(x_test)

#DataFlair - Initialize a PassiveAggressiveClassifier
pac=PassiveAggressiveClassifier(max_iter=50)
pac.fit(tfidf_train,y_train)
#DataFlair - Predict on the test set and calculate accuracy
y_pred=pac.predict(tfidf_test)
score=accuracy_score(y_test,y_pred)
print(f'Accuracy: {round(score*100,2)}%')

#DataFlair - Build confusion matrix
confusion_matrix(y_test,y_pred, labels=['FAKE','REAL'])

"""Twitter API Consume"""

!pip install tweepy

import tweepy
from textblob import TextBlob
import pandas as pd
import re

API_KEY = "XC8RN7qtQH9apkyqdOv1WkPeR"
API_SECRET = "08y6a6mMIfKe3mIXXLEeYs609LbNAF5pW9U1b2UNiUjXqwRIPq"
BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAAN7MVwEAAAAAXQtFdnPo3WMUEBLv2XsxEW7a4R8%3DZLfz63tW8P4P2N9tKMkhxAClEPvFQw8wKqFANzNRlq5uQ6nI3U"
ACCESS_TOKEN = "596090159-3KzqC9ndCEtGTE4aQbleluOSUDid0G8uQ3WXz3VB"
ACCESS_TOKEN_SECRET = "c9DANcKaOkH2Yvs4yOfQRb6Drb0yRJdPpgiDwTctoBEYZ"

auth = tweepy.OAuthHandler(API_KEY,API_SECRET)
auth.set_access_token(ACCESS_TOKEN,ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

# result = api.user_timeline(id="covid19",lang="en",count=1000)
result = api.search(q="covid",lang="en",count=100)

result

tweet_data = []
for tweet in result:
  tweet_property={}
  tweet_property["tanggal_tweet"] = tweet.created_at
  tweet_property["pengguna"] = tweet.user.screen_name
  tweet_property["isi_tweet"] = tweet.text
  tweet_property["tweet_bersih"] = ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)"," ",tweet.text).split())
  tweet_data.append(tweet_property)

tweet_data

def findLabel(text):
  vec_new_test = tfidf_vectorizer.transform([text])
  y_pred = pac.predict(vec_new_test)
  return y_pred

fake = 0
real = 0
for i in tweet_data:
  result_scanning = findLabel(i["tweet_bersih"])
  print("Data tweet =",i["tweet_bersih"])
  print("Hasil analisa =",result_scanning[0],"\n")
  if result_scanning[0]=='FAKE':
    fake+=1
  else:
    real+=1

print ("Total fake news =",fake)
print ("Total real news =",real)