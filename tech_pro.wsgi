#!/usr/bin/python3.6
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"tech_pro/")

from FlaskApp import app as application
