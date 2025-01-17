from web.extensions import db
from web.models.models import User, UserBusiness, DictType
from web.view.user import commonUpdateScraper


def ryNoParams():
    from app import app
    with app.app_context():
        user = User.query.filter_by(user_type='2')
        for u in user:
            dict_list = (db.session.query(UserBusiness.user_id, DictType.dict_name)
                         .outerjoin(DictType, DictType.id == UserBusiness.business_id)
                         .filter(UserBusiness.user_id == u.id).all())
            args = []
            for item in dict_list:
                args.append(item[1])
            commonUpdateScraper(u, args)
