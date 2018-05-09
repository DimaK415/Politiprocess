import argparse
import glob
import os
import json
import pytz
from datetime import datetime

from Mongo import Connect
from Paramerator import Parameters

parser = argparse.ArgumentParser(description='Settings for scraper_script')
parser.add_argument('-v', '--verbose', help='Use for verbose output to console.', action='store_true')
parser.add_argument('-sl', '--set_local', help='Use for setting local time.', action='store_true')

args = parser.parse_args()

verbose = args.verbose
set_local = args.set_local

def utc_to_pacific(self, utc_dt):
    local_tz = pytz.timezone('America/Los_Angeles')
    os.environ['TZ'] = 'America/Los_Angeles'
    local_dt = utc_dt.replace(tzinfo=pytz.utc).astimezone(local_tz)
    return local_tz.normalize(local_dt)


list_of_files = glob.glob('save/json/*')
list_of_files.sort(key=os.path.getctime, reverse=True)
list_of_files = list_of_files[:4]

list_of_terms = []
for file in list_of_files:
    term_dict = json.load(open(file, "r"))
    json.load(open(file, "r"))
    term_dict['timestamp'] = datetime.fromtimestamp(os.path.getctime(file))

    if "Blue" in file:
        term_dict['color'] = "Blue"
    else:
        term_dict['color'] = "Red"
    list_of_terms.append(term_dict)

mongo = Connect()
client = mongo.client

collection = client.Politiprocess.terms

start_count = collection.count()

for entry in list_of_terms:
    client.Politiprocess.terms.update_one({"timestamp": entry['timestamp']},{'$set': entry},
                                          upsert=True, bypass_document_validation=True)

end_count = collection.count()

added_count = end_count - start_count

if set_local:
    time_now = datetime.ctime(utc_to_pacific(datetime.now()))
else:
    time_now = datetime.ctime(datetime.now())


log = Parameters()
log.loader('log/JSON.log', default=True)

log.loaded.JSONLOG.Date    = time_now
log.loaded.JSONLOG.Added   = added_count
log.loaded.JSONLOG.Total   = end_count

log.writer('log/scraper.log', log.loaded, append=True)