"""Example of Python client calling Knowledge Graph Search API."""
import json
import urllib.parse
import urllib.request
import os
import sys
from tqdm import tqdm
from colorama import Fore
import wikipedia

from utils import load_entities,getFromWikipediaAPI,getFromGoogleAPI,getFromOpenAI,getFromGoogleWikipediaAPI,getFromGoogleWiktionaryAPI,getFromWiktionaryAPI

dataset='WN18RR-subset'
data_dir=f'data/{dataset}/'
save_dir=f'save/{dataset}/'
char_len=512

entities=load_entities(dataset,data_dir)

# key= open('.api_key_Google').read()
# cx=open('.cx_google_wikipedia').read()
# # getFromGoogleAPI(key,entities,'save/FB15k-237-subset/')
#
# getFromGoogleWikipediaAPI(entities,save_dir,key,True,cx)

# key= open('.api_key_OpenAI').read()
# getFromOpenAI(key,entities,save_dir)
# print()

key= open('.api_key_Google2').read()
cx=open('.cx_google_wiktionary').read()


getFromGoogleWiktionaryAPI(entities,save_dir,key,cx)

# getFromWiktionaryAPI(entities,save_dir)