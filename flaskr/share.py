import os
import datetime
from flask import (
    Blueprint, render_template, request, flash, redirect, url_for, current_app, session
)
from werkzeug.utils import secure_filename

bp = Blueprint('share', __name__)


@bp.route('/share', methods=['GET', 'POST'])
def share():
    from . import db
    database = db.get_db()
    if 'username' in session:
        data = database.execute("SELECT id FROM users WHERE username = (?)", (session['username'],)).fetchone()
        if not data:
            return redirect(url_for("index"))
    else:
        return redirect(url_for("index"))

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
            folderpath = current_app.config["UPLOAD_FOLDER"]
            for file_name in os.listdir(folderpath):
                if filename == file_name:
                    flash("This file already exists")
                    return redirect(request.url)
        try:
            user_id = database.execute("SELECT id FROM users WHERE username = ?", (session['username'],)).fetchone()
            if not user_id:
                flash("login error")
                return redirect("/index")
            database.execute(
                "INSERT INTO files (name, user_id, date) VALUES (?, ?, ?)",
                (file.filename, user_id[0], datetime.datetime.now()),
            )
            database.commit()
            file.save(os.path.join(folderpath, file.filename))
        except:
            flash("inserting files error")
            return redirect(request.url)

    # -------======Models======--------
    files_data = database.execute("SELECT * FROM files JOIN users ON files.user_id = users.id").fetchall()
    folder_path = current_app.config["UPLOAD_FOLDER"]
    files = []
    # -------==================--------
    if files_data:
        try:
            for file in files_data:
                for file_name in os.listdir(folder_path):
                    if file_name != file["name"]:
                        continue
                    file_path = os.path.join(folder_path, file_name)
                    f = {}
                    if os.path.isfile(file_path):
                        file_stat = os.stat(file_path)
                        f["length"] = file_stat.st_mtime
                        f["size"] = file_stat.st_size / 1024
                        f["type"] = file_name[-3:]
                        f["name"] = file_name[:-4]
                        f["fullname"] = file_name
                        f["username"] = file["username"]
                        f["date"] = file["date"]
                        files.append(f)
        except:
            flash("reading data from share table failed")
        return render_template("share.html", files=files)

    return render_template("share.html")
