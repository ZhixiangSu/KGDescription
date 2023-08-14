import json
import urllib.parse
import urllib.request
import os
import sys
from tqdm import tqdm
from colorama import Fore
import wikipedia
import openai
import time

def getFromGoogleAPI(API_key,query_ids,save_dir,batch_size=20):
    service_url = 'https://kgsearch.googleapis.com/v1/entities:search'
    responses=[]
    pbar = tqdm(total=len(query_ids),
                        position=0, leave=True,
                        file=sys.stdout, bar_format="{l_bar}%s{bar}%s{r_bar}" % (Fore.GREEN, Fore.RESET))
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    with open(os.path.join(save_dir,"entity2textGoogle.txt"),'a',encoding='utf-8') as f1, \
            open(os.path.join(save_dir,"entity2typeGoogle.txt"),'a',encoding='utf-8') as f2:
        for i in range(0,len(query_ids),batch_size):
            params = [
                ('ids',q[0]) for q in query_ids[i:i+batch_size]
            ]
            params.append(('key',API_key))
            url = service_url + '?' + urllib.parse.urlencode(params)
            r = json.loads(urllib.request.urlopen(url).read())
            text=[r['itemListElement'][i]['result']['detailedDescription']['articleBody'] for i in range(len(r['itemListElement']))]
            text=[t.replace('\n',' ') for t in text]
            text = [t.replace('\t', ' ') for t in text]
            text="\n".join(text)
            type="\n".join(["\t".join(r['itemListElement'][i]['result']['@type']) for i in range(len(r['itemListElement']))])
            f1.write(text+"\n")
            f2.write(type+"\n")
            f1.flush()
            f2.flush()
            pbar.update(len(params)-1)
        pbar.close()
def getFromGoogleWikipediaAPI(query_ids,save_dir,Google_API_key,Google_cx,check_url,char_len=512):
    if check_url:
        assert wikipedia.API_URL == 'http://en.wikipedia.org/w/api.php'
    service_url = 'https://customsearch.googleapis.com/customsearch/v1'
    responses = []

    pbar = tqdm(total=len(query_ids),
                position=0, leave=True,
                file=sys.stdout, bar_format="{l_bar}%s{bar}%s{r_bar}" % (Fore.GREEN, Fore.RESET))
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    continue_num = 40835
    pbar.update(continue_num)
    with open(os.path.join(save_dir, "entity2textGoogleWikipedia.txt"), 'a', encoding='utf-8') as f1:
        for entity, name in query_ids[continue_num:]:
            params = {
                'key': Google_API_key,
                'q': name,
                'cx': Google_cx,
                'start':0,
                'num': 10,
            }
            url = service_url + '?' + urllib.parse.urlencode(params)
            get_result=False
            while(not get_result):
                try:
                    r = json.loads(urllib.request.urlopen(url).read())
                    get_result=True
                except Exception as e:
                    time.sleep(60)
                    print(f'retry:{name}')
            if 'items' not in r:
                s = name
            else:
                s = urllib.parse.unquote(r['items'][0]['link']).split("/")[-1]
                s = s.replace("_"," ")
            s = s[:300]
            auto_suggest = False
            wikipedia.API_URL = 'http://en.wiktionary.org/w/api.php'
            keywords, suggestion = wikipedia.search(s, suggestion=True)
            if len(keywords) == 0 and suggestion != None:
                keywords, suggestion = wikipedia.search(suggestion, suggestion=True)
            if len(keywords) == 0:
                print(f'no search result:{s}')
                p = name
            else:
                s = keywords[0]
                times = 5
                while (times > 0):
                    times -= 1
                    try:
                        p = wikipedia.summary(s, chars=char_len, auto_suggest=auto_suggest)
                    except wikipedia.exceptions.PageError as e1:
                        if auto_suggest == False:
                            auto_suggest = True
                            continue
                        else:
                            print(f'no summary result:{entity}')
                            p = name
                    except wikipedia.DisambiguationError as e2:
                        s = e2.options[0]
                        auto_suggest = False
                        continue
                    break
                if times == 0:
                    print(f'no search result:{s}')
                    p = name
            text = p.replace('\n', ' ')
            text = text.replace('\t', ' ')
            text = entity + "\t" + text
            f1.write(text + '\n')
            f1.flush()
            pbar.update(1)
            time.sleep(1)
    pbar.close()
