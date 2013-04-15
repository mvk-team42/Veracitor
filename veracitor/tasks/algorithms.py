# algorithms.py
# ===========
# Defines tasks for the algorithms.

try:
    from veracitor.tasks.tasks import taskmgr
except:    
    from tasks import taskmgr

from ..algorithms.tidaltrust import compute_trust
from ..database import globalNetwork as gn

@taskmgr.task
def sunny(source, sink, tag, network):
    pass

@taskmgr.task
def tidaltrust(source, sink, tag):
    network = gn.get_global_network()
    trust = compute_trust(network=network,
                          source=source,
                          sink=sink, tag=tag)
    return trust
