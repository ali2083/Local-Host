import datetime

from flask import (
    Blueprint, render_template, request, flash, redirect, url_for, current_app, session
)

bp = Blueprint('chatbox', __name__)


@bp.route('/chatbox', methods=['GET', 'POST'])
def chatbox():
    from . import db
    database = db.get_db()
    if 'username' in session:
        data = database.execute("SELECT id FROM users WHERE username = (?)", (session['username'],)).fetchone()
        if not data:
            return redirect(url_for("index"))
    else:
        return redirect(url_for("index"))

    if request.method == 'POST':
        message = request.form.get('message')
        if not message:
            flash("void massage")
            return redirect("/chatbox")
        try:
            user_id = database.execute("SELECT id FROM users WHERE username = ?", (session['username'],)).fetchone()
            if not user_id:
                flash("login error")
                return redirect("/index")
            database.execute(
                "INSERT INTO chats (user_id, massage_text, date) VALUES (?, ?, ?)",
                (user_id[0], message, datetime.datetime.now()),
            )
            database.commit()
            return redirect(request.url)
        except:
            flash("inserting message error")
            return redirect(request.url)
    else:
        chats_data = database.execute("SELECT * FROM chats JOIN users ON chats.user_id = users.id").fetchall()
        return render_template("chat.html", chats=chats_data)
