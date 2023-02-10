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
            'page': 1,
            'offset': 100,            #10000 is max, more does the api not support
            'startblock': 0,
            'endblock': 27025780,
            'sort': 'asc',
            'apikey': "K3XB7RJNEGRD8GGK42UDBCQQN4HUMB483H"
            }

        r = requests.get(self.url, params=self.params)
        json_data = json.loads(r.text)["result"]
        df = pd.json_normalize(json_data)
        #df = df[["timeStamp", "hash", "nonce", "blockHash", "transactionIndex", "from", "to", "value",
         #"gas", "gasPrice", "gasUsed"]]

        return df


#Dictionary for the ContractAdresses of the NFT Collections we are getting the Data from
#After "The Sandbox" the Top 10 Art NFTs where included
Contract_Adresses = {
    "Bored Ape Yacht Club": "0xbc4ca0eda7647a8ab7c2061c2e118a18a936f13d",
    "CryptoPunks": "0xb47e3cd837ddf8e4c57f05d70ab865de6e193bbb",
    "Mutant Ape Yacht Club": "0x60e4d786628fea6478f785a6d7e704777c86a7c6",
    "Otherdeed for Otherside": "0x34d85c9cdeb23fa97cb08333b511ac86e1c4e258",
    "Azuki": "0xed5af388653567af2f388e6224dc7c4b3241c544",
    "Clone X - X Takashi": "0x49cf6f5d44e70224e2e23fdcdd2c053f30ada28b",
    "Moonbirds": "0x23581767a106ae21c074b2276d25e5c3e136a68b",
    "Doodles": "0x8a90cab2b38dba80c64b7734e58ee1db38b8992e",
    "Bored Ape Kennel Club": "0xba30e5f9bb24caa003e9f2f0497ad287fdf95623",
    "The Sandbox": "0x5cc5b05a8a13e3fbdb0bb9fccd98d38e50f90c38",
    "CrypToadz": "0x1cb1a5e65610aeff2551a50f76a87a7d3fb649c6",
    "SuperRare": "0xb932a70a57673d89f4acffbe830e8ed7f75fb9e0",
    "Chromie Squiggle": "0x059edd72cd353df5106d2b9cc5ab83a52287ac3a",
    "My Curio Cards": "0x73da73ef3a6982109c4d5bdb0db9dd3e3783f313",
    "Deadfellaz": "0x2acab3dea77832c09420663b0e1cb386031ba17b",
    "Meridian": "0xa7d8d9ef8d8ce8992df33d8b8cf4aebabd5bd270",
    "Checks": "0x34eebee6942d8def3c125458d1a86e0a897fd6f9",
    "Dooplicator": "0x466cfcd0525189b573e794f554b8a751279213ac",
    "FULL SEND METACARD NFT": "0x7ecb204fed7e386386cab46a1fcb823ec5067ad5",
    "MakersPlace": "0x2a46f2ffd99e19a89476e2f62270e0a35bbf0756"

}


#Combining all of the NFT Transaction Informations in one DataFrame:

"""""
def getDF(Contract_Adresses: dict):

    adresses = Contract_Adresses.values()
    dfs = []

    for i in adresses:
        run = TokenTransferEvents().__int__(i)
        df_A = pd.DataFrame(run)
        dfs.append(df_A)

    df = pd.concat(dfs)
    return df
"""


def getDF(Contract_Adresses: dict):
    adresses = Contract_Adresses.values()
    labels = Contract_Adresses.keys()
    dfs = []

    for i, j in zip(adresses, labels):
        run = TokenTransferEvents().__int__(i)
        df_A = pd.DataFrame(run).assign(label=j)
        dfs.append(df_A)

    df1 = pd.concat(dfs[:10])
    df1["label"] = "NFT_all"
    df2 = pd.concat(dfs[10:])
    df2["label"] = "NFT_art"

    df = pd.concat([df1, df2])
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

def CentralityGraph(df):
    # Convert DataFrame into an adjacency list
    edges = []
    for index, row in df.iterrows():
        edge = (row['from'], row['to'], {'tokenID': row['tokenID'], 'gasUsed': row['gasUsed']})
        edges.append(edge)

    # Create graph object
    G = nx.Graph()
    G.add_edges_from(edges)

    # Compute centrality
    centrality = nx.betweenness_centrality(G, k=10, endpoints=True)

    # Dictionary for mapping node names to scores of 'centrality'
    node_centrality = dict(centrality)

    top_nodes = sorted(node_centrality, key=node_centrality.get, reverse=True)[:10]

    node_labels = {node: node for node in top_nodes}

    # Compute community structure
    lpc = nx.community.label_propagation_communities(G)
    community_index = {n: i for i, com in enumerate(lpc) for n in com}

    label_mapping = {node: data['label'] for node, data in df.iterrows()}

    # Extracting the last column "label" from the DataFrame
    labels = df['label'].to_dict()

    # Creating list of colors based on the labels
    colors = [labels.get(node, 'blue') for node in G.nodes()]

    # Draw graph
    nx.draw(G, node_color=colors, node_size=[v * 2000 for v in centrality.values()], labels=node_labels)
    plt.show()


#Network Graph colored different NFTs:

def colNetGraph(df):
    # Create an empty graph
    G = nx.Graph()

    # Add nodes
    for index, row in df.iterrows():
        G.add_node(row["from"], label=row["label"])
        G.add_node(row["to"], label=row["label"])

    # Add edges
    for index, row in df.iterrows():
        G.add_edge(row["from"], row["to"], weight=row["gasUsed"])

    # Get a list of unique labels
    labels = list(set(df["label"]))

    # Map the labels to colors
    label_colors = {label: color for label, color in
                    zip(labels, plt.get_cmap('viridis')(np.linspace(0, 1, len(labels))))}

    # Map the nodes to their respective labels
    label_mapping = nx.get_node_attributes(G, 'label')

    # Compute centrality
    centrality = nx.betweenness_centrality(G, k=10, endpoints=True)

    # Color the nodes based on their labels
    node_colors = [label_colors[label_mapping[node]] for node in G.nodes()]

    # Draw the graph
    nx.draw(G, node_color=node_colors, labels=label_mapping, node_size=[v * 2000 for v in centrality.values()])
    plt.show()

#First NetworkGraph
def NetworkGraph(df):
    G = nx.from_pandas_edgelist(df, source='from', target='to')
    nx.draw_spring(G)
    plt.show()

colNetGraph(df)
#CentralityGraph(df)        #Either use df or df_Drop to visualize the data






