import numpy as np
import textacy
import spacy

from Stop_Handler import Stop_Handler


class Processing:
    def __init__(self, settings):
        self.settings = settings

    def pre_processor(self, df, column='text', new_column_name='cleaned'):
    
        preprocessing = self.settings.Pre_Processing
        
        df[column].replace(np.nan, '', inplace=True)
        
        cleaned = [] 
        for x in range(len(df)):
            text = textacy.preprocess.preprocess_text(df[column][x],
                                                 fix_unicode          = preprocessing.Fix_Unicode,
                                                 lowercase            = preprocessing.All_Lowercase,
                                                 no_punct             = preprocessing.Remove_Punctuation,
                                                 no_contractions      = preprocessing.Remove_Contradictions,
                                                 no_currency_symbols  = preprocessing.Replace_Currency,
                                                 no_emails            = preprocessing.Remove_Emails,
                                                 no_accents           = preprocessing.Remove_Accents)
            if preprocessing.Remove_Newline:
                text = text.replace('\n', ' ')
            
            cleaned.append(text)
        
        df[new_column_name] = cleaned
    
    def spacy_processor(self, df, spacy_model=None, use_cleaned=None, named_entities=None,
                                split_columns=None, min_word_length=None, 
                                fix_stop=None, verbose=False):

        spacy_params = self.settings.Spacy_Params

        if not spacy_model:
            spacy_model         = spacy_params.Spacy_Model
        if not use_cleaned:
            use_cleaned         = spacy_params.Use_Cleaned_Text
        if not named_entities: 
            named_entities      = spacy_params.Named_Entity_List
        if not split_columns:   
            split_columns       = spacy_params.Split_Columns
        if not min_word_length:
            min_word_length     = spacy_params.Min_Word_Length
        if not fix_stop:
            fix_stop            = spacy_params.Fix_Stop

        if use_cleaned:
            corpus    = 'cleaned'
            df_column = 'cleaned'
        else:
            corpus    = 'raw'
            df_column = 'text'   
        
        if verbose:
            print(f'''Filtering stops and words shorter than {min_word_length + 1} letters. 
Chunking and identifying {named_entities} entities from {corpus} corpus.''')    
        
        if 'nlp' not in globals():
            if verbose:
                print(f"Loading Spacy Model {spacy_model}.  This could take a while...")
            global nlp
            nlp = spacy.load(spacy_model)
            if verbose:
                print("Complete")  

        if fix_stop:
            stop = Stop_Handler()
            stop.load()
            stop.spacy_adder(spacy_model)

        chunks_list = []
        ents_list   = []
        
        for text in df[df_column]:
            
            doc = nlp(str(text))
            
            chunks = []
            ents   = []
            
            for span in doc.noun_chunks:
                if len(span) == 1:
                    if span[0].is_stop or len(span[0]) <= min_word_length:
                        continue
                    else:
                        chunks.append(span.text)
                        continue
                else:
                    chunks.append(span.text)
            
            for ent in doc.ents:
                if ent.label_ in named_entities:
                    ents.append(ent.text)
                    
            chunks_list.append(chunks)
            ents_list.append(ents)
        
        if split_columns:
            df['spacy_chunks'], df['spacy_ents'] = chunks_list, ents_list
            del chunks_list, ents_list
            if verbose:
                print(f'''Done inserting {len(df.spacy_chunks.sum())} chunks and
                  {len(df.spacy_ents.sum())} entities into df.chunks and df.ents.''')
        else:
            joined_list = [a + b for a, b in zip(chunks_list, ents_list)]
            del chunks_list, ents_list
            df['spacy_chunks_ents'] = joined_list
            del joined_list
            if verbose:
                print(f"Done inserting {len(df.spacy_chunks_ents.sum())} chunks and entities into df.chunks_ents.)")    