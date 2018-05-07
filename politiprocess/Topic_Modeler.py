import os
from collections import OrderedDict
from datetime import datetime
import pytz
import json
import textacy

class Topic_Modeler:

    def __init__ (self, df, settings):
        self.settings   = settings
        self.df         = df

    def utc_to_pacific(self, utc_dt):
        local_tz = pytz.timezone('America/Los_Angeles')
        os.environ['TZ'] = 'America/Los_Angeles'
        local_dt = utc_dt.replace(tzinfo=pytz.utc).astimezone(local_tz)
        return local_tz.normalize(local_dt)

    def topic_modeler(self, save=True, set_local = False, visualize=True, weighting = None, 
                    normalize = None, sublinear_tf = None, smooth_idf = None, vocabulary = None,
                    min_df = None, max_df = None, min_ic = None, max_n_terms = None, verbose=False):

        if verbose:
            print(f"Loading Vectorizer Paramaters")
        
        
        # Query
        if self.settings.Query.Count:
            label = str(self.settings.Query.Count) + '_cnt'
        else:
            label = str(self.settings.Query.Time_Frame_in_Hours) + '_hrs'

        red_or_blue = self.df.name
        
        # Vectorizer Params
        tf_type             = self.settings.TFIDF_Params.TF_Type
        apply_idf           = self.settings.TFIDF_Params.Apply_IDF
        idf_type            = self.settings.TFIDF_Params.IDF_Type
        apply_dl            = self.settings.TFIDF_Params.Apply_DL
        dl_type             = self.settings.TFIDF_Params.DL_Type
        norm                = self.settings.TFIDF_Params.Norm
        min_df              = self.settings.TFIDF_Params.Min_DF
        max_df              = self.settings.TFIDF_Params.Max_DF
        max_n_terms         = self.settings.TFIDF_Params.Max_N_Terms
        vocabulary_terms    = self.settings.TFIDF_Params.Vocabulary_Terms
        columns             = self.settings.TFIDF_Params.Columns_to_Vectorize
    
        # Decomposition Params
        n_topics          = self.settings.Decomposition_Params.Number_of_Topics
        model_type        = self.settings.Decomposition_Params.Model_Type
        
        self.vectorizer = textacy.vsm.Vectorizer(tf_type, apply_idf, idf_type, apply_dl,
                                            dl_type, norm, min_df, max_df,
                                            max_n_terms, vocabulary_terms)

        if verbose:
            print(f"Fitting Vectorizor on {columns} column(s)")
        
        self.doc_term_matrix = self.vectorizer.fit_transform(self.df.spacy_chunks)
        
        self.model = textacy.tm.TopicModel(model_type, n_topics=n_topics)
        self.model.fit(self.doc_term_matrix)

        if set_local:
            time_stamp = str(self.utc_to_pacific(datetime.now()).strftime('%m_%d_%y_%H_%M'))
        else:
            time_stamp = str(datetime.now().strftime('%m_%d_%y_%H_%M'))
        
        save_columns = ""
        for column in columns:
            save_columns += column
    
        json_save = f"save/json/{label}_{red_or_blue}_{time_stamp}.json"        
        
        x = self.model.top_topic_terms(self.vectorizer.id_to_term, top_n=10, weights=True)

        topic_list = []
        for y in x:
            topic_list.append(y[1])
        
        topic_list.sort(key=lambda dic: dic[0][1], reverse=True)
        
        topic_dict = OrderedDict()
        for i, group in enumerate(topic_list):
            
            temp_list = []
            for term in group:
                temp_dict = OrderedDict()
                temp_dict['term']  = term[0]
                temp_dict['score'] = term[1]
                temp_list.append(temp_dict)
    
            topic_dict[f'topic {i+1}'] = temp_list
        
        with open(json_save, 'w') as fp:
            json.dump(topic_dict, fp, indent=1)
        

    def visualizer(self, set_local=False):

        if self.settings.Query.Count:
            label = str(self.settings.Query.Count) + '_cnt'
        else:
            label = str(self.settings.Query.Time_Frame_in_Hours) + '_hrs'

        red_or_blue = self.df.name

        sort_terms_by       = self.settings.Visualizer.Sort_Terms_By
        term_depth          = self.settings.Visualizer.Depth_of_Termite_Plot
        highlight           = self.settings.Visualizer.Highlight
        columns             = self.settings.TFIDF_Params.Columns_to_Vectorize

        save_columns = ""
        for column in columns:
            save_columns += column

        if set_local:
            time_stamp = str(self.utc_to_pacific(datetime.now()).strftime('%m_%d_%y_%H_%M'))
        else:
            time_stamp = str(datetime.now().strftime('%m_%d_%y_%H_%M'))

        self.save = f"save/plots/{label}_{red_or_blue}_{time_stamp}.png"
        
        self.model.termite_plot(self.doc_term_matrix, self.vectorizer.id_to_term, highlight_topics=highlight,
                       topics=-1,  n_terms=term_depth, sort_terms_by=sort_terms_by, save=self.save)