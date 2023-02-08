#Used Libraries:
import re
import numpy as np
import pandas as pd
import praw
import json
import requests
import matplotlib.pyplot as plt
import urllib
from urllib.request import Request, urlopen
import snscrape.modules.twitter as sntwitter
from bs4 import BeautifulSoup as bs
from requests import get


###Ouptut Modification For Pycharm###
desired_width=320
pd.set_option('display.width', desired_width)
pd.set_option('display.max_columns',20)
######################################



###################### Scrapping - Social Media #################################################################

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

############################## Scrapping Etherium Blockchain from Ehterscan#############################################

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
#transaction details of a specific Collection like the "Bored Ape Yacht Club"

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
        df = df[["timeStamp", "hash", "nonce", "blockHash", "transactionIndex", "from", "to", "value",
         "gas", "gasPrice", "gasUsed"]]

        return df


class TokenTransferEvents:

    def __int__(self, ContractAddress: str):
        self.url = 'https://api.etherscan.io/api'
        self.params = {
            'module': 'account',
            'action': 'tokennfttx',
            'address': ContractAddress,
            #'page': 1,
            #'offset': 100,
            #'startblock': 0,
            #'endblock': 27025780,
            #'sort': 'asc',
            'apikey': "K3XB7RJNEGRD8GGK42UDBCQQN4HUMB483H"
            }

        r = requests.get(self.url, params=self.params)
        json_data = json.loads(r.text)["result"]
        df = pd.json_normalize(json_data)
        #df = df[["timeStamp", "hash", "nonce", "blockHash", "transactionIndex", "from", "to", "value",
         #"gas", "gasPrice", "gasUsed"]]

        return df


#Dictionary for the ContractAdresses of the NFT Collections we are getting the Data from
Contract_Adresses = {
    "Bored Ape Yacht Club": "0xbc4ca0eda7647a8ab7c2061c2e118a18a936f13d",
    "CryptoPunks": "0xb47e3cd837ddf8e4c57f05d70ab865de6e193bbb",
    "Mutant Ape Yacht Club": "0x60e4d786628fea6478f785a6d7e704777c86a7c6",
    "Otherdeed for Otherside": "0x34d85c9cdeb23fa97cb08333b511ac86e1c4e258"
}



def getDF(Contract_Adresses: dict):

    adresses = Contract_Adresses.values()
    dfs = []

    for i in adresses:
        run = TokenTransferEvents().__int__(i)
        df_A = pd.DataFrame(run)
        dfs.append(df_A)

    df = pd.concat(dfs)
    return df


df = getDF(Contract_Adresses)

#df = TokenTransferEvents().__int__("0x34d85c9cdeb23fa97cb08333b511ac86e1c4e258")
print(df.info())


def DataSelection(DataFrame, column):
    df = DataFrame.drop_duplicates(subset=[column])
    return df


pd.set_option('display.max_rows', None)

df_Drop = DataSelection(df, "transactionIndex")

print(df_Drop)

#print(TTE['from'].value_counts())
#print(TTE['to'].value_counts())

#print(TTE[TTE['tokenID'] == '2'])






#Class to read in a final Dataset to make Analysis and return results
class Analyse_Dataset:
    def __init__(self, data):
        self.data = data

    def show_data(self):
        print(self.data.head())



####### Data Visualization ####################################################################

import networkx as nx
import scipy as sp

G = nx.from_pandas_edgelist(df, source='from', target='to')

nx.draw_spring(G)
plt.show()





