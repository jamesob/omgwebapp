
import os

# Are we in a dev environment?
DEV = os.environ.get('DEV')
PORT = int(os.environ.get('PORT', 7082))
DB_URL = os.environ.get('DB_URL') or 'sqliteext:///changeme.db'

# Webpack builds the JS and drops it into this folder.
STATIC_PATH = os.environ.get('STATIC_PATH', '/build')

# Images and stuff are in here.
ASSETS_PATH = os.environ.get('ASSETS_PATH', '/assets')
