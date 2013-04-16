# algorithms.py
# ===========
# Defines tasks for the algorithms.

try:
    from veracitor.tasks.tasks import taskmgr
except:    
    from tasks import taskmgr

from ..database import *


@taskmgr.task
def get_producers(name, type_of):
    res = extractor.search_producers(possible_prod=f['name'],
                                     type_of=f['type'])
    if res:
        return res
    else:
        return {}

    