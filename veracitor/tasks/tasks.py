# tasks.py - used to load up celery
# authors : Anton Erholt - <antonaut@github>


from __future__ import absolute_import

from celery import Celery

app = Celery('veracitor.tasks.celery',
                broker='mongodb://localhost',
                include=['veracitor.tasks.crawler'])

# Optional configuration, see the application user guide.
# celery.conf.update(
#     CELERY_TASK_RESULT_EXPIRES=3600,
#)                              

if __name__ == '__main__':
    celery.start()
