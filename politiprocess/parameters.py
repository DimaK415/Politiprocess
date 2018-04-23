from ast import literal_eval
from collections import namedtuple, OrderedDict
from pathlib import Path

class Parameters:

    def __init__(self, stop=True, from_file=True, verbose=False):
        
        from Defaults import Default_dict as dd
        
        self.dd         = dd
        self.params     = self.param_loader(dd['Params']['Default Path'])
        self.mongo      = self.param_loader(dd['Mongo']['Default Path'])
        
            
    def param_writer(self, file, params, default_location= True, overwrite=False):
        '''A writer definition for writing new param files and overwriting old ones.  USE WITH CAUTION!'''
        
        from pathlib import Path
        
        if Path(file).is_file():
            overwrite = literal_eval(input(f'{file} already exists. Overwrite?  :'))
            if overwrite:
                pass
            else:
                file = input('/path/to/new.file :')

        writer = open(file, mode='w+')
        
        for key in params:
            writer.writelines('\n' + '{}'.format(key) + '\n')
            for value in params[key]:
                
                writer.writelines('{:30}{}{}'.format(value, '= ', params[key][value]) + '\n')
        print(f"Completed writing {list(params.keys())} to '{file}'.")
    
    def param_loader(self, file):
        '''A loader definition for loading script dependant parameters from file'''
        
        self.file = file
        
        from pathlib import Path
        
        if not Path(file).is_file():
            response = literal_eval(input(f'"{file}" not found.  Would you like to attempt to generate a default?'))
            if response:
                for key in self.dd:
                    if self.dd[key]['Default Path'] == file:
                        response = literal_eval(input(f'Found Default "{file}". Generate?'))
                        if response:
                            dft_dict = self.dd[key]['DAT']
                            self.param_writer(file, dft_dict)
            
            else:
                pass
        
        fileObj = open(file, mode='r')
            
        params_dict  = OrderedDict()
        
        for line in fileObj:
            if not line:
                pass
            line = line.strip()
            key_value = line.split('=')
    
            if "#" in line:
                section = line[3:].replace(" ", "")
                params_dict[section] = {}

            if len(key_value) == 2:
                key = key_value[0].strip().replace(" ", "")
                value = key_value[1].strip()
 
                if not value:
                    value = input(f'Required parameter "{key_value[0].strip()}" is missing: ')
                    while not value:
                        value = input(f'You must enter a value for {key_value[0].strip()}: ')
                    
                
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
        
        param_nt = namedtuple('params', params_dict.keys())(**params_dict)
        return param_nt