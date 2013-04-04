# jobs.py
# =======
# Defines job handling via a RESTful api and some utility functions

from flask import request, redirect, url_for, render_template
from veracitor.web import app

import veracitor.tasks.crawler as crawler
import simplejson as json

@app.route('/scrape_article', methods=['GET','POST'])
def scrape_article():
    
    if request.method == 'POST':
        if not request.form:
            return error_tojson("Unable to parse request data.")
        try:
            url = request.form['url']
        except KeyError:
            return error_tojson("Unable to retrieve the url.")

        res = crawler.scrape_article.delay(url)
        store_job_result(res)

        raise TypeError
    else:
        return redirect(url_for('index'))


def error_tojson(err_msg):
    """Returns an error json-object."""
    return json.dumps({"error": err_msg})


def store_job(result):
    if not hasattr(app, 'results'):
        app.results = {}
    if not hasattr(app, 'current_number_of_jobs'):
        app.current_number_of_jobs = 0
    app.results[result.id] = result

    # Here you could add the job id to the session object if the user
    # is logged in.

    app.current_number_of_jobs += 1

@app.route("/job_ids")
def get_job_ids():
    try:
        keys = app.results.keys()
    except AttributeError:
        keys = []

    return json.dumps({"error": "",
                       "data": keys})
    
@app.route("/job_state/<job_id>")
def get_job_state(job_id):
    try:
        return json.dumps({"error": "",
                           "data": str(app.results[job_id].state)})
    except:
        return error_tojson("No job with that id.")

@app.route("/job_result/<job_id>")
def get_job_result(job_id):
    try:
        res = app.results[job_id]
    except:
        return error_tojson("No job with that id.")
    
    if not res.ready():
        return error_tojson("Job not ready.")
    else:
        return json.dumps({"error": "",
                           "data": res.result})
