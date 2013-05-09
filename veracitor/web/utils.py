

from json import JSONEncoder
from bson.json_util import default

from veracitor.web import app
from veracitor.database import *

from flask import Flask, render_template, request, redirect, url_for, jsonify, session, abort

log = app.logger.debug

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

    try:
        source_ratings = []
        for s in user_obj.source_ratings.keys():
            for tag in user_obj.source_ratings[s]:
                source_ratings.append({
                        'name' : s,
                        'tag' : tag,
                        'rating': user_obj.source_ratings[s][tag] ,
                        'description': extractor.get_producer(__safe_string(s)).description})  
                        
        info_ratings = []
        for iurl in user_obj.info_ratings.keys():
            info_ratings.append({
                    'title': extractor.get_information(__safe_string(iurl)).title,
                    'rating': user_obj.info_ratings[iurl],
                    'url': iurl,
                    })
            
            
        groups = [{'name' : g.name,
                   'description' : g.description,
                   'producers' : [pname for pname in g.producers.keys()]}
                  for g in user_obj.groups]
        
        
        user_dict = {'name' : user_obj.name,
                     'description' : user_obj.description,
                     'type_of' : user_obj.type_of,
                     'source_ratings' : source_ratings,
                     'groups' : groups,
                     'group_ratings' : user_obj.group_ratings,
                     'info_ratings' : info_ratings}
        
        return user_dict
    except Exception, e:
        log(e)
        return ""

@app.route('/utils/get_user', methods=['GET', 'POST'])
def get_user():
    """
    Extracts a user from the database and returns it. Only use when you KNOW
    the name of the user, and that it exists.

    """
    return jsonify(extractor.entity_to_dict(extractor.get_user(request.form["user_name"])));
    
def __safe_string(url):
    return url.replace("|", ".")

    
