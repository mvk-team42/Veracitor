# start_celery.py
# ===============
# Starts the celery worker server

def start_celery():
    """Starts the celery worker server in a subprocess."""
    import subprocess
    subprocess.call(['celery',
                     '-A',
                     'veracitor.tasks.tasks.taskmgr',
                     'worker'])

if __name__ == "__main__":
    start_celery()