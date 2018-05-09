import os
import pytz

def utc_to_pacific(self, utc_dt):
    local_tz = pytz.timezone('America/Los_Angeles')
    os.environ['TZ'] = 'America/Los_Angeles'
    local_dt = utc_dt.replace(tzinfo=pytz.utc).astimezone(local_tz)
    return local_tz.normalize(local_dt)