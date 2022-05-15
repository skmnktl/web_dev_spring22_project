"""
    This file holds all the libraries to be imported
"""

from flask import Flask
from flask import render_template, redirect, url_for
from datetime import datetime
import re
import time
from flask_login import LoginManager
from flask import Blueprint
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField, IntegerField, DateField
from wtforms.widgets import TextArea
from wtforms.validators import DataRequired, Email