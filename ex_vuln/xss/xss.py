from flask import render_template
from models import Books

def xss_page(request, app):
    books = Books.query
    search = request.args.get('search')
    if search:
        books = books.filter(Books.name.like(search)).all()
    else: 
        books = Books.query.all()
    return render_template('xss.html', books=books)