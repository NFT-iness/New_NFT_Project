#Used Libraries:
import re

import pandas as pd
import praw
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

BASE_url = "https://api.etherscan.io/api"
API_Key = "K3XB7RJNEGRD8GGK42UDBCQQN4HUMB483H"


#Function that produces an url for sending a GET request to:
def make_api_url(module, action, adress, **kwargs):
    url = BASE_url + f"?module={module}&action={action}&adress={adress}&apikey={API_Key}"

    for key, value in kwargs.items():
        url += f"&{key}={value}"

    return url

#Function to get 'normal' transactions:
def get_transaction(adress):
    get_transactions_url = make_api_url("account",
                                        "txlist",
                                        adress,
                                        startblock= 0,
                                        endblock = 99999999,
                                        page=1,
                                        offset = 10000,
                                        sort="desc")

    response = get(get_transactions_url)
    data = response.json()["result"]

    for tx in data:
        to = tx['to']
        from_addr = tx['from']
        value = tx['value']
        gas = tx['gasUsed']
        time = tx['timestamp']

        print("---------------------------------------------------")
        print("To:", to)
        print("From:", from_addr)
        print("Value:", value)
        print("Gas used:", gas)
        print("TransactionDate:", time)

    print(data)

adress = "0xc5102fE9359FD9a28f877a67E36B0F050d81a3CC"
get_transaction(adress)

"""""
url = "https://etherscan.io/txs"
request_site = Request(url, headers={"User-Agent": "Mozilla/5.0"})
webpage = urlopen(request_site).read()
soup = bs(webpage, "html.parser")
result = soup.find('tr')

print(result)
print(soup)


#page & url
page = urllib.request.urlopen("https://etherscan.io/address/0x14ae8100Ea85a11bbb36578f83AB1b5C1cFDd61c")
soup = bs(page.content, "html.parser")

#getting elements
element = soup.find('a', class_= "MuiTypography-root MuiTypography-inherit MuiLink-root MuiLink-underlineNone css-1ci8y0t")
#function_names = re.findall('0x\w+', str(names))

print(element)
"""""

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









