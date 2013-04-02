# tasks - a package for celery tasks
# authors : Anton Erholt - <antonaut@github>

celery = Celery('veracitor.tasks','mogodb://localhost')

@task
def add(a, b):
    return a + b