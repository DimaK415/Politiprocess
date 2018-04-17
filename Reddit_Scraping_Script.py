print('Loading Libraries')

# Standard Libraries 
import pandas as pd
import numpy as np
from datetime import datetime

# URL Parser
from urllib.parse import urlparse

# Reddit API
import praw

# Sentiment and NLP TextBlob
from textblob import TextBlob

# Newspaper3k
from newspaper import Article

# MongoDB
from pymongo import MongoClient

print('Complete')


print('Loading Reddit Params')

fileObj = open('Scraper_Params.dat', mode='r')

reddit_params = {}

for line in fileObj:
    line = line.strip()
    
    key_value = line.split('=')
    if len(key_value) == 2:
        reddit_params[key_value[0].strip()] = key_value[1].strip()

print('Complete')
print('Assigning Variables')

api = praw.Reddit(client_id=      reddit_params['client_id'],
                  client_secret=  reddit_params['client_secret'],
                  password=       reddit_params['password'],
                  user_agent=     reddit_params['user_agent'],
                  username=       reddit_params['username'])

red_sub_list = reddit_params['red_list'].strip().split(', ')
blu_sub_list = reddit_params['blu_list'].strip().split(', ')

sub_limit    = int(reddit_params['limit_per_sub'].strip().split(', ')[0])

mongo_host   = str(reddit_params['mongodb_host'])
mongo_port   = int(reddit_params['mongodb_port'])

print('Complete')

def subreddit_title_scraper(df = True):
    
    global sub_limit
    global red_sub_list
    global blu_sub_list
    global api
    
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
    
    article_count = 0
    invalid_links = 0
    failed_links = 0
    
    for sub in red_sub_list + blu_sub_list:
        submissions = (x for x in api.subreddit(sub).hot(limit=sub_limit) if not x.stickied)
        
        for post in submissions:
            
            if sub in red_sub_list:
                posts_dict["target"].append(True)
            if sub in blu_sub_list:
                posts_dict["target"].append(False)
           
            posts_dict["post title"].append(post.title)           ## praw reddit scraping to dict##
            posts_dict["link"].append(post.url)
            posts_dict["score"].append(int(post.score))
            posts_dict["subreddit"].append(sub)
            posts_dict["date"].append(datetime.fromtimestamp(post.created_utc))
            
            comments = []                                         ## Comments parsing and scoring 
            for comment in post.comments:
                if comment.author != 'AutoModerator':
                    comments.append((round(comment.score/(post.num_comments), 2), comment.body))
            posts_dict["comments"].append(comments)
            
            parsed_url = urlparse(post.url)                       ## Parse URL for domain
            posts_dict['domain'].append(parsed_url.netloc)
            
            post_blob = TextBlob(post.title)                      ## TextBlob NLP - VERY SIMPLE
            posts_dict["title polarity"].append(post_blob.sentiment[0])
            posts_dict["title objectivity"].append(post_blob.sentiment[1])
            posts_dict["keywords"].append(post_blob.noun_phrases)
            
            
            article = Article(post.url)                           ## Instantiate newspaper3k library ##
            if article.is_valid_url():                            ## Is post a URL?  ##
                
                try:                                                         ## Try to download and parse article ##
                    article.download()
                    article.parse()
                    
                    article_count += 1
                    posts_dict["is article"].append(True)
                    
                    if article.title != []:                                  ## Title parsed? ##
                        posts_dict["article title"].append(article.title)
                    else:
                        posts_dict["article title"].append(np.nan)
                    
                    if article.authors != []:                                ## Author parsed?  ##
                        posts_dict["author"].append(article.authors)
                    else:
                        posts_dict["author"].append(np.nan)
                        
                    if article.text != []:                                   ## Text parsed?  ##
                        posts_dict['text'].append(article.text)
                    else:
                        posts_dict["text"].append(np.nan)
                    
                    if article_count % 5 == 0:
                        print(f"Added {article_count} articles")

                except:                               
                    failed_links += 1
                    posts_dict["is article"].append(False)
                    posts_dict["article title"].append(np.nan)
                    posts_dict["author"].append(np.nan)
                    posts_dict["text"].append(np.nan)
                    
                    if invalid_links % 5 == 0:
                        print(f"{failed_links} links failed parse")
                    
                    pass
            
                        
            else:
                invalid_links += 1
                posts_dict["is article"].append(False)
                posts_dict["article title"].append(np.nan)
                posts_dict["author"].append(np.nan)
                posts_dict["text"].append(np.nan)
                
                if invalid_links % 5 == 0:
                        print(f"{invalid_links} none-articles added")
                
                    
    if df:
        
        print(f"creating data frame from {article_count + invalid_links } links. {failed_links} failed to download")
        
        posts_df = pd.DataFrame(posts_dict)                             ## Make it a dataframe ##
        posts_df =posts_df[["subreddit",
                            "post title",
                            "score",
                            "keywords",
                            "comments",
                            "title polarity",
                            "title objectivity",
                            "domain", 
                            "link",
                            "is article",
                            "article title",
                            "author",
                            "text",
                            "date", 
                            "target"
                           ]]
        
        print(f"Done processing {article_count} articles and {invalid_links} non-articles as dataframe")
        
        return posts_df
                
    else:
        print(f"Done processing {article_count} articles and {invalid_links} non-articles as dictionary")
        
        return posts_dict

print(f"Pulling {sub_limit} posts from {str(blu_sub_list)} and {str(red_sub_list)}")

df = subreddit_title_scraper(df = True)

print('Complete')

print('Connecting to MongoDB')

client = MongoClient(host=mongo_host, port=mongo_port)

db = client.Politiprocess

collection = db.reddit_posts

print('Connection Established')

print('Converting DataFrame to BSON')

data = df.to_dict(orient='records')

print('Complete')

print('Updating Records in Database')

old_count = collection.count()

for post in data:
    collection.update_one({'link': post['link']},{'$set': post}, upsert=True)
    
new_count = collection.count()

added_count = new_count - old_count

print(f'Added {added_count} Entries to Database')
print('All Processes Completed Succesfully')

## Garbage Collection ##

data = []
df = []