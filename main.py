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
            'offset': 100,            #10000 is max, more does the api not support, using more than 100 costs a lot of computational power with same results => the pattern are similar
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
    "Bored Ape Yacht Club_art": "0xbc4ca0eda7647a8ab7c2061c2e118a18a936f13d",
    "CryptoPunks_art": "0xb47e3cd837ddf8e4c57f05d70ab865de6e193bbb",
    "Rarible": "0xd07dc4262bcdbf85190c01c996b4c06a461d2430",
    "SuperRare": "0xb932a70a57673d89f4acffbe830e8ed7f75fb9e0",
    "Karafuru": "0xd2f668a8461d6761115daf8aeb3cdf5f40c532c6",
    "Hashmasks": "0xc2c747e0f7004f9e8817db2ca4997657a7746928",
    "My Curio Cards_art": "0x73da73ef3a6982109c4d5bdb0db9dd3e3783f313",
    "3Landers": "0xb4d06d46a8285f4ec79fd294f78a881799d8ced9",
    "PhantaBear": "0x67d9417c9c3c250f61a83c7e8658dac487b56b09",
    "Creepz by OVERLORD": "0xfe8c6d19365453d26af321d0e8c910428c23873f",

    "CryptoPunks_coll": "0xb47e3cd837ddf8e4c57f05d70ab865de6e193bbb",
    "Bored Ape Yacht Club_coll": "0xbc4ca0eda7647a8ab7c2061c2e118a18a936f13d",
    "Mutant Ape Yacht Club": "0x60e4d786628fea6478f785a6d7e704777c86a7c6",
    "Azuki": "0xed5af388653567af2f388e6224dc7c4b3241c544",
    "Clone X - X TAKASHI MURAKAMI": "0x49cf6f5d44e70224e2e23fdcdd2c053f30ada28b",

    "Ethereum Name Service": "0x57f1887a8bf19b14fc0df6fd9b2acc9af147ea85",
    "Decentraland Names": "0x2a187453064356c898cae034eaed119e1663acb8",
    "dotbit(.bit)": "0x2a187453064356c898cae034eaed119e1663acb8",
    "Unstoppable Domains": "0xa9a6a3626993d487d2dbda3173cf58ca1a9d9e9f",
    "Ether Name Service": "0xcc7187ddbe8f099d31bac88d8d67f793001d718e",

    "WVRPS by WarpSound (Official)": "0xcbc67ea382f8a006d46eeeb7255876beb7d7f14d",
    "The Orbs by BT": "0x52e66ca968010d064938a8099a172cbaaf08c125",
    "EulerBeats Genesis": "0x8754f54074400ce745a7ceddc928fb1b7e985ed6",
    "EulerBeats Enigma": "0xa98771a46dcb34b34cdad5355718f8a97c8e603e",
    "KINGSHIP": "0x9f83b08d90eeda539f7e2797fed3f6996917bba8",

    "Justin Aversano - Twin Flames": "0x495f947276749ce646f68ac8c248420045cb7b5e",
    "Where My Vans Go": "0x509a050f573be0d5e01a73c3726e17161729558b",
    "Editions x Guido": "0x8887ce34f6f1a4de4e8eb2a9195eeb261c413365",
    "Women Unite": "0xbee7cb80dfd21a9eaae714208f361601f68eb746",
    "First Day Out by DrifterShoots": "0x6913233ada65330adf01f24f715dffcc60497cc8",

    "Sorare": "0x629a673a8242c2ac4b7b8c5d8735fbeac21a6205",
    "VaynerSports Pass VSP": "0xbce6d2aa86934af4317ab8615f89e3f9430914cb",
    "The Association": "0xd7bea2b69c7a1015aadaa134e564eee6d34149c0",
    "F1 Delta Time": "0x2af75676692817d85121353f0d6e8e9ae6ad5576",
    "Legion DAO": "0x7c6f282efbe06e93de4ab5e646478bee20f966b8",
    "MLB Champions": "0x7c6f282efbe06e93de4ab5e646478bee20f966b8",

    "Parallel Alpha": "0x76be3b62873462d2142405439777e971754e8e77",
    "My Curio Cards_tradeCards": "0x73da73ef3a6982109c4d5bdb0db9dd3e3783f313",
    "Trump Digital Trading Cards": "0x24a11e702cd90f034ea44faf1e180c0c654ac5d9",
    "Meme Ltd.": "0xe4605d46fd0b3f8329d936a8b258d69276cba264",
    "Playing Arts Crypto Edition": "0xc22616e971a670e72f35570337e562c3e515fbfe",

    "Emblem Vault": "0x82c7a8f707110f5fbb16184a5933e9f78a34c6ab",
    "Metroverse Genesis": "0x0e9d6552b85be180d941f1ca73ae3e318d2d4f1f",
    "oncyber labs": "0x226bf5293692610692e2c996c9875c914d2a7f73",
    "Project NANOPASS": "0xf54cc94f1f2f5de012b6aa51f1e7ebdc43ef5afc",
    "JRNY Club": "0x0b4b2ba334f476c8f41bfe52a428d6891755554d",

    "Otherdeed for Otherside": "0x34d85c9cdeb23fa97cb08333b511ac86e1c4e258",
    "The Sandbox": "0x5cc5b05a8a13e3fbdb0bb9fccd98d38e50f90c38",
    "Decentraland": "0xf87e31492faf9a91b02ee0deaad50d51d56d5d4d",
    "NFT Worlds": "0xbd4455da5929d5639ee098abfaa3241e9ae111af",
    "Worldwide Webb Land": "0xa1d4657e0e6507d5a94d06da93e94dc7c8c44b51"


}


