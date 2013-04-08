# Celery configuration.
# @see http://docs.celeryproject.org/en/latest/configuration.html
# for more information.

### NOTE : Celery requires the celerybeat daemon to be running if the results should be
###        properly removed from the database.

BROKER_URL = u'mongodb://localhost:27017'

#CELERY_TASK_RESULT_EXPIRES = 1
CELERY_RESULT_BACKEND = "mongodb"

# Used to store task states and results
CELERY_MONGODB_BACKEND_SETTINGS = {
    "host": "localhost",
    "database": "celery_db",
#    "user":"admin",
#    "password":"default",
    "taskmeta_collection": "veracitor_taskmeta_collection",
}

