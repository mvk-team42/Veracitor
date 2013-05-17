# general.py
# by <aerholt@kth.se>

try:
    from veracitor.tasks.tasks import taskmgr
except:
    from tasks import taskmgr


from veracitor.database import *

@taskmgr.task
def get_producer_name_from_url(url):
    pass