#Combining all of the NFT Transaction Informations in one DataFrame:
def getDF(Contract_Adresses: dict):
    adresses = Contract_Adresses.values()
    labels = Contract_Adresses.keys()
    dfs = []

    for i, j in zip(adresses, labels):
        run = TokenTransferEvents().__int__(i)
        df_A = pd.DataFrame(run).assign(label=j)
        dfs.append(df_A)

    df1 = pd.concat(dfs[:10])
    df1["label"] = "NFT_art"
    df2 = pd.concat(dfs[10:15])
    df2["label"] = "NFT_collectibles"
    df3 = pd.concat(dfs[15:20])
    df3["label"] = "NFT_DomainNames"
    df4 = pd.concat(dfs[20:25])
    df4["label"] = "NFT_music"
    df5 = pd.concat(dfs[25:30])
    df5["label"] = "NFT_photograpy"
    df6 = pd.concat(dfs[30:36])
    df6["label"] = "NFT_sports"
    df7 = pd.concat(dfs[36:41])
    df7["label"] = "NFT_trading_cards"
    df8 = pd.concat(dfs[41:46])
    df8["label"] = "NFT_utility"
    df9 = pd.concat(dfs[46:51])
    df9["label"] = "NFT_virtual_worlds"

    df = pd.concat([df1, df2, df3, df4, df5, df6, df7, df8, df9])
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

    df["gasUsed"] = df["gasUsed"].astype(int)

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

    # Resizing with Fruchterman-Reingold layout to fix Data overlapping issues
    pos = nx.kamada_kawai_layout(G) #Best alternative layout to kamada_kawai found: nx.planar_layout(G)

    # Draw the graph
    nx.draw(G, pos, node_color=node_colors, labels=label_mapping, node_size=[v * 2000 for v in centrality.values()])
    nx.draw_networkx_labels(G, pos, labels= label_mapping, font_size=0.05) #making the text size doesn't really work...
    plt.show()

#First NetworkGraph
def NetworkGraph(df):
    G = nx.from_pandas_edgelist(df, source='from', target='to')
    nx.draw_spring(G)
    plt.show()

colNetGraph(df_Drop)
#CentralityGraph(df)        #Either use df or df_Drop to visualize the data






