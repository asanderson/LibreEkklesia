from django.tasks import task


@task
def ping():
    """Round-trip check for the task queue."""
    return "pong"
