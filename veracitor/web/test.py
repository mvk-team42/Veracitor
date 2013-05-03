
from flask import request, redirect, url_for, render_template, abort, jsonify,\
    make_response
from veracitor.web import app
from veracitor.web.utils import store_job_result
from veracitor.tasks.test import mkawesome

@app.route('/test/jobs/awesome')
def awesome():
    res = mkawesome.delay()
    store_job_result(res)
    return jsonify(job_id=res.id)
    