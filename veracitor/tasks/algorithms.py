# algorithms.py
# ===========
# Defines tasks for the algorithms.

try:
    from veracitor.tasks.tasks import taskmgr
except:
    from tasks import taskmgr

from ..algorithms.tidaltrust import compute_trust
from ..algorithms.sunny import sunny as sunny_algo
from ..database import networkModel as nm
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)

def _fail_dict(source, sink, tag):
    return {"trust": None,
            "threshold": None,
            "paths_used": [],
            "nodes_used": [],
            "nodes_unused": [],
            "source": source,
            "sink": sink,
            "tag": tag,}

@taskmgr.task
def sunny(source, sink, tag):
    source, sink, tag = _to_unicode((source, sink, tag))
    
    network = nm.get_global_network()
    
    try:
        trust = sunny_algo.sunny(network, source, sink, tag=tag)
        return trust

    except Exception as e:
        logger.info("Exception: "+str(e)+"\nMsg: "+e.message)
        
        return _fail_dict(source, sink, tag)
        

@taskmgr.task
def tidaltrust(source, sink, tag):
    # Convert input to unicode
    source = unicode(source)
    sink = unicode(sink)
    tag = unicode(tag)

    # Get global network
    network = nm.get_global_network()

    # Calc trust
    try:
        trust = compute_trust(network=network,
                              source=source,
                              sink=sink, tag=tag)
        return trust

    except KeyError as e:
        logger.info("Exception: "+str(e)+"\nMsg: "+e.message)
        
        return _fail_dict(source, sink, tag)

def _to_unicode(iterable):
    for el in iterable:
        el = unicode(el)
    return iterable
