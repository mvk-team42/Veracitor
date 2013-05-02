# search.py
# ===========
# Defines tasks for searching.

try:
    from veracitor.tasks.tasks import taskmgr
except:
    from tasks import taskmgr

from ..database import *

from celery.utils.log import get_task_logger


logger = get_task_logger(__name__)

@taskmgr.task
def get_producers(name, type_of):
    res = extractor.search_producers(possible_prod=name,
                                     type_of=type_of)
    logger.info('res: %s', str(res))

    if res:
        producers = []
        for r in res:
            source_ratings = [{'name' : s.source.name,
                               'tag' : s.tag.name,
                               'rating': s.rating }
                              for s in r.source_ratings]
            producers.append({'name' : r.name,
                              'description' : r.description,
                              'url' : r.url,
                              'type_of' : r.type_of,
                              'source_ratings' : source_ratings})

        return {
            'data': producers
        }
    else:
        return {}
