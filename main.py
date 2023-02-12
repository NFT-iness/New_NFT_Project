#Used Libraries:
import re
import numpy as np
import pandas as pd
import praw
import json
import requests
import matplotlib.pyplot as plt
import datetime
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from scipy.special import softmax
from matplotlib.patches import Patch
import snscrape.modules.twitter as sntwitter
from bs4 import BeautifulSoup as bs
from requests import get


###Ouptut Modification For Pycharm###
desired_width=320
pd.set_option('display.width', desired_width)
pd.set_option('display.max_columns',20)
######################################



###################### Scrapping - Social Media #################################################################

#RedditScrapping
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
    "Moonbirds": "0x23581767a106ae21c074b2276d25e5c3e136a68b",
    "Meebits": "0x7bd29408f11d2bfc23c34f18275bbf23bb716bc7",
    "Cool Cats NFT": "0x1a92f7381b9f03921564a437210bb9396471050c",
    "Pudgy Penguins": "0xbd3531da5cf5857e7cfaa92426877b022e612cf8",
    "World of Women": "0xe785e82358879f061bc3dcac6f0444462d4b5330",
    "Parallel Alpha_coll": "0x76be3b62873462d2142405439777e971754e8e77",
    "CrypToadz": "0x1cb1a5e65610aeff2551a50f76a87a7d3fb649c6",
    "CryptoKitties": "0x06012c8cf97bead5deae237070f9587f8e7a266d",
    "ZED RUN Legacy_coll": "0xa5f1ea7df861952863df2e8d1312f7305dabf215",
    "Axie Infinity": "0xf5b0a3efb8e8e4c201e2a935f110eaaf3ffecb8d",

    "Ethereum Name Service": "0x57f1887a8bf19b14fc0df6fd9b2acc9af147ea85",
    "Decentraland Names": "0x2a187453064356c898cae034eaed119e1663acb8",
    "dotbit(.bit)": "0x2a187453064356c898cae034eaed119e1663acb8",
    "Unstoppable Domains": "0xa9a6a3626993d487d2dbda3173cf58ca1a9d9e9f",
    "Ether Name Service": "0xcc7187ddbe8f099d31bac88d8d67f793001d718e",
    "Decentraweb - Top & Sub-level Domains": "0x3eaf3d0e21f452adf632744b5608e6c02e88827a",
    "WNS: Web3 Name Service": "0xba9bbea08241845013b40a061e4a77c9345e4562",
    "EDNS Domains": "0x53a0018f919bde9c254bda697966c5f448ffddcb",
    "Cryptovoxels Names": "0x4243a8413a77eb559c6f8eaffa63f46019056d08",
    "StoryFire - Social Entertainment Platform": "0x495f947276749ce646f68ac8c248420045cb7b5e",

    "WVRPS by WarpSound (Official)": "0xcbc67ea382f8a006d46eeeb7255876beb7d7f14d",
    "The Orbs by BT": "0x52e66ca968010d064938a8099a172cbaaf08c125",
    "EulerBeats Genesis": "0x8754f54074400ce745a7ceddc928fb1b7e985ed6",
    "EulerBeats Enigma": "0xa98771a46dcb34b34cdad5355718f8a97c8e603e",
    "KINGSHIP": "0x9f83b08d90eeda539f7e2797fed3f6996917bba8",
    "Stickmen Toys": "0x2a459947f0ac25ec28c197f09c2d88058a83f3bb",
    "Audioglyphs": "0xfb3765e0e7ac73e736566af913fa58c3cfd686b7",
    "Dogg on it: Death Row Mixtape Vol.1": "0x2953399124f0cbb46d2cbacd8a89cf0599974963",
    "SAN Origin": "0x33333333333371718a3c2bb63e5f3b94c9bc13be",
    "Snoop Dogg - B.O.D.R": "0xc36cf0cfcb5d905b8b513860db0cfe63f6cf9f5c",

    "Justin Aversano - Twin Flames": "0x495f947276749ce646f68ac8c248420045cb7b5e",
    "Where My Vans Go": "0x509a050f573be0d5e01a73c3726e17161729558b",
    "Editions x Guido": "0x8887ce34f6f1a4de4e8eb2a9195eeb261c413365",
    "Women Unite 10k Assemble": "0xbee7cb80dfd21a9eaae714208f361601f68eb746",
    "Justin Aversano - Twin Flames - Cyanotype Collection": "0x495f947276749ce646f68ac8c248420045cb7b5e",
    "Beautiful Cities of the World": "0x495f947276749ce646f68ac8c248420045cb7b5e",
    "First Day Out by DrifterShoots": "0x6913233ada65330adf01f24f715dffcc60497cc8",
    "Somewhere Else: A Collection of 100 Palms by Will Nichols": "0x495f947276749ce646f68ac8c248420045cb7b5e",
    "Math Art (1980-1995)": "0x46ac8540d698167fcbb9e846511beb8cf8af9bd8",
    "Ghozali Everyday": "0x2953399124f0cbb46d2cbacd8a89cf0599974963",


    "Sorare": "0x629a673a8242c2ac4b7b8c5d8735fbeac21a6205",
    "ZED RUN Legacy_card": "0xa5f1ea7df861952863df2e8d1312f7305dabf215",
    "VaynerSports Pass VSP": "0xbce6d2aa86934af4317ab8615f89e3f9430914cb",
    "The Association": "0xd7bea2b69c7a1015aadaa134e564eee6d34149c0",
    "F1 Delta Time": "0x2af75676692817d85121353f0d6e8e9ae6ad5576",
    "Legion DAO": "0x7c6f282efbe06e93de4ab5e646478bee20f966b8",
    "MLB Champions": "0x7c6f282efbe06e93de4ab5e646478bee20f966b8",
    "Knights of Degen": "0xe3f92992bb4f0f0d173623a52b2922d65172601d",
    "Wrapped Strikers": "0x11739d7bd793543a6e83bd7d8601fcbcde04e798",
    "ZED Run": "0x67f4732266c7300cca593c814d46bee72e40659f",

    "Parallel Alpha_tradeCards": "0x76be3b62873462d2142405439777e971754e8e77",
    "My Curio Cards_tradeCards": "0x73da73ef3a6982109c4d5bdb0db9dd3e3783f313",
    "Trump Digital Trading Cards": "0x24a11e702cd90f034ea44faf1e180c0c654ac5d9",
    "Meme Ltd.": "0xe4605d46fd0b3f8329d936a8b258d69276cba264",
    "Playing Arts Crypto Edition": "0xc22616e971a670e72f35570337e562c3e515fbfe",
    "BCCG": "0xe4c3421645edcf1f4f60d79684aee32c366adf95",
    "Ether Cards Founder": "0x97ca7fe0b0288f5eb85f386fed876618fb9b8ab8",
    "PolkaPets TCG": "0x8cb813bf27dc744fc5fb6ba7515504de45d39e08",
    "Yokai Kingdom Genesis": "0x35b0ecc952cef736c12a7ef3a830f438f67912b3",
    "Bullrun Babes": "0x4ad4455ad5ef891695c221e8e683efa65fabede0",

    "Emblem Vault": "0x82c7a8f707110f5fbb16184a5933e9f78a34c6ab",
    "Metroverse Genesis": "0x0e9d6552b85be180d941f1ca73ae3e318d2d4f1f",
    "oncyber labs": "0x226bf5293692610692e2c996c9875c914d2a7f73",
    "Project NANOPASS": "0xf54cc94f1f2f5de012b6aa51f1e7ebdc43ef5afc",
    "JRNY Club": "0x0b4b2ba334f476c8f41bfe52a428d6891755554d",
    "PREMINT Collector Pass": "0xe0176ba60efddb29cac5b15338c9962daee9de0c",
    "Decentral Games ICE Poker All Access Wearables": "0xdd649d6daceff4e504231718868d577a67feb18a",
    "Rug Radio - Genesis NFT": "0x8ff1523091c9517bc328223d50b52ef450200339",
    "10KTF Stockroom": "0x7daec605e9e2a1717326eedfd660601e2753a057",
    "The Watch": "0x236672ed575e1e479b8e101aeeb920f32361f6f9",

    "Otherdeed for Otherside": "0x34d85c9cdeb23fa97cb08333b511ac86e1c4e258",
    "The Sandbox": "0x5cc5b05a8a13e3fbdb0bb9fccd98d38e50f90c38",
    "Decentraland": "0xf87e31492faf9a91b02ee0deaad50d51d56d5d4d",
    "NFT Worlds": "0xbd4455da5929d5639ee098abfaa3241e9ae111af",
    "Worldwide Webb Land": "0xa1d4657e0e6507d5a94d06da93e94dc7c8c44b51",
    "Voxels": "0x79986af15539de2db9a5086382daeda917a9cf0c",
    "Town Star": "0xc36cf0cfcb5d905b8b513860db0cfe63f6cf9f5c",
    "Somnium Space VR": "0x2a378c8d96e7d994fb9bec6adb7c6af2fe772c3b",
    "Arcade Land": "0x4a8c9d751eeabc5521a68fb080dd7e72e46462af",
    "Treeverse Plots": "0x1b829b926a14634d36625e60165c0770c09d02b2"


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
    df1["label"] = "Art"
    df2 = pd.concat(dfs[10:25])
    df2["label"] = "Collectibles"
    df3 = pd.concat(dfs[25:35])
    df3["label"] = "DomainNames"
    df4 = pd.concat(dfs[35:45])
    df4["label"] = "Music"
    df5 = pd.concat(dfs[45:55])
    df5["label"] = "Photography"
    df6 = pd.concat(dfs[55:65])
    df6["label"] = "Sports"
    df7 = pd.concat(dfs[65:75])
    df7["label"] = "Trading_cards"
    df8 = pd.concat(dfs[75:85])
    df8["label"] = "Utility"
    df9 = pd.concat(dfs[85:95])
    df9["label"] = "Virtual_worlds"

    df = pd.concat([df1, df2, df3, df4, df5, df6, df7, df8, df9])

    #changing the UNIX timestamp into useable date-time values:
    df['timeStamp'] = df['timeStamp'].astype(int)
    df['timeStamp'] = df['timeStamp'].apply(lambda x: datetime.datetime.fromtimestamp(x).strftime('%Y-%m-%d %H:%M:%S'))

    return df

