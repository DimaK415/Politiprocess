import pandas as pd
from datetime import datetime
from datetime import timedelta
from pymongo import MongoClient
from tqdm import tqdm

from Paramerator import Parameters

class Connect:
    def __init__(self, settings=None, mongo_cfg=None):
        
        self.settings   = settings
        self.mongo_cfg  = mongo_cfg

        self.mongo      = Parameters()
        self.mongo.loader('dat/mongo.secret', 'server')
        self._mongo     = self.mongo.server.Mongo_DB_Server_Params
        
        self.client     = MongoClient(host=self._mongo.host, port=self._mongo.port)
        self.db         = getattr(self.client, self._mongo.db)
        self.collection = getattr(self.db, self._mongo.collection)
        self.query_df   = None
        self.query_dict = {}
        
    def load_all(self):
        self.query_df = pd.DataFrame(list(self.collection.find()))
        
    def query(self, red_or_blue=None, articles=None, n_hours=None, custom_query=None):
        
        if not red_or_blue:
            red_or_blue = self.settings.Query.Red_Blue_or_All
        if not articles:
            articles = self.settings.Query.Articles_Only
        if not n_hours:
            n_hours = self.settings.Query.Time_Frame_in_Hours

        if articles:
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

    def update_from_df(self, df=None, drop_id=None, upsert=None):

        try:
            if not df:
                df = self.query_df
        except:
            pass
        if not drop_id:
            drop_id = self.mongo_cfg.Options.Set_Local
        if not upsert:
            upsert = self.mongo_cfg.Options.Upsert

        if drop_id:
            df = df.drop(['_id'], axis=1)

        data = df.to_dict(orient='records')
        
        old_count = self.collection.count()
        
        for post in tqdm(data):
            self.collection.update_one({'post title': post['post title']},{'$set': post}, upsert=upsert)
            
        new_count = self.collection.count()
        
        added_count = new_count - old_count

        print(f'Added {added_count} Entries to Database')

        log = Parameters()
        log.loader('log/mongo.log', default=True)

        log.loaded.MONGOLOG.Date    = datetime.ctime(datetime.now())
        log.loaded.MONGOLOG.Added   = added_count
        log.loaded.MONGOLOG.Total   = new_count

        log.writer('log/scraper.log', log.loaded, append=True)

    def count(self, query=None, red_or_blue=None):
        return self.collection.count(query)
