#Used Libraries:
import re
import numpy as np
import pandas as pd
import networkx as nx
import scipy as sp
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

#reading in csv Data to work with:
def GetData(CSV_file):
    df = pd.read_csv(CSV_file)
    return df



#normalization of the Data
def DataSelection(DataFrame, column):
    df = DataFrame.drop_duplicates(subset=[column])
    return df


GetData('NFT_RawData_Offset100')


pd.set_option('display.max_rows', None)

df_Drop = DataSelection(GetData('NFT_RawData_Offset100'), "transactionIndex")

print(df_Drop.info())
print(df_Drop.head())



#Class to read in a final Dataset to make Analysis and return results
class Analyse_Dataset:
    def __init__(self, data):
        self.data = data

    def show_data(self):
        print(self.data.head())



####### Data Visualization ####################################################################



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
    nx.draw(G, pos, node_color=node_colors, labels=label_mapping, node_size=[v * 1500 for v in centrality.values()])
    nx.draw_networkx_labels(G, pos, labels= label_mapping, font_size=0.05) #making the text size doesn't really work...

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
    nx.draw(G, pos, node_color=node_colors, labels={}, node_size=[v * 2500 for v in centrality.values()], edge_color='gainsboro', alpha=0.4)
    #nx.draw_networkx_labels(G, pos, labels= label_mapping, font_size=0.05) #making the text size doesn't really work...

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





################################Analysis#########################################################################

"""""
Hyperparameter that change our plots/results:
- using the 'normalized' (df_Drop) Version of our DataFrame
- 'Offset' in the 'TokenTransferEvents' class => Going further back in time the majority of traded NFTs are 
  Collectibles and Art. Other genres like 'sport cards', 'virtual worlds' etc. where later on introduced 

Further Restrictions:
- we are using (with one exception) only the Top10 rated Collections of each NFT genre

Recommendation:
- if the network graph shall capture also transactions between newer types of NFTs Offset should be set to 100
  and then either NetworkGraph or LabeldNetGraph can be plotted to study the traffic or bubble creation between
  different NFTs
 
"""""

################################Executng Plots#########################################################################

#LabeldNetGraph(df_Drop)     #df_Drop, otherwise to messy, => USING df_Drop AS NORMALIZED?????????????????????????????????
NetworkGraph(df_Drop)            #df can be used because this graph doesn't use labels and can be analyzed by comparing the nodes
#BarC(df_Drop)
#LinePlot(df)







