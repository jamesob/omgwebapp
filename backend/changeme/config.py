
import os

# Are we in a dev environment?
DEV = os.environ.get('DEV')

# A change here needs to be reflected in the docker-compose.yaml file, probably.
PORT = int(os.environ.get('PORT', 7082))

# We use the SqliteExtDatabase by default for its json capabilities.
DB_URL = os.environ.get('DB_URL') or 'sqliteext:///changeme.db'

# Webpack builds the JS and drops it into this folder.
STATIC_PATH = os.environ.get('STATIC_PATH', '/build')

# Images and stuff are in here.
ASSETS_PATH = os.environ.get('ASSETS_PATH', '/assets')
