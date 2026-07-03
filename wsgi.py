# wsgi.py — Entry point untuk PythonAnywhere WSGI server
# Di PythonAnywhere, set "Source code" ke direktori ini
# dan "WSGI configuration file" menunjuk ke file ini.

import sys
import os

# Tambahkan direktori proyek ke path Python
project_home = os.path.dirname(os.path.abspath(__file__))
if project_home not in sys.path:
    sys.path.insert(0, project_home)

from app import app as application  # noqa
