import pandas as pd
from datetime import datetime
from datetime import timedelta
from pymongo import MongoClient
from tqdm import tqdm

from Paramerator import parameters

class connect:
    def __init__(self):
        
        _params = parameters()
        _mongo  = _params.loader('dat/mongo.secret').MongoDBServerParams
        
        self.client     = MongoClient(host=_mongo.host, port=_mongo.port)
        self.db         = getattr(self.client, _mongo.db)
        self.collection = getattr(self.db, _mongo.collection)
        self.query_df   = None
        self.query_dict = {}
        
    def load_all(self):
        self.query_df = pd.DataFrame(list(self.collection.find()))
        return self.query_df
        
    def query(self, red_or_blue = 'Both', articles = True, n_hours = 24, custom_query = {}):
        
        self.query_dict = {'is article': articles}
            
        if articles:
            post = 'articles'
        else:
            post = 'documents'
        
        if n_hours == 0:
            print(f"Pulling all {post} from {red_or_blue} targets.")
        else:
            print(f"Pulling {red_or_blue} articles from last {n_hours} hours.")
            dt = datetime.utcnow() - timedelta(hours=n_hours)
            self.query_dict['date'] = {'$gt': dt}
        
        if red_or_blue == 'Red':
            self.query_dict['target'] = True
        elif red_or_blue == 'Blue':
            self.query_dict['target'] = False
        else:
            pass

        if custom_query:
            self.query_dict = {**self.query_dict, **custom_query}

        self.query_df = pd.DataFrame(list(self.collection.find(self.query_dict)))
    
        print(f'''Completed pulling {len(self.query_df)} {post}.
        Latest article is from {self.collection.find_one(sort=[('date', -1)])['date']} UTC''')

        return self.query_df

    def update_from_df(self, custom_df=None, upsert=True):
        if custom_df is not None:
            data = custom_df.to_dict(orient='records')
        else:
            data = self.query_df.to_dict(orient='records')
        
        old_count = self.collection.count()
        
        for post in tqdm(data):
            self.collection.update_one({'link': post['link']},{'$set': post}, upsert=True)
            
        new_count = self.collection.count()
        
        added_count = new_count - old_count

        print(f'Added {added_count} Entries to Database')
        print('All Processes Completed Succesfully')

    def count(self, query=None, red_or_blue=None):
        return self.collection.count(query)
