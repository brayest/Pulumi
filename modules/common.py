import json
import datetime
from pygments import highlight, lexers, formatters

# A better map class
class MapCreate():
    def __init__(self):
        self._client = []

    def put(self, key, value):
        if ( not self.contains(key) ):
            self._client.append([key,value])
        else:
            raise ValueError('ERROR: Key already exsits on Map')

    def contains(self, key):
        for i in self._client:
            if ( key in i):
                return True
        return False

    def get(self, key):
        for i in self._client:
            if ( key in i):
                return i[1]

    def getKey(self, value):
        for i in self._client:
            if ( value in i):
                return i[0]

    def getMap(self):
        return self._client

    def printMap(self):
        print(self._client)

# Datetime format is unreadable for JSON, fix.
class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()
        elif isinstance(obj, datetime.date):
            return obj.isoformat()
        elif isinstance(obj, datetime.timedelta):
            return (datetime.datetime.min + obj).time().isoformat()
        else:
            return super(DateTimeEncoder, self).default(obj)

# Function to reformat AWS JSON output in order to be read
def get_json(json_format, display=False):
    output_json = json.dumps(json_format, cls=DateTimeEncoder, indent=4, sort_keys=True)
    if ( display ):
        print(output_json)
        return json.loads(output_json)
    else:
        return json.loads(output_json)

def str_to_bool(s):
    if s == 'True':
         return True
    elif s == 'False':
         return False
    else:
         raise ValueError # evil ValueError that doesn't tell you what the wrong value was
