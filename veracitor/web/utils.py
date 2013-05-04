

from json import JSONEncoder
from bson.json_util import default

from veracitor.web import app
from veracitor.database import extractor

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


def store_job_result(result):
    """Stores the job result in the app context."""
    if not hasattr(app, 'results'):
        app.results = {}
    if not hasattr(app, 'current_number_of_jobs'):
        app.current_number_of_jobs = 0
    app.results[result.id] = result

    # Here you could add the job id to the session object if the user
    # is logged in.

    app.current_number_of_jobs += 1

def get_user_as_dict(username):
    user_obj = extractor.get_user(username)
    
    source_ratings = [{'name' : s.source.name,
                       'tag' : s.tag.name,
                       'rating': s.rating }
                      for s in user_obj.source_ratings]
    
    info_ratings = [{'title':ir.information.title, 'rating':ir.rating}
                    for ir in user_obj.info_ratings]
    
    groups = [{'name' : g.name,
               'description' : g.description,
               'owner' : g.owner,
               'producers' : [p.name for p in g.producers]}
              for g in user_obj.groups]
    
    userDict = {'name' : user_obj.name,
                'description' : user_obj.description,
                'type_of' : user_obj.type_of,
                'source_ratings' : source_ratings,
                'groups' : groups,
                'group_ratings' : [{'group':gr.group, 'rating':gr.rating}
                                   for gr in user_obj.group_ratings],
                'info_ratings' : info_ratings}
    
    return userDict
