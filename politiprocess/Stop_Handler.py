import re

import spacy
from spacy.lang.en.stop_words import STOP_WORDS

class Stop_Handler:

    def __init__(self, settings=None):
        self.settings = settings
        self.vocab_dict = None
        self.vocab_list = None

    def load(self, file='dat/stop.words'):
        '''A loader for loading a unicode file of stop words as dictionaries.
        Keys are categories and Values are lists of terms'''
        
        vocab_dict = {}
        vocab_list = []
        current_key = ""
    
        with open(file, mode='r') as fileObj:
        
            for line in fileObj.read().split('\n'):
                
                if not line:
                    continue
                    
                if "#" in line:
                    vocab_list = []
                    vocab_dict[line] = []
                    current_key = str(line)
                
                if line[0].isalpha():
                    vocab_list.append(line)
                
                vocab_dict[current_key] = vocab_list
                
            
            vocab_list = []
            for terms in vocab_dict.values():
                vocab_list.extend(terms)
            print(f"Loading {len(vocab_list)} stop words from {list(vocab_dict.keys())}")
        
        self.vocab_dict = vocab_dict
        self.vocab_list = vocab_list
    
    def fix(self, upper=True, no_punct=True):
        
        '''Reads and parses Stop_Handler stop words adding upper and no_punt versions. 
        (if upper) adds capitalized version of stop words
        (if no_punct) adds unpunctuated version of stop words'''

        for key in self.vocab_dict:
            if no_punct or upper:
                for word in self.vocab_dict[key]:
                    if no_punct:
                        word_punct = re.sub('[^A-Za-z0-9]+', '', word)
                        if word_punct not in self.vocab_dict[key]:
                            self.vocab_dict[key].append(word_punct)
                    
                    if upper:
                        word_caps = word.capitalize()
                        if word_caps not in self.vocab_dict[key]:
                            self.vocab_dict[key].append(word_caps)
        
           
            sorted(self.vocab_dict[key], key=str.lower)
            self.vocab_dict[key] = sorted(self.vocab_dict[key], key=str.lower)
            
    def save(self, file):
        with open(file, mode='w+')as writer:
        
            for key in self.vocab_dict:
                writer.writelines('\n' + key + '\n')
                for word in self.vocab_dict[key]:
                    writer.writelines(word  + '\n')
    
    def spacy_adder(self, model='en'):

        if not 'nlp' in globals():
            print(f"Loading Spacy Model {model}.  This could take a while...")
            global nlp
            nlp = spacy.load(model)
            print("Complete")
        
        for stopword in self.vocab_list:
            STOP_WORDS.add(stopword)
            
        nlp.vocab.add_flag(lambda s: s.lower() in spacy.lang.en.stop_words.STOP_WORDS, spacy.attrs.IS_STOP)
        print(f"Complete. There are {len(self.vocab_list)} stop words in the list.")