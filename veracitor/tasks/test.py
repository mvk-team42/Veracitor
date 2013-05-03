
try:
    from veracitor.tasks.tasks import taskmgr
except:    
    from tasks import taskmgr

@taskmgr.task
def mkawesome():
    res = {'data': {'age': 23, 'name': 'Anton'}, 'template_url': 'awesome.html'}
    import time
    time.sleep(4)
    return res
