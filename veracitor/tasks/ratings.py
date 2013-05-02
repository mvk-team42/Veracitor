# ratings.py
# ===========
# Defines tasks for ratings.
try:
    from veracitor.tasks.tasks import taskmgr
except:
    from tasks import taskmgr

from ..database import *

from celery.utils.log import get_task_logger


logger = get_task_logger(__name__)

@taskmgr.task
def get_user(user_id):
    res = extractor.get_user(user_id)
    logger.info('res: %s', str(res))

    if res:
        return {
            'data': res
        }
    else:
        return {}

@taskmgr.task
def get_information_objects(tag):
    #Använda denna med possible_info = tom sträng
    # för att matcha alla med viss tag?
    # Och den tar emot tag-objekt fortfarande, eller strings? dokumentation antyder objekt..
    #res = extractor.get_informations()

def get_information_object(possible_info, tag):
    # Samma här. sök efter info-objekt. behövs
    # tag-objekt?
    #res = extractor.get_informations()
    
