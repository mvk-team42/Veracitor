from json import JSONEncoder
from bson.json_util import default

class JSONEnc(JSONEncoder):

    def default(self, o):
        try:
            d = o.__dict__
        except:
            pass
        else:
            return d
        # Let the base class default method raise the TypeError
        return JSONEncoder.default(self, o)
