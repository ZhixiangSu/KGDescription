"""Example of Python client calling Knowledge Graph Search API."""
import json
import urllib.parse
import urllib.request
import os
import sys
from tqdm import tqdm
from colorama import Fore
import wikipedia
import openai
from utils import load_entities,getFromWikipediaAPI,getFromGoogleAPI

max_chars=512

entities=load_entities('data/FB15k-237-subset/')

# key= open('.api_key_Google').read()
# response=getFromGoogleAPI(key,entities)

# getFromWikipediaAPI(entities)
print()




OPENAI_API_KEY = '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'
openai.api_key = OPENAI_API_KEY
messages=[{"role": "user", "content": 'As an intelligent AI model, if you could be any fictional character, who would you choose and why?'}]

response = openai.ChatCompletion.create(
model="gpt-3.5-turbo",
max_tokens=max_chars,
temperature=1.2,
messages = messages)

print(response)
