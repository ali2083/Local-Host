from flask import (
    Blueprint, render_template
)

bp = Blueprint('share', __name__)

@bp.route('/share')
def share():
    return "nope"