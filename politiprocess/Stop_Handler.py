import re

def loader(file='dat/stop.words', as_list=True):
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
            
        if as_list:
            vocab_list = []
            for terms in vocab_dict.values():
                vocab_list.extend(terms)
            print(f"Loading {len(vocab_list)} stop words from {list(vocab_dict.keys())}")
            return vocab_list
    return vocab_dict

def fixer(file, upper=True, no_punct=True, fix_in_place=False):
    
    '''Reads and parses *file* - Returns list of stops or (if fix_in_place) overwrites existing *file*
    (if upper) adds capitalized version of stop words
    (if no_punct) adds unpunctuated version of stop words'''
    
    vocab_dict = loader('dat/stop.words', as_list = False)
    
    for key in vocab_dict:
        if no_punct or upper:
            print(key)
            for word in vocab_dict[key]:
                if no_punct:
                    word_punct = re.sub('[^A-Za-z0-9]+', '', word)
                    if word_punct not in vocab_dict[key]:
                        vocab_dict[key].append(word_punct)
                
                if upper:
                    word_caps = word.capitalize()
                    if word_caps not in vocab_dict[key]:
                        vocab_dict[key].append(word_caps)
    
       
        sorted(vocab_dict[key], key=str.lower)
        vocab_dict[key] = sorted(vocab_dict[key], key=str.lower)
        
    if fix_in_place:
        
        with open(file, mode='w+')as writer:
        
            for key in vocab_dict:
                writer.writelines('\n' + key + '\n')
                for word in vocab_dict[key]:
                    writer.writelines(word  + '\n')
    else:       
        return vocab_dict

def spacy_adder():
    print(f"Adding {len(stop_words_list)} custom stop words to Spacy Model {spacy_model}.")
    
    if not 'nlp' in globals():
        print(f"Loading Spacy Model {spacy_model}.  This could take a while...")
        global nlp
        nlp = spacy.load(spacy_model)
        print("Complete")
    
    for stopword in tqdm(stop_words_list):
        STOP_WORDS.add(stopword)
        
    nlp.vocab.add_flag(lambda s: s.lower() in spacy.lang.en.stop_words.STOP_WORDS, spacy.attrs.IS_STOP)
    print(f"Complete. There are {len(STOP_WORDS)} stop words in the list.")