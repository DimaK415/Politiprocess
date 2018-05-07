import pandas as pd
from datetime import datetime
from datetime import timedelta
from pymongo import MongoClient
import pytz
import os

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
        self.added_count= None

    def utc_to_pacific(self, utc_dt):
        local_tz = pytz.timezone('America/Los_Angeles')
        os.environ['TZ'] = 'America/Los_Angeles'
        local_dt = utc_dt.replace(tzinfo=pytz.utc).astimezone(local_tz)
        return local_tz.normalize(local_dt)
        
    def load_all(self):
        self.query_df = pd.DataFrame(list(self.collection.find()))
        
    def query(self, red_or_blue=None, articles=None, n_hours=None, count=None,
        custom_query=None, append_dfs= False, verbose=False):
        
        self.query_dict = {}

        if not red_or_blue:
            red_or_blue = self.settings.Query.Red_Blue_or_All
        if not articles:
            articles = self.settings.Query.Articles_Only
        if not n_hours:
            n_hours = self.settings.Query.Time_Frame_in_Hours
        if not append_dfs:
            append_dfs = self.settings.Query.Append_DFs
        if not count:
            count = self.settings.Query.Count
        else:
            n_hours = 0

        if articles:
            self.query_dict['is article'] = articles
            
        if articles:
            post = 'articles'
        else:
            post = 'documents'
        
        if not n_hours:
            if verbose:
                print(f"Pulling {count} {post} from {red_or_blue} targets.")
        else:
            if verbose:
                print(f"Pulling {red_or_blue} articles from last {n_hours} hours.")
            dt = datetime.utcnow() - timedelta(hours=n_hours)
            self.query_dict['date'] = {'$gt': dt}
        
        if red_or_blue == 'Red':
            self.query_dict['target'] = True
        elif red_or_blue == 'Blue':
            self.query_dict['target'] = False
        elif red_or_blue == 'All':
            self.query_dict['target'] = [True, False]

        if custom_query:
            self.query_dict = {**self.query_dict, **custom_query}

        if self.query_dict['target'] == [True, False]:
            self.query_dict['target'] = True
            self.red_df = pd.DataFrame(list(self.collection.find(self.query_dict, sort=[('_id', -1)], limit=count)))
            self.red_df.name = 'Red'
            self.query_dict['target'] = False
            self.blue_df = pd.DataFrame(list(self.collection.find(self.query_dict, sort=[('_id', -1)], limit=count)))
            self.blue_df.name = 'Blue'
        if append_dfs:
            self.query_df= self.red_df.append(self.blue_df)
            self.query_df.name = 'All'
        
        if verbose:
            print(f'''Completed pulling {len(self.query_df)} {post}.
        Latest article is from {self.collection.find_one(sort=[('date', -1)])['date']} UTC''')

    def update_from_df(self, df=None, drop_id=None, upsert=None, set_local=None, verbose=False):

        try:
            if not df:
                df = self.query_df
        except:
            pass
        if not drop_id:
            drop_id = self.mongo_cfg.Options.Set_Local
        if not upsert:
            upsert = self.mongo_cfg.Options.Upsert
        if not set_local:
            set_local = self.mongo_cfg.Options.Set_Local

        if drop_id:
            df = df.drop(['_id'], axis=1)

        data = df.to_dict(orient='records')
        
        old_count = self.collection.count()
        
        for post in data:
            self.collection.update_one({'link': post['link'], 'subreddit': post['subreddit']},{'$set': post}, upsert=upsert)
            
        new_count = self.collection.count()
        
        self.added_count = new_count - old_count

        if verbose:
            print(f'Added {self.added_count} Entries to Database')

        if set_local:
            time_stamp = datetime.ctime(self.utc_to_pacific(datetime.now()))
        else:
            time_stamp = datetime.ctime(datetime.now())

        log = Parameters()
        log.loader('log/mongo.log', default=True)

        log.loaded.MONGOLOG.Date    = time_stamp
        log.loaded.MONGOLOG.Added   = self.added_count
        log.loaded.MONGOLOG.Total   = new_count

        log.writer('log/scraper.log', log.loaded, append=True)

    def count(self, query=None, red_or_blue=None):
        count_query = {}
        if red_or_blue == 'Red':
            count_query['target'] = 1
        elif red_or_blue == 'Blue':
            count_query['target'] = 0

        return self.collection.count(count_query)