df = getDF(Contract_Adresses)

print(df.info())


def DataSelection(DataFrame, column):
    df = DataFrame.drop_duplicates(subset=[column])
    return df


pd.set_option('display.max_rows', None)

df_Drop = DataSelection(df, "transactionIndex")

print(df_Drop.info())
print(df_Drop.head())

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

#Network Graph colored different NFTs:

def LabeldNetGraph(df):
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
    #nx.draw_networkx_labels(G, pos, labels= label_mapping, font_size=0.05) #making the text size doesn't really work...

    # Create a custom legend
    patches = [Patch(color=color, label=label) for label, color in label_colors.items()]
    plt.legend(handles=patches, loc='upper left', frameon=False)

    plt.show()

#First NetworkGraph
def NetworkGraph(df):
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
    pos = nx.kamada_kawai_layout(G)  # Best alternative layout to kamada_kawai found: nx.planar_layout(G)

    # Draw the graph
    nx.draw(G, pos, node_color=node_colors, labels={}, node_size=[v * 5000 for v in centrality.values()])
    # nx.draw_networkx_labels(G, pos, labels= label_mapping, font_size=0.05) #making the text size doesn't really work...

    # Create a custom legend
    patches = [Patch(color=color, label=label) for label, color in label_colors.items()]
    plt.legend(handles=patches, loc='upper left', frameon=False)

    plt.show()

def ScatterC(df):
    df_plot = df[['tokenID', 'label']]

    plt.scatter(df_plot['tokenID'], df_plot['label'])

    plt.xlabel('NFT Tokens')
    plt.ylabel('NFT Genres')
    plt.title('Distribution of Tokens among the NFT Genres')

    plt.show()

def BarC(df):
    df_count = df['label'].value_counts()
    df_count.plot(kind='bar')
    plt.title('NFT Popularity')
    plt.xticks(rotation=25)
    plt.show()

def LinePlot(df):
    grouped = df.groupby('label')
    fig, ax = plt.subplots()

    # Plot each group in a different line
    for name, group in grouped:
        group['gasUsed'] = group['gasUsed'].astype(int)
        group.set_index('timeStamp').plot(ax=ax, y='gasUsed', label=name)

    ax.set_xlabel('Time')
    ax.set_ylabel('Used Gas')
    ax.legend()
    plt.title('GasUsed Over Time on different NFTs')
    plt.show()





################################Executng Plots#########################################################################

#LabeldNetGraph(df_Drop)     #df_Drop, otherwise to messy
#NetworkGraph(df)           #df can be used because this graph doesn't use labels and can be analyzed by comparing the nodes
#BarC(df)
#LinePlot(df)






