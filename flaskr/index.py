from flask import (
    Blueprint, render_template, request, redirect, session, flash
)
# import psutil
from . import db

bp = Blueprint('index', __name__)


@bp.route('/')
def redirect_to_index():
    return redirect('/index')


@bp.route('/index', methods=['GET', 'POST'])
def index():
    msg = ""
    from . import db
    database = db.get_db()

    if request.method == 'POST':
        username = request.form.get("name")
        session['username'] = username
        try:
            data = database.execute("SELECT id FROM users WHERE username = (?)", (username,)).fetchone()
            if not data:
                database.execute("INSERT INTO users (username) VALUES (?)", (username,))
                database.commit()
        except:
            flash("inserting to database at start failed")
            msg = "internal error 500"

    if 'username' in session:
        username = session['username']
        data = database.execute("SELECT id FROM users WHERE username = (?)", (username,)).fetchone()
        if data and username:
            username = str(data[0]) + " - " + username
            msg = "you are logged in"
    else:
        username = "username"
        msg = "Please! Enter yourname"

    return render_template(
        "index.html",
        name=username,
        msg=msg,
    )
# Done
