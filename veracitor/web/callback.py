from flask import request, redirect, url_for, render_template
from veracitor.web import app

import veracitor.tasks.crawler as crawler

app.callback_id_counter = 0
app.callback_ids = {}


@app.route('/scrape_article', methods=['GET','POST'])
def scrape_article():
#    if request.method == 'POST':
    if not hasattr(app, 'results'):
        app.results = {}
    if not hasattr(app, 'current_job_id'):
        app.current_job_id = 0
    res = crawler.scrape_article.delay("http://www.dn.se/nyheter/varlden/nordkoreaexpert-varre-an-pa-mycket-lange")
    app.results[app.current_job_id] = res
    app.current_job_id += 1
    #return str(app.jobid - 1)
#    else:
#        return redirect(url_for("index"))
    raise TypeError

@app.route("/job_state/<job_id>")
def get_job_state(job_id):
    return str(app.results[job_id].state)

@app.route("/job_result/<job_id>")
def get_job_result(job_id):
    return app.results[job_id].result



"""
Returns a unique crawl procedure  id.
"""
def get_unique_id():
    id = '#' + str(app.callback_id_counter)
    app.callback_ids[id] = None

    app.callback_id_counter += 1
    return id

"""
Sets an item for the specified id.
"""
def set_item(id, item):
    app.callback_ids[id] = item

"""
Returns the item related to the given crawl procedure id.
If an item has been set the id is removed from the dict.
"""
def check_id(id):
    item = app.callback_ids[id]

    if item:
        del app.callback_ids[id]

    return item
