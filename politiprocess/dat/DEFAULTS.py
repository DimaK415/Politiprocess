default_dict =  {'STOPFILE':
                    {'Default Path'                     : 'dat/stop.words'},

                'PRAWAPI':
                    {'Default Path'                     : 'dat/praw.secret',
                    'DAT':
                        {'API Script Keys':
                            {'client_id'                : '',
                            'client_secret'             : '',
                            'password'                  : '',
                            'user_agent'                : '',
                            'username'                  : '',}}},

                'MONGO':
                    {'Default Path'                     : 'dat/mongo.secret',
                    'DAT':
                        {'Mongo DB Server Params':  
                            {'host'                     : '',
                            'port'                      : '',
                            'db'                        : '',
                            'collection'                : '',}}},

                'SCRAPERLOG':
                    {'Default Path'                     : 'log/empty_scraper.log',
                    'DAT':
                        {'ScraperLog':
                            {'Date'                     : '',
                            'Scraper_Timer'             : '',
                            'Article_Count'             : '',
                            'Invalid_Links '            : '',
                            'Failed_Links_Count'        : '',
                            'Failed_Links'              : '',
                            'Red_Sub_Count'             : '',
                            'Blue_Sub_Count'            : '',}}},

                'SCRAPER':
                    {'Default Path'                     : 'dat/scraper.cfg',
                    'DAT':
                        {'Reddit Params':
                            {'Red List'                 : 'conservative, republican',
                            'Blue List'                 : 'liberal, democrats',
                            'Scraper Depth Limit'       : '30'},
                        'Article':
                            {'None Article Links'       : 'www.reddit.com, i.reddit.it'}}},

                'PARAMS':
                    {'Default Path'                     : 'save/params/current.cfg',
                    'DAT':
                        {'Query':
                            {'Time Frame in Hours'      : '24',
                             'Red Blue or All'          : 'All'},
                        'PreProcessing':
                            {'Fix Unicode'              : '1',
                             'All Lowercase'            : '0',
                             'Remove Newline'           : '1',
                             'Remove Punctuation'       : '0',
                             'Remove Contradictions'    : '0',
                             'Remove Emails'            : '1',
                             'Remove Accents'           : '1',
                             'Replace Currency'         : '1'},
                        'Spacy Params':
                            {'Spacy Model'              : 'en',
                             'Min Word Length'          : '2',
                             'Use Cleaned Text'         : '1',
                             'Named Entity List'        : 'PERSON, GPE, ORG, NORP',
                             'Split Columns'            : '0'},
                        'TFIDF Params':
                            {'Use IDF'                  : '1 ',
                             'Normalize'                : '0 ',
                             'Sublinear TF'             : '1',
                             'Smooth IDF'               : '0',
                             'Vocabulary'               : 'None',
                             'Min DF'                   : '0',
                             'Max DF'                   : '0.6',
                             'Min IC'                   : '0.0',
                             'Max Terms'                : '0',
                             'Column to Vectorize'      : 'chunks_ents'},
                        ' Decomposition Params':
                            {'Number of Topics'         : '10',
                             'Model Type'               : 'nmf'},
                        ' Visualizer':
                            {'Top Terms Per Topic'      : '10',
                             'Sort Terms By'            : 'seriation',
                             'Depth of Termite Plot'    : '50',
                             'Highlight'                : '0, 1, 2, 3, 4, 5',
                             'Save'                     : '1',
                             'Save Directory'           : '/Plots'}}}}