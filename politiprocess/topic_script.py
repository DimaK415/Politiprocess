import argparse

from Paramerator import Parameters
from Mongo import Connect
from Topic_Modeler import Topic_Modeler

parser = argparse.ArgumentParser(description='Settings for scraper_script')
parser.add_argument('-v', '--verbose', help='Use for verbose output to console.', action='store_true')
parser.add_argument('-sl', '--set_local', help='Use for setting local time.', action='store_true')

args = parser.parse_args()

verbose = args.verbose
set_local = args.set_local

p = Parameters()

p.loader('save/params/default.params', 'params')
p.loader('dat/scraper.cfg', 'scraper')

connection = Connect(settings=p.params, mongo_cfg=p.scraper)

connection.query()

red_topics = Topic_Modeler(connection.red_df, p.params)
red_topics.topic_modeler(set_local=set_local, verbose=verbose)
red_topics.visualizer(set_local=set_local)

blue_topics = Topic_Modeler(connection.blue_df, p.params)
blue_topics.topic_modeler(set_local=set_local, verbose=verbose)
blue_topics.visualizer(set_local=set_local)