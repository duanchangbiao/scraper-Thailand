from flask import request, Blueprint

from web.common.helper import ModelFilter
from web.extensions import db
from web.models.models import User, AftLicense
from web.utils.response import table_api

app_router = Blueprint("aft", __name__, url_prefix="/aft")


@app_router.get("/list")
def getAftList():
    data = []
    size = request.args.get("size", type=int)
    current = request.args.get("current", type=int)
    username = request.args.get("username", type=str)
    applyStatus = request.args.get("applyStatus", type=str)
    applyType = request.args.get("applyType", type=str)
    applyNumber = request.args.get("applyNumber", type=str)

    mf = ModelFilter()
    if username:
        user = User.query.filter_by(username=username).first()
        mf.like("user_id", str(user.id))
    if applyStatus:
        mf.exact("apply_status", applyStatus)
    if applyType:
        mf.exact("aft_type", applyType)
    if applyNumber:
        mf.like("apply_number", applyNumber)
    aftLicense_user = (db.session().query(AftLicense, User)
                       .outerjoin(User, User.id == AftLicense.user_id)
                       .filter(mf.get_filter(AftLicense))
                       .order_by(AftLicense.update_type.desc(), AftLicense.ctime.desc(), AftLicense.mtime.desc(),
                                 AftLicense.aft_type.desc())
                       .paginates(page=current, pageSize=size))

    for morLicense, user in aftLicense_user:
        resposne = {
            "id": morLicense.id,
            "username": user.username,
            "applyStatus": morLicense.apply_status,
            "applyType": morLicense.aft_type,
            "applyNumber": morLicense.apply_number,
            "applyDate": morLicense.apply_date,
            "applyLicense": morLicense.apply_license,
            "standardName": morLicense.standard_name,
            "updateType": morLicense.update_type,
            "tisCode": morLicense.TIS_code,
            "ctime": morLicense.ctime.strftime("%Y-%m-%d %H:%M:%S") if morLicense.ctime is not None else None,
            "mtime": morLicense.mtime.strftime("%Y-%m-%d %H:%M:%S") if morLicense.mtime is not None else None,
        }
        data.append(resposne)
    return table_api(data=data, total=aftLicense_user.total, current=current, size=size, msg='查询成功')
