# search.py
# ===========
# Defines tasks for searching.

try:
    from veracitor.tasks.tasks import taskmgr
except:
    from tasks import taskmgr

from ..database import *

from celery.utils.log import get_task_logger

import datetime

logger = get_task_logger(__name__)

@taskmgr.task
def get_producers(name, type_of):
    res = extractor.search_producers(possible_prod=name,
                                     type_of=type_of)
    logger.info('res: %s', str(res))

    if res:
        return {
            'data': {
                'producers': [ extractor.entity_to_dict(p) for p in res ]
             },
            'template_url': 'tabs/search_results.html'
        }
    else:
        return {}

@taskmgr.task
def get_information(title_part, tags,
                    startD=None,
                    endD=None):

    res = extractor.search_informations(title_part, tags, startD, endD)
    
    logger.info('res: %s', str(res))

    if res:
        return {
            'data' : {
                "information" : [extractor.entity_to_dict(i) for i in res]
                },
            'template_url':'tabs/search_results.html',
            }
    else:
        return {}
