"""
    This file holds all the libraries to be imported
"""

from flask import Flask
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user, logout_user, login_user, UserMixin
from datetime import datetime
import re
import time
import datetime
from datetime import datetime
from flask_login import LoginManager
from flask import Blueprint
from flask_wtf import FlaskForm
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms import StringField, SubmitField, RadioField, IntegerField, DateField
from wtforms.widgets import TextArea
from wtforms.validators import DataRequired, Email
import requests
import json