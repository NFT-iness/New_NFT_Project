#Used Libraries:
import re
import numpy as np
import pandas as pd
import praw
import json
import requests
import urllib
from urllib.request import Request, urlopen
import snscrape.modules.twitter as sntwitter
from bs4 import BeautifulSoup as bs
from requests import get



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

#ScrappingCryptoSlam from Ehterscan :

#Class to get Log data of a specific NFT, needs the NFT Contract Address to work!
class nft_log_data:
    def __int__(self, ContractAddress: str):
        self.url = 'https://api.etherscan.io/api'
        self.params = {
            'module': 'logs',
            'action': 'getLogs',
            'address': ContractAddress,
            'apikey': "K3XB7RJNEGRD8GGK42UDBCQQN4HUMB483H"
            }

        r = requests.get(self.url, params=self.params)
        json_data = json.loads(r.text)["result"]
        df = pd.json_normalize(json_data)
        #df[["topics", "data", "timeStamp", "transactionHash", ]].head()

        return df

#class to get nft transaction data
#transaction details 'From' & 'To'
class nft_transaction_data:
    def __int__(self, ContractAddress: str):
        self.url = 'https://api.etherscan.io/api'
        self.params = {
            'module': 'account',
            'action': 'txlist',
            'address': ContractAddress,
            'apikey': "K3XB7RJNEGRD8GGK42UDBCQQN4HUMB483H"
            }

        r = requests.get(self.url, params=self.params)
        json_data = json.loads(r.text)["result"]
        df = pd.json_normalize(json_data)
        #df[["topics", "data", "timeStamp", "transactionHash", ]].head()

        return df

###Ouptut Modification For Pycharm###
desired_width=320
pd.set_option('display.width', desired_width)
pd.set_option('display.max_columns',20)
######################################

t1 = nft_transaction_data().__int__("0xbc4ca0eda7647a8ab7c2061c2e118a18a936f13d")
print(t1.head())





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







