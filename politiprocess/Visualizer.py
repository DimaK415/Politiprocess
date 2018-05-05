import os
from datetime import datetime
import pytz
import textacy

class Visualizer:

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

        # for x in self.df['spacy_ents']:
        #     print(x)
    
        if verbose:
            print(f"Loading Vectorizer Paramaters")
        
        
        # Query
        n_hours     = self.settings.Query.Time_Frame_in_Hours
        red_or_blue = self.settings.Query.Red_Blue_or_All
        
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
    
        # Visualization Params
        # top_n_terms       = self.settings.Visualizer.Top_Terms_Per_Topic
        sort_terms_by     = self.settings.Visualizer.Sort_Terms_By
        term_depth        = self.settings.Visualizer.Depth_of_Termite_Plot
        highlight         = self.settings.Visualizer.Highlight
        directory         = self.settings.Visualizer.Save_Directory
    
        
        vectorizer = textacy.vsm.Vectorizer(tf_type, apply_idf, idf_type, apply_dl,
                                            dl_type, norm, min_df, max_df,
                                            max_n_terms, vocabulary_terms)
        
        # print(self.df[columns])

        if verbose:
            print(f"Fitting Vectorizor on {columns} column(s)")
        
        doc_term_matrix = vectorizer.fit_transform(self.df.spacy_ents)
        
        model = textacy.tm.TopicModel(model_type, n_topics=n_topics)
        model.fit(doc_term_matrix)
        
        # topics_string = ""
        
        # for topic_idx, top_terms in model.top_topic_terms(vectorizer.id_to_term, top_n=top_n_terms):
        #     topics_string += ' - '.join(top_terms) + ' '
        #     print('topic', topic_idx, ':', '   '.join(top_terms))
            
        if visualize:
            if set_local:
                time_stamp = str(self.utc_to_pacific(datetime.now()).strftime('%m_%d_%y_%H_%M'))
            else:
                time_stamp = str(datetime.now().strftime('%m_%d_%y_%H_%M'))

            save_columns = ""
            for column in columns:
                save_columns += column

            self.save = f"{directory}/{n_hours}hr_{red_or_blue}_{save_columns}_{time_stamp}"
            
            model.termite_plot(doc_term_matrix, vectorizer.id_to_term, highlight_topics=highlight,
                           topics=-1,  n_terms=term_depth, sort_terms_by=sort_terms_by, save=self.save)