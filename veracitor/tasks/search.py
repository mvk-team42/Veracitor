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
        producers = []
        for r in res:
            producers.append({'name' : r.name,
                              'description' : r.description,
                              'url' : r.url,
                              'type_of' : r.type_of,
                              'source_ratings' : r.source_ratings})

        return {
            'data': producers
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
            'data' : [extractor.entity_to_dict(i) for i in res]
            }
    else:
        return {}
