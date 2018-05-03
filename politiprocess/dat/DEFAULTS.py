default_dict =  {'STOPFILE':
                    {'Default Path'                     : 'dat/stop.words'},

                'PRAWAPI':
                    {'Default Path'                     : 'dat/praw.secret',
                    'DAT':
                        {'API_Script_Keys':
                            {'client_id'                : '*',
                            'client_secret'             : '*',
                            'password'                  : '*',
                            'user_agent'                : '*',
                            'username'                  : '*',}}},

                'MONGOUPDATE':
                    {'Default Path'                     : 'dat/mongo.cfg',
                    'DAT':
                        {'Mongo_Update':
                            {'Drop_ID'                  : False,
                            'Upsert'                    : True,}}},

                'MONGO':
                    {'Default Path'                     : 'dat/mongo.secret',
                    'DAT':
                        {'Mongo_DB_Server_Params':  
                            {'host'                     : '*',
                            'port'                      : '*',
                            'db'                        : '*',
                            'collection'                : '*',}}},

                'SCRAPER':
                    {'Default Path'                     : 'dat/scraper.cfg',
                    'DAT':
                        {'Options': 
                            {'Set_Local'                : False,
                            'Upsert'                    : True},
                        'Reddit_Params':
                            {'Red_List'                 : ['conservative', 'republican'],
                            'Blue_List'                 : ['liberal', 'democrats'],
                            'Scraper_Depth_Limit'       : 30},
                        'Article':
                            {'None_Article_Links'       : ['www.reddit.com', 'i.reddit.it']},
                        'Pre_Processing':
                            {'Fix_Unicode'              : True,
                             'All_Lowercase'            : False,
                             'Remove_Newline'           : True,
                             'Remove_Punctuation'       : False,
                             'Remove_Contradictions'    : False,
                             'Remove_Emails'            : True,
                             'Remove_Accents'           : True,
                             'Replace_Currency'         : True},
                        'Spacy_Params':
                            {'Spacy_Model'              : 'en',
                             'Min_Word_Length'          : 2,
                             'Use_Cleaned_Text'         : 1,
                             'Named_Entity_List'        : ['PERSON', 'GPE', 'ORG', 'NORP'],
                             'Split_Columns'            : True,
                             'Fix_Stop'                 : True}}},

                'PARAMS':
                    {'Default Path'                     : 'save/params/default.params',
                    'DAT':
                        {'Query':
                            {'Time_Frame_in_Hours'      : 24,
                             'Red_Blue_or_All'          : 'All',
                             'Articles_Only'            : True},
                        'TFIDF_Params':
                            {'Use_IDF'                  : True,
                             'Normalize'                : False,
                             'Sublinear_TF'             : True,
                             'Smooth_IDF'               : False,
                             'Vocabulary'               : None,
                             'Min_DF'                   : False,
                             'Max_DF'                   : 0.6,
                             'Min_IC'                   : 0.0,
                             'Max_Terms'                : False,
                             'Column_to_Vectorize'      : 'chunks_ents'},
                        'Decomposition_Params':
                            {'Number_of_Topics'         : 10,
                             'Model_Type'               : 'nmf'},
                        'Visualizer':
                            {'Top_Terms_Per_Topic'      : 10,
                             'Sort_Terms_By'            : 'seriation',
                             'Depth_of_Termite_Plot'    : 50,
                             'Highlight'                : [0, 1, 2, 3, 4, 5],
                             'Save'                     : True,
                             'Save_Directory'           : '/Plots'}}},

                'SCRAPERLOG':
                    {'Default Path'                     : 'log/scraper.log',
                    'DAT':
                        {'SCRAPERLOG':
                            {'Date'                     : '',
                            'Scraper_Timer'             : '',
                            'Article_Count'             : '',
                            'Invalid_Links'             : '',
                            'Failed_Links_Count'        : '',
                            'Failed_Links'              : '',
                            'Red_Sub_Count'             : '',
                            'Blue_Sub_Count'            : '',}}},

                'MONGOLOG':
                    {'Default Path'                     : 'log/mongo.log',
                    'DAT':
                        {'MONGOLOG':
                            {'Date'                     : '',
                            'Added'                     : '',
                            'Total'                     : '',}}}}