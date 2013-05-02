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
def get_user(name):
    res = extractor.get_user(name)
    logger.info('res: %s', str(res))

    if res:
        return {
            'data': res
        }
    else:
        return {}
