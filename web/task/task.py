from datetime import datetime

from web.models.models import User


def ryNoParams():
    from app import app
    with app.app_context():
        user = User.query.filter_by(user_type='2')
        for u in user:
            print(u)