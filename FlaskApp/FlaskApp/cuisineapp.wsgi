#!/usr/bin/python
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/FlaskApp/")

from CuisineWise import app as application
application.secret_key = 'my_super_secret_key'

