import os
import time
from flask import (
    Blueprint, render_template, request , flash, redirect,  url_for, current_app
)
from werkzeug.utils import secure_filename

bp = Blueprint('share', __name__)

@bp.route('/share', methods=['GET', 'POST'])
def share():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(current_app.config["UPLOAD_FOLDER"], filename))
            return redirect('/share')
    
    else:
        from . import db
        database = db.get_db()
        files = database.execute("SELECT * FROM files JOIN users ON files.user_id = users.id")
        folder_path = current_app.config["UPLOAD_FOLDER"]
        for file in files:
            for file_name in os.listdir(folder_path):
                if file_name != file["name"]:
                    continue
                file_path = os.path.join(folder_path, file_name)
                if os.path.isfile(file_path):
                    if file_name.endswith([".mp4", "mp3", "mkv"]):
                        file_stat = os.stat(file_path)
                        file["lengh"] = file_stat.st_mtime
                        file["siza"] = file_stat.st_size
                        file["type"] = file_name[-3]
                        file["name"] = file_name.removesuffix(file["type"])
        return render_template("share.html")
        