import os
import pandas as pd
from pprint import pprint

data = {}

file_list = [os.path.join(root, file) for root, dirs, files in os.walk(os.path.expanduser("dcss/data/")) for file in files]

for file_path in file_list:
    file = file_path.split('.')[0]
    try:
        filename = file.split('\\')[2]
    except:
        filename = file.split('/')[3]
    data[filename] = file_path



def list_datasets():
    pprint(data)


def load(filename):
    """
    Loads one of the datasets used in DCSS.
    """
    df = pd.read_csv(data[filename], low_memory=False)
    return df

def load_dataset(dataset):
    """
    Loads the full V-DEM 10 dataset.
    """
    dfs = []
    for file in os.listdir(os.path.join('dcss/data/' + dataset)):
        datapath = os.path.join('dcss/data/' + dataset, file)
        df = pd.read_csv(datapath, low_memory=False)
        dfs.append(df)
    df = pd.concat(dfs)
    return df