def getFromWikipediaAPI(query_ids,save_dir,check_url,char_len=512):
    if check_url:
        assert wikipedia.API_URL == 'http://en.wikipedia.org/w/api.php'
    responses=[]
    pbar = tqdm(total=len(query_ids),
                position=0, leave=True,
                file=sys.stdout, bar_format="{l_bar}%s{bar}%s{r_bar}" % (Fore.GREEN, Fore.RESET))
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    with open(os.path.join(save_dir, "entity2textWikipedia.txt"), 'a', encoding='utf-8') as f1:
        for entity,name in query_ids:
            s=name
            auto_suggest=False
            keywords, suggestion = wikipedia.search(s, suggestion=True)
            if len(keywords) == 0 and suggestion!=None:
                keywords, suggestion = wikipedia.search(suggestion, suggestion=True)
            if len(keywords) == 0:
                print(f'no search result:{s}')
                p = name
            else:
                s=keywords[0]
                times=5
                while(times>0):
                    times-=1
                    try:
                        p = wikipedia.summary(s, chars=char_len, auto_suggest=auto_suggest)
                    except wikipedia.exceptions.PageError as e1:
                        if auto_suggest==False:
                            auto_suggest= True
                            continue
                        else:
                            print(f'no summary result:{entity}')
                            p=name
                    except wikipedia.DisambiguationError as e2:
                        s = e2.options[0]
                        auto_suggest=False
                        continue
                    break
                if times==0:
                    print(f'no search result:{s}')
                    p=name

            text = p.replace('\n', ' ')
            text = text.replace('\t', ' ')
            text =entity+"\t"+text
            f1.write(text+'\n')
            f1.flush()
            pbar.update(1)
    pbar.close()

def getFromGoogleWiktionaryAPI(query_ids,save_dir,Google_API_key,Google_cx,char_len=512):
    #=================== IMPORTANT =======================
    # Wiktionary is not implemented by package wikipedia.
    # However, this api is applicable for wiktionary.
    # To use it for wiktionary, please manually change the variable API_URL in package 'wikipedia' to 'http://en.wiktionary.org/w/api.php'
    assert wikipedia.API_URL=='http://en.wiktionary.org/w/api.php'
    getFromGoogleWikipediaAPI(query_ids,save_dir,Google_API_key,Google_cx,False,char_len)

def getFromWiktionaryAPI(query_ids,save_dir,char_len=512):
    #=================== IMPORTANT =======================
    # Wiktionary is not implemented by package wikipedia.
    # However, this api is applicable for wiktionary.
    # To use it for wiktionary, please manually change the variable API_URL in package 'wikipedia' to 'http://en.wiktionary.org/w/api.php'
    assert wikipedia.API_URL=='http://en.wiktionary.org/w/api.php'
    getFromWikipediaAPI(query_ids,save_dir,False,char_len)


def getFromOpenAI(key,query_ids,save_dir,char_len=512,batch_size=10):
    pbar = tqdm(total=len(query_ids),
                position=0, leave=True,
                file=sys.stdout, bar_format="{l_bar}%s{bar}%s{r_bar}" % (Fore.GREEN, Fore.RESET))
    continue_num=0
    pbar.update(continue_num)
    with open(os.path.join(save_dir, "entity2textOpenAI.txt"), 'a', encoding='utf-8') as f1:
        for entity,name in query_ids[continue_num:]:
            times=5
            while(True):

                try:
                    openai.api_key = key
                    messages=[
                        {"role": "user", "content": f'Provide detailed descriptions about {name} for relation prediction on knowledge graph.'}]
                    p = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    max_tokens=char_len,
                    temperature=1.2,
                    messages = messages)
                    text=p['choices'][0]['message']['content']
                    text = text.replace('\n', ' ')
                    text = entity + "\t" + text
                    f1.write(text + '\n')
                    f1.flush()
                    pbar.update(1)
                except Exception as e:
                    times-=1
                    if times>0:
                        print(f'Error to get {entity}:{name}.\n')
                        continue
                    else:
                        raise Exception
                break

    pbar.close()

def load_entities(dataset,path):
    entities=[]
    with open(os.path.join(path,'entity2text.txt'),'r',encoding='utf-8') as f:
        for line in f:
            if dataset in ['FB15k-237-subset','FB15k-237-subset-inductive','NELL-995-subset','NELL-995-subset-inductive']:
                line = line.rstrip('\t\n')
                entity,name=line.split('\t')
                name=name.replace(":"," ")
                name=name.replace("-"," ")
                entities.append((entity,name))
            elif dataset in ['WN18RR-subset','WN18RR-subset-inductive']:
                line = line.rstrip('\t\n')
                entity, name = line.split('\t')
                name=name.split(',')[0]
                name = name.replace(":", " ")
                name = name.replace("-", " ")
                entities.append((entity, name))
            else:
                raise NotImplementedError
    return entities