from flask import render_template, send_file, make_response
import os

def path_traversal_page():
    return render_template("pathtraversal.html")

def path_traversal_image(request, app):
    image_path = f"{app.config['PUBLIC_IMG_FOLDER']}/{os.path.basename(request.args.get('img'))}"
    try:
        return send_file(image_path)
    except FileNotFoundError:
        return make_response(render_template('pathtraversal.html'), 404)