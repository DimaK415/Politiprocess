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
                            {'Set_Local'                : True,
                            'Upsert'                    : True},
                        'Reddit_Params':
                            {'Red_List'                 : ['conservative', 'republican'],
                            'Blue_List'                 : ['liberal', 'democrats'],
                            'Scraper_Depth_Limit'       : 10},
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
                             'Replace_Currency'         : True,
                             'Remove_Extras'            : True,
                             'Extras'                   : ['-', '·', '"', "'", '–', '..', '(', ')', '——', '—', '°', '[', ']', ':', ';', '_', '  ', '   ']},
                        'Spacy_Params':
                            {'Spacy_Model'              : 'en_core_web_lg',
                             'Min_Word_Length'          : 2,
                             'Use_Cleaned_Text'         : 1,
                             'Named_Entity_List'        : ['PERSON', 'GPE', 'ORG', 'NORP'],
                             'Split_Columns'            : True,
                             'Fix_Stop'                 : True}}},

                'PARAMS':
                    {'Default Path'                     : 'save/params/default.params',
                    'DAT':
                        {'Query':
                            {'Time_Frame_in_Hours'      : 0,
                             'Red_Blue_or_All'          : 'All',
                             'Articles_Only'            : True,
                             'Count'                    : 50,
                             'Append_DFs'               : False},
                        'TFIDF_Params':
                            {'TF_Type'                  : 'linear',
                             'Apply_IDF'                : True,
                             'IDF_Type'                 : 'smooth',
                             'Apply_DL'                 : False,
                             'DL_Type'                  : 'sqrt',
                             'Norm'                     : None,
                             'Min_DF'                   : 1,
                             'Max_DF'                   : .6,
                             'Max_N_Terms'              : None,
                             'Vocabulary_Terms'         : None,
                             'Columns_to_Vectorize'     : ['spacy_ents', 'spacy_chunks']},
                        'Decomposition_Params':
                            {'Number_of_Topics'         : 10,
                             'Model_Type'               : 'nmf'},
                        'Visualizer':
                            {'Top_Terms_Per_Topic'      : 10,
                             'Sort_Terms_By'            : 'seriation',
                             'Depth_of_Termite_Plot'    : 50,
                             'Highlight'                : [0, 1, 2, 3, 4, 5],
                             'Save'                     : True,
                             'Save_Directory'           : 'save/plots'}}},

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