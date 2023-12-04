from flask import render_template
from models import Users

def sqli_page(request, app):
    return render_template('sqli.html', user=None)


def sqli_api(request, app):
    form = request.form

    username = form.get('username')
    password = form.get('password')

    user = Users.query.filter(Users.username == username).first()
    if user and user.check_password(password):
        return render_template('sqli.html', user=user is not None)
    else:
        return render_template('sqli.html', user=False)