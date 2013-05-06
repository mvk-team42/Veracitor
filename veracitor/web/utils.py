

from json import JSONEncoder
from bson.json_util import default

from veracitor.database import extractor
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

    source_ratings = []
    for s in user_obj.source_ratings.keys():
        for tag in s.keys():
            source_ratings.append({
                    'name' : s,
                    'tag' : tag,
                    'rating': s[tag] ,
                    'description': extractor.get_producer(s).description})

    info_ratings = []
    for iurl in user_obj.info_ratings.keys():
        info_ratings.append({
                'title': extractor.get_information(iurl).title,
                'rating': user_obj.info_ratings[iurl],
                'url': iurl,
                })

    groups = [{'name' : g,
               'description' : extractor.get_group(g).description,
               'producers' : [p.name for p in extractor.get_group(g).producers],
               'rating' : user_obj.groups_ratings[g]}
              for g in user_obj.groups.keys()]

    user_dict = {'name' : user_obj.name,
                'description' : user_obj.description,
                'type_of' : user_obj.type_of,
                'source_ratings' : source_ratings,
                'groups' : groups,
                'group_ratings' : [{'group':gr.group, 'rating':gr.rating}
                                   for gr in user_obj.group_ratings],
                'info_ratings' : info_ratings}

    return user_dict
