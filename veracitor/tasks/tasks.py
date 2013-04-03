# tasks.py - used to load up celery
# authors : Anton Erholt - <antonaut@github>


from __future__ import absolute_import

from celery import Celery

app = Celery('veracitor.tasks.celery',
             broker='mongodb://localhost',
             include=['veracitor.tasks.crawler'])

# Celery configuration.
# @see http://docs.celeryproject.org/en/latest/configuration.html
# for mor information.
celery.conf.update(
    CELERY_TASK_RESULT_EXPIRES=3600,
    CELERY_RESULT_BACKEND = "mongodb",
    CELERY_MONGODB_BACKEND_SETTINGS = {
        "host": "localhost",
        "port": 30000,
        "database": "celery_db",
        "taskmeta_collection": "veracitor_taskmeta_collection",
    }
)

if __name__ == '__main__':
    celery.start()
