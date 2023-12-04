from flask import Flask, render_template, request, redirect, url_for
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from database import db
from models import Users, Books
import os

from ex_vuln.xss.xss import xss_page
from ex_vuln.pathtrav.pathtrav import path_traversal_page, path_traversal_image
from ex_vuln.bruteforce.bruteforce import brute_page, brute_api

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
# название файла с базой данных
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["100 per hour"],
    storage_uri="memory://",
)

db_name = 'database.db'

app.config['SQLALCHEMY_DATABASE_URI'] = \
    'sqlite:///' + os.path.join(basedir, db_name)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['PUBLIC_IMG_FOLDER'] = f"{basedir}/static/img"

db.init_app(app)

# главная страница
@app.route("/")
def home():
    return render_template('home.html')

# ex XSS
@app.route("/xss")
def xss():
    return xss_page(request, app)

#Path Traversal
@app.route('/pathtraversal', methods=['GET'])
def path_traversal():
    return path_traversal_page(request, app)


@app.route('/pathtraversalimg', methods=['GET'])
def path_traversal_img():
    return path_traversal_image(request, app)


#Brute Force
@app.route('/bruteforce', methods=['GET', 'POST'])
@limiter.limit("5/minute")
def brute_force():
    if request.method == 'GET':
        return brute_page(request, app)

    return brute_api(request, app)

if __name__ == "__main__":
    app.run(debug=True)