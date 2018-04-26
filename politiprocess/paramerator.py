from pathlib import Path
from ast import literal_eval
from recordclass import recordclass
from collections import namedtuple
from collections import OrderedDict

from dat import DEFAULTS


class parameters:
    '''Super awesome py module written by Dmitry Karpovich - I'll fill this in later'''

    def __init__(self, params=None):

        self.def_dict   = DEFAULTS.default_dict

    def writer(self, file, params, in_place=False):
        '''A writer definition for writing new param files and overwriting old ones.  USE WITH CAUTION!'''
        
        if Path(file).is_file() and not in_place:
            overwrite = literal_eval(input(f'{file} already exists. Overwrite?  :'))
            if overwrite:
                pass
            else:
                file = input('/path/to/new.file :')
        
        with open(file, mode='w+') as writer:
            
            if not isinstance(params, dict):
                params_dict = OrderedDict()
                for section in params._asdict():
                    params_dict[section] = params._asdict()[section]
                for param in params_dict:
                    params_dict[param] = params_dict[param]._asdict()
                params = params_dict
            
            for key in params:
                writer.writelines('\n##' + '{}'.format(key) + '\n')
                for value in params[key]:
                    
                    writer.writelines('{:30}{}{}'.format(value, '= ', params[key][value]) + '\n')
            print(f"Completed writing {list(params.keys())} to '{file}'.")
    
    def loader(self, file):
        '''A loader definition for loading script dependant parameters from file'''
        
        
        if not Path(file).is_file():
            response = literal_eval(input(f'"{file}" not found.  Generate from default?'))
            if response:
                found = False
                for key in self.def_dict:
                    if self.def_dict[key]['Default Path'] == file:
                        found = True
                        response = literal_eval(input(f'Found Default "{file}". Generate?'))
                        if response:
                            self.writer(file, self.def_dict[key]['DAT'])
                if not found:
                    raise FileNotFoundError(f"""No reference to '{file}' in 'dat/DEFAULTS.py'.
                                            Check the file path and name.""")
            else:
                print(f"'{file}' no file found or generated.")
                return
        
        params_dict = OrderedDict()
        user_input = False
        
        with open(file, mode='r') as fileObj:
        
            for line in fileObj:
                
                if not line:
                    continue
                line = line.strip()
                key_value = line.split('=')
                
                if "#" in line:
                    section = line[2:].replace(" ", "")
                    params_dict[section] = {}
    
                if len(key_value) == 2:
                    key = key_value[0].strip().replace(" ", "")
                    value = key_value[1].strip()
     
                    if value == '*':
                        value = input(f'Required parameter "{key_value[0].strip()}" is missing: ')
                        while not value:
                            value = input(f'You must enter a value for "{key_value[0].strip()}": ')
                        user_input = True
                    if "," in value:
                        try:
                            params_dict[section][key] = list(literal_eval(value))
                        except:
                            params_dict[section][key] = value.split(", ")
                    else:
                        try:
                            params_dict[section][key] = literal_eval(value)
                        except:
                            params_dict[section][key] = value
        
        for x in params_dict:
            params_dict[x] = recordclass('param', params_dict[x].keys())(**params_dict[x])
        
        param_nt = namedtuple('section', params_dict.keys())(**params_dict)
        
        if user_input:
            response = input(f"Would you like to save your input to the default file?")
            self.writer(file, param_nt, in_place=True)
        
        return param_nt
    
    def generate_defaults(self):
        '''Generate new new defualt files found in DEFAULTS.py'''
        
        file_list = []
        for x in self.def_dict:
            file_list.append(self.def_dict[x]['Default Path'])

        for x in file_list:
            self.loader(x)