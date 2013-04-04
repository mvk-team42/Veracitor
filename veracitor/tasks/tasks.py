# tasks.py
# author(s): Anton Erholt - <antonaut@github>
# ========
# Used to load up celery aswell as to define the taskmgr
# for the tasks.



from __future__ import absolute_import

from celery import Celery

taskmgr = Celery('veracitor.tasks.celery',
             broker='mongodb://localhost',
             include=['veracitor.tasks.crawler'])

# Celery configuration.
# @see http://docs.celeryproject.org/en/latest/configuration.html
# for more information.
taskmgr.conf.update(
    CELERY_TASK_RESULT_EXPIRES=3600,
    CELERY_RESULT_BACKEND = "mongodb",
    CELERY_MONGODB_BACKEND_SETTINGS = {
        "host": "localhost",
        "database": "celery_db",
        "taskmeta_collection": "veracitor_taskmeta_collection",
    }
)

if __name__ == '__main__':
    taskmgr.start()
