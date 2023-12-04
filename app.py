from flask import Flask, render_template, request
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_login import LoginManager, login_required

from database import db
from models import Users
import os

from ex_vuln.xss.xss import xss_page
from ex_vuln.idor.idor import idor_page, idor_api, idor_next_page, idor_logout
from ex_vuln.sqli.sqli import sqli_page, sqli_api
from ex_vuln.osci.osci import os_page
from ex_vuln.pathtrav.pathtrav import path_traversal_page, path_traversal_image
from ex_vuln.bruteforce.bruteforce import brute_page, brute_api

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

app.config['SECRET_KEY'] = 'a really really really really long secret key'

limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["100 per hour"],
    storage_uri="memory://",
)
# название файла с базой данных
db_name = 'database.db'

app.config['SQLALCHEMY_DATABASE_URI'] = \
    'sqlite:///' + os.path.join(basedir, db_name)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['PUBLIC_IMG_FOLDER'] = f"{basedir}/static/img"

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'idor'


@login_manager.user_loader
def load_user(user_id):
    return db.session.query(Users).get(user_id)


# главная страница
@app.route("/")
def home():
    return render_template('home.html')


# ex XSS
@app.route("/xss")
def xss():
    return xss_page(request)


# ex IDOR
@app.route('/idor', methods=['GET', 'POST'])
def idor():
    if request.method == 'GET':
        return idor_page()

    return idor_api(request)


@app.route('/idor_profile', methods=['GET'])
@login_required
def idor_profile():
    return idor_next_page()


@app.route('/logout')
@login_required
def logout():
    return idor_logout()


# ex SQLI
@app.route('/sqli', methods=['GET', 'POST'])
def sqli():
    if request.method == 'GET':
        return sqli_page()

    return sqli_api(request)


# ex OS command injection
@app.route('/os', methods=['GET'])
def os_injection():
    return os_page(request)


# ex Path Traversal
@app.route('/pathtraversal', methods=['GET'])
def path_traversal():
    return path_traversal_page()


@app.route('/pathtraversalimg', methods=['GET'])
def path_traversal_img():
    return path_traversal_image(request, app)


# ex Brute Force
@app.route('/bruteforce', methods=['GET', 'POST'])
@limiter.limit("5/minute")
def brute_force():
    if request.method == 'GET':
        return brute_page()

    return brute_api(request)

if __name__ == "__main__":
    app.run(debug=True)