# start_celerybeat.py
# ===============
# Starts the celery scheduling server


def start_celerybeat():
    """Starts the celery scheduling server in a subprocess."""
    import subprocess
    subprocess.call(['celerybeat',
                     '-A',
                     'veracitor.tasks.tasks.taskmgr'])

if __name__ == "__main__":
    start_celerybeat()