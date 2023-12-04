from flask import render_template, redirect, url_for
from flask_login import current_user, login_user, logout_user
from models import Users

def idor_page(request, app):
    return render_template('idor.html', error=False)

def idor_api(request, app):
    if current_user.is_authenticated:
        return redirect(url_for('idor_profile'))
    
    form = request.form

    username = form.get('username')
    password = form.get('password')

    user = Users.query.filter(Users.username == username).first()
    if user and user.check_password(password):
        login_user(user)
        return redirect(url_for('idor_profile'))
    else:
        return redirect(url_for('idor'))


def idor_next_page(request, app):

    user = Users.query.get_or_404(current_user.id)

    return render_template('idor_profile.html', user=user.username)

def idor_logout(request, app):
    logout_user()
    return redirect(url_for('idor'))