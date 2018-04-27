import os
import pandas as pd
import numpy as np
from datetime import datetime
from urllib.parse import urlparse
import pytz
from tqdm import tqdm

import praw
from textblob import TextBlob
from newspaper import Article

from Paramerator import parameters

def utc_to_pacific(utc_dt):
    local_tz = pytz.timezone('America/Los_Angeles')
    os.environ['TZ'] = 'America/Los_Angeles'
    local_dt = utc_dt.replace(tzinfo=pytz.utc).astimezone(local_tz)
    return local_tz.normalize(local_dt)

def run(df = True, set_local=False):

    print('Starting Scraper')
    
    start_time = datetime.now()
    
    params = parameters()

    scraper_p  = params.loader('dat/scraper.cfg')
    reddit     = scraper_p.RedditParams
    art_ignore = scraper_p.Article.NoneArticleLinks
    API        = params.loader('dat/praw.secret').APIScriptKeys
        
    api = praw.Reddit(client_id      = API.client_id,
                      client_secret  = API.client_secret,
                      password       = API.password,
                      user_agent     = API.user_agent,
                      username       = API.username)
    
    posts_dict = {"post title"        : [],
                  "subreddit"         : [],
                  "score"             : [],
                  "is article"        : [],
                  "article title"     : [],
                  "title polarity"    : [],
                  "title objectivity" : [],
                  "keywords"          : [],
                  "domain"            : [],
                  "link"              : [],
                  "author"            : [],
                  "text"              : [],
                  "comments"          : [],
                  "date"              : [],
                  "target"            : [],
                   }
    
    article_count   = 0
    invalid_links   = 0
    failed_links_c  = 0
    failed_links    = []
    red_sub         = 0
    blue_sub        = 0

    print("Pulling Articles")
    
    for sub in reddit.RedList + reddit.BlueList:
        submissions = (x for x in api.subreddit(sub).hot(limit=reddit.ScraperDepthLimit) if not x.stickied)
        
        print(sub)
        for post in tqdm(submissions):
            
            if sub in reddit.RedList:
                posts_dict["target"].append(True)
                red_sub += 1
            if sub in reddit.BlueList:
                blue_sub += 1
                posts_dict["target"].append(False)
           
            posts_dict["post title"].append(post.title)           # praw reddit scraping to dict
            posts_dict["link"].append(post.url)
            posts_dict["score"].append(int(post.score))
            posts_dict["subreddit"].append(sub)
            posts_dict["date"].append(datetime.fromtimestamp(post.created_utc))
            
            comments = []                                         # Comments parsing and scoring 
            for comment in post.comments:
                if comment.author != 'AutoModerator':
                    comments.append((round(comment.score/(post.num_comments), 2), comment.body))
            posts_dict["comments"].append(comments)
            
            parsed_url = urlparse(post.url)                       # Parse URL for domain 
            posts_dict['domain'].append(parsed_url.netloc)
            
            post_blob = TextBlob(post.title)                      # TextBlob NLP - VERY SIMPLE 
            posts_dict["title polarity"].append(post_blob.sentiment[0])
            posts_dict["title objectivity"].append(post_blob.sentiment[1])
            posts_dict["keywords"].append(post_blob.noun_phrases)
            
            
            article = Article(post.url)                                     # Instantiate newspaper3k library
            if article.is_valid_url() and parsed_url.netloc not in art_ignore:
                
                try:                                                        # Try to download and parse article
                    article.download()
                    article.parse()
                    
                    article_count += 1
                    posts_dict["is article"].append(True)
                    
                    if article.title != []:                                  # Title parsed? 
                        posts_dict["article title"].append(article.title)
                    else:
                        posts_dict["article title"].append(np.nan)
                    
                    if article.authors != []:                                # Author parsed?
                        posts_dict["author"].append(article.authors)
                    else:
                        posts_dict["author"].append(np.nan)
                        
                    if article.text != []:                                   # Text parsed?
                        posts_dict['text'].append(article.text)
                    else:
                        posts_dict["text"].append(np.nan)

                except:                               
                    posts_dict["is article"].append(False)
                    posts_dict["article title"].append(np.nan)
                    posts_dict["author"].append(np.nan)
                    posts_dict["text"].append(np.nan)
                    failed_links_c +=1
                    failed_links.append(post.url)
                        
            else:
                invalid_links += 1
                posts_dict["is article"].append(False)
                posts_dict["article title"].append(np.nan)
                posts_dict["author"].append(np.nan)
                posts_dict["text"].append(np.nan)
    
    if set_local:
        time_now = utc_to_pacific(datetime.now())
    else:
        time_now = datetime.now()                                       # Set local Time
    log_date = time_now.strftime('%m%d%y_%H%M')

    print("Generating DataFrame")
    
    if df:
        
        posts_df = pd.DataFrame(posts_dict)                             # Make it a dataframe
        posts_df = posts_df[["subreddit",
                            "post title",
                            "title polarity",
                            "title objectivity",
                            "score",
                            "keywords",
                            "comments",
                            "domain", 
                            "link",
                            "is article",
                            "article title",
                            "author",
                            "text",
                            "date", 
                            "target"
                           ]]
        
        
        posts_df.to_pickle(f'log/{log_date}.pickle')
        
    z = datetime.now() - start_time
    scrape_time = f"{(z.seconds//60)%60}min, {z.seconds%60}sec"
    
    log = params.loader('log/empty_scraper.log')
    
    log.ScraperLog.Date               = time_now.ctime()
    log.ScraperLog.Scraper_Timer      = scrape_time
    log.ScraperLog.Article_Count      = article_count 
    log.ScraperLog.Invalid_Links      = invalid_links 
    log.ScraperLog.Failed_Links       = failed_links 
    log.ScraperLog.Failed_Links_Count = failed_links_c
    log.ScraperLog.Red_Sub_Count      = red_sub       
    log.ScraperLog.Blue_Sub_Count     = blue_sub      
    
    params.writer(f'log/{log_date}_scraper.log', log)
    
    if df: 
        return posts_df
    else:
        return