#Used Libraries:
import pandas as pd
import praw
import requests
from bs4 import BeautifulSoup as bs



####Web Scrapping - Part

#Class for RedditScrapping
class ScrapeReddit:
    def __init__(self, user_agent, client_id, client_secret):
        self.user_agent= user_agent
        self.client_id = client_id
        self.client_secret = client_secret

    def Access(self):
        self.redit = praw.Reddit(
            client_id = self.client_id,
            client_secret = self.client_secret,
            user_agent = self.user_agent

        )

    def FindTopics(self):
        self.headlines = set()
        for submission in self.redit.subreddit("NFT").hot(limit=None):
            print(submission.title)         #prints are for testing the function
            print(submission.id)
            print(submission.author)
            print(submission.created_utc)
            print(submission.score)
            print(submission.upvote_ratio)
            print(submission.url)
            break                           #to stop an overload
            headlines.add(submission.titel) #for summary of interesting headlines about NFTs

    def result2DF(self):
        df = pd.DataFrame(self.headlines)
        df.head()




#Kaggle Datasets
#basic:
b_data = pd.read_csv('https://raw.githubusercontent.com/hemil26/NFT-Dataset/master/nft_sales.csv')
#twitter:



#Class to read in Datasets, make Analysis and return results
class Analyse_Dataset:
    def __init__(self, data):
        self.data = data

    def show_data(self):
        print(self.data.head())









