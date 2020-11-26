import requests
import json
import pickle
from time import time,sleep
import os
from tqdm import tqdm
import pandas as pd

if not os.path.isfile("mal_id_list_top_500.pkl"):
    mal_id_list = []

    url="https://api.jikan.moe/v3/top/anime/{}/bypopularity"
    for i in tqdm(range(10)):
        timeend = time()+4 # Rate Limit

        response = requests.get(url.format(str(i)))
        results=response.json()["top"]
        response.close()

        for res in results:
            mal_id = res["mal_id"]
            mal_id_list.append(mal_id)

        if timeend-time()>0:
            sleep(timeend-time()) # Rate Limit

    with open("mal_id_list_top_500.pkl","wb") as f:
        pickle.dump(mal_id_list,f)

with open("mal_id_list_top_500.pkl","rb") as f:
    mal_id_list=pickle.load(f)

"""   
"reviewer": {
    ...     
    "scores": {
            "overall": 8,
            "story": 8,
            "animation": 9,
            "sound": 9,
            "character": 8,
            "enjoyment": 9
            }
},
"content": "review text"
"""

data = [[0,0,0,0,0,0,"test review"]]
col = ['overall', 'story','animation','sound','character','enjoyment','review']
data = pd.DataFrame(data, columns = col) 
num = ['overall', 'story','animation','sound','character','enjoyment']

url="https://api.jikan.moe/v3/anime/{}/reviews/{}"
for mal_id in tqdm(mal_id_list):
    print("Working on MAL ID:",mal_id)
    for i in range(100):
        timeend = time()+4 # Rate Limit

        response = requests.get(url.format(str(mal_id),str(i)))
        reviews = response.json()["reviews"]
        response.close()

        if reviews[0] is None:
            break

        for r in reviews:
            score_data = [s for s in r["reviewer"]["scores"].values()]
            score_data.append(r["content"])
            df = pd.DataFrame([score_data],columns=col)
            data=data.append(df,ignore_index=True)
            data[num]=data[num].astype("int8")
        
        data.to_hdf('data.h5', key='df', mode='w')

        if timeend-time()>0:
            sleep(timeend-time()) # Rate Limit