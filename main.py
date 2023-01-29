#Used Libraries:
import re

import pandas as pd
import praw
import requests
import urllib.request
import snscrape.modules.twitter as sntwitter
from bs4 import BeautifulSoup as bs



####Web Scrapping - Part

#Class for RedditScrapping
class ScrapeReddit:
    def __init__(self, user_agent, client_id, client_secret):
        self.user_agent= user_agent
        self.client_id = client_id
        self.client_secret = client_secret


        self.redit = praw.Reddit(
            client_id = self.client_id,
            client_secret = self.client_secret,
            user_agent = self.user_agent)


    def FindTopics(self):
        headlines = set()
        ids = set()
        creator = set()
        for submission in self.redit.subreddit("NFT").top(limit=None):

            headlines.add(submission.title)
            ids.add(submission.id)
            creator.add(submission.author)
            #.add(submission.created_utc)
            #.add(submission.score)
            #.add(submission.upvote_ratio)
            #.add(submission.url)


        df_headlines = pd.DataFrame(list(headlines) , columns=['Headlines:'])
        df_ids = pd.DataFrame(list(ids), columns=['IDs:'])
        df_author = pd.DataFrame(list(creator), columns=['Creator:'])

        df_comb = pd.concat([df_headlines, df_ids, df_author], axis=0)

        return df_comb

"""""
r1_input = ScrapeReddit("Scraper 1.0 by u/ExoticTrack-200", 'hzOgEEsCkTaBb1gHTVkpsw', 'grDAf4hLL7slDn2-9cN32F6JcdxOuA')
r1 = r1_input.FindTopics()

print(r1)

"""

#ScrappingCryptoSlam:
l = set()

#page & url
page = urllib.request.urlopen("https://www.cryptoslam.io/nfts")
soup = bs(page, "html.parser")

#getting elements
element = soup.find('a', class_= "MuiTypography-root MuiTypography-inherit MuiLink-root MuiLink-underlineNone css-1ci8y0t")
#function_names = re.findall('0x\w+', str(names))

print(element)


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









