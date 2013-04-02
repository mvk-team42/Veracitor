# tasks - a package for celery tasks
# authors : Anton Erholt - <antonaut@github>

from celery import Celery, task

celery = Celery('veracitor.tasks','mogodb://localhost')

@task
def add(a, b):
    return a + b