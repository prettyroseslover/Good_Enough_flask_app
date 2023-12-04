from flask import render_template, make_response
from models import Users

def brute_page(request, app):
    return make_response(render_template('bruteforce.html', user=None), 404)


def brute_api(request, app):
    form = request.form

    username = form.get('username')
    password = form.get('password')

    user = Users.query.filter(Users.username == username).first()
    if user and user.check_password(password):
        return make_response(render_template('bruteforce.html', user=user.username), 200)
    else: 
        return make_response(render_template('bruteforce.html', user=None), 404)
