"""
The flask application package.
"""

from flask import Flask,session
import os
app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
import lianjia.views
