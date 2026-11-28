"""Docker health check for the web container: the API answers on Gunicorn's port."""

import os
import urllib.request

host = os.environ["DJANGO_ALLOWED_HOSTS"].split(",")[0].strip()
request = urllib.request.Request("http://127.0.0.1:8000/api/health", headers={"Host": host})
with urllib.request.urlopen(request, timeout=5) as response:
    if response.status != 200:
        raise SystemExit(f"/api/health answered {response.status}")
