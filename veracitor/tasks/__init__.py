# tasks - a package for celery tasks
# authors : Anton Erholt - <antonaut@github>

from celery import Celery

celery = Celery('veracitor.tasks','mogodb://localhost')


if __name__=="__main__":

    @task
    def add(a, b):
        return a + b