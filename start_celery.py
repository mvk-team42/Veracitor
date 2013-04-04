# start_celery.py
# ===============
# Starts the celery worker server. This script also starts the celery
# beat daemon needed by mongodb to cleanup results.

def start_celery():
    """Starts the celery worker server in a subprocess."""
    import subprocess
    subprocess.call(['celery',
                     '-A',
                     'veracitor.tasks.tasks.taskmgr',
                     'worker',
                     '-B'])

if __name__ == "__main__":
    start_celery()