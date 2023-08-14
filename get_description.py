"""Example of Python client calling Knowledge Graph Search API."""
import json
import urllib.parse
import urllib.request
import os
import sys
from tqdm import tqdm
from colorama import Fore
import wikipedia
import argparse

from utils import load_entities,getFromWikipediaAPI,getFromGoogleAPI,getFromOpenAI,getFromGoogleWikipediaAPI,getFromGoogleWiktionaryAPI,getFromWiktionaryAPI

parser = argparse.ArgumentParser(description='Detailed Description Generation')

parser.add_argument('--dataset', type=str, default='WN18RR-subset',)
parser.add_argument('--char_len', type=int, default='512',)
parser.add_argument('--source', type=str, default='GoogleWikipedia',
                    help='choose from [GoogleWikipedia,Wikipedia,Wiktionary,GoogleWiktionary,OpenAI]')
args = parser.parse_args()



data_dir=f'data/{args.dataset}/'
save_dir=f'save/{args.dataset}/'
entities=load_entities(args.dataset,data_dir)

if args.source=='GoogleWikipedia':
    key= open('.api_key_Google').read()
    cx=open('.cx_google_wikipedia').read()
    # getFromGoogleAPI(key,entities,'save/FB15k-237-subset/')

    getFromGoogleWikipediaAPI(entities,save_dir,key,True,cx,args.char_len)

elif args.source=='OpenAI':
    key= open('.api_key_OpenAI').read()
    getFromOpenAI(key,entities,save_dir,args.char_len)

elif args.source=='GoogleWiktionary':
    key= open('.api_key_Google2').read()
    cx=open('.cx_google_wiktionary').read()

    getFromGoogleWiktionaryAPI(entities,save_dir,key,cx,args.char_len)

elif args.source=='Wikipedia':
    getFromWikipediaAPI(entities,save_dir,True,args.char_len)

elif args.source=='Wiktionary':
    getFromWiktionaryAPI(entities,save_dir,args.char_len)