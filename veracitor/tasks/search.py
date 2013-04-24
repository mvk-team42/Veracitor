# search.py
# ===========
# Defines tasks for searching.

try:
    from veracitor.tasks.tasks import taskmgr
except:
    from tasks import taskmgr

from ..database import *

from flask import render_template
from celery.utils.log import get_task_logger


logger = get_task_logger(__name__)

@taskmgr.task
def get_producers(name, type_of):
    res = extractor.search_producers(possible_prod=name,
                                     type_of=type_of)
    logger.info('res: %s', str(res))

    html = render_template('tabs/search_results.html', data=res)

    if res:
        return {
            'html': html
        }
    else:
        return {}
