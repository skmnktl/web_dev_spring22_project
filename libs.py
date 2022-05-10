"""
    This file holds all the libraries to be imported
"""

from flask import Flask
app = Flask(__name__)
from flask import render_template
from datetime import datetime
import re
import time