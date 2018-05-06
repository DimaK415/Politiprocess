import argparse

from Paramerator import Parameters
from Mongo import Connect
from Scraper import Scraper
from Processing import Processing

parser = argparse.ArgumentParser(description='Settings for scraper_script')
parser.add_argument('-v', '--verbose', help='Use for verbose output to console.', action='store_true')
parser.add_argument('-sl', '--set_local', help='Use for setting local time.', action='store_true')

args = parser.parse_args()

verbose = args.verbose
set_local = args.set_local

p = Parameters()

p.loader('save/params/default.params', 'params')
p.loader('dat/scraper.cfg', 'scraper')

scraper = Scraper(p.scraper)

scraper.run(verbose=verbose, set_local=set_local)

processor = Processing(p.scraper)

processor.pre_processor(scraper.scraper_df)

processor.spacy_processor(scraper.scraper_df, verbose=verbose)

connection = Connect(settings=p.params, mongo_cfg=p.scraper)

connection.update_from_df(scraper.scraper_df, verbose=verbose, set_local=set_local)