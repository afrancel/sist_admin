#************** IMPORTAMOS ***************#
from flask import Flask
from flask import render_template
from flask import request, redirect
from flask import session
from flaskext.mysql import MySQL
from datetime import datetime
import os
from flask import send_from_directorys