import json
import urllib.parse
import urllib.request
import os
import sys
from tqdm import tqdm
from colorama import Fore
import wikipedia

def getFromGoogleAPI(API_key,query_ids,batch_size=500):
    service_url = 'https://kgsearch.googleapis.com/v1/entities:search'
    responses=[]
    pbar = tqdm(total=len(query_ids),
                        position=0, leave=True,
                        file=sys.stdout, bar_format="{l_bar}%s{bar}%s{r_bar}" % (Fore.GREEN, Fore.RESET))
    for i in range(0,len(query_ids),batch_size):
        params = [
            ('ids',q[0]) for q in query_ids[i:i+batch_size]
        ]
        params.append(('key',API_key))
        url = service_url + '?' + urllib.parse.urlencode(params)
        response = json.loads(urllib.request.urlopen(url).read())
        responses.append(response)
        pbar.update(len(params)-1)
    pbar.close()
    return responses

def getFromWikipediaAPI(query_ids,char_len=512):
    responses=[]
    wikipedia.set_lang('en')
    for entity,name in query_ids:
        try:
            p = wikipedia.summary(name,chars=char_len,auto_suggest=False)
        except wikipedia.DisambiguationError as e:
            s = e.options[1]
            p = wikipedia.summary(s,chars=char_len,auto_suggest=False)
        responses.append(p)
    return responses


def load_entities(path):
    entities=[]
    with open(os.path.join(path,'entity2text.txt'),'r',encoding='utf-8') as f:
        for line in f:
            line = line.rstrip('\t\n')
            entity,name=line.split('\t')
            entities.append((entity,name))
    return entities