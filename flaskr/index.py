from flask import (
    Blueprint, render_template, request, redirect
)
import psutil
from . import db

bp = Blueprint('index', __name__)

@bp.route('/')
def redirect_to_index():
    return redirect('/index')

@bp.route('/index', methods=['GET', 'POST'])
def index():
    # Iterate over all the keys in the dictionary
    for interface in psutil.net_if_addrs():
        # Check if the interface has a valid MAC address
        if psutil.net_if_addrs()[interface][0].address:
            # Print the MAC address for the interface
            mac_address = psutil.net_if_addrs()[interface][0].address
            mac_address = str(mac_address).replace('-','')
            break


    database = db.get_db()
    username = ""
    if request.method == 'post':
        username = request.form['name']
        print(username)
        names = database.execute("SELECT username FROM users")
        for name in names:
            if name == username:
                return render_template(
                    'index.html',
                    name = "",
                    msg = "This name already been used",
                    )
        database.execute("UPDATE users SET (username) = (?) mac_address = (?)", (username, mac_address,))

    else:
        name = database.execute("SELECT username FROM users WHERE mac_address = (?)", (mac_address,))
        if not name.fetchone():
            username = mac_address
            database.execute(
                "INSERT INTO users (username, mac_address) VALUES (?, ?)",
                (username,
                mac_address,
                ))
            print("in rune")
        else:
            username = name.fetchone()[0]
        return render_template(
            'index.html',
            name = username,
            msg = "change your name:)"
            )
        
    return render_template(
        'index.html',
        name = username,
        )