from datetime import datetime

from flask import request, Blueprint

from web.common.helper import ModelFilter
from web.extensions import db
from web.models.models import User, AftLicense, NswLicense
from web.utils.response import table_api

app_router = Blueprint("nsw", __name__, url_prefix="/nsw")


@app_router.get("/list")
def getAftList():
    data = []
    size = request.args.get("size", type=int)
    current = request.args.get("current", type=int)
    username = request.args.get("username", type=str)
    applyStatus = request.args.get("applyStatus", type=str)
    applyType = request.args.get("applyType", type=str)

    mf = ModelFilter()
    if username:
        user = User.query.filter_by(username=username).first()
        mf.like("user_id", str(user.id))
    if applyStatus:
        mf.exact("apply_status", applyStatus)
    if applyType:
        mf.exact("mor_type", applyType)
    aftLicense_user = (db.session().query(NswLicense, User)
                       .outerjoin(User, User.id == NswLicense.user_id)
                       .filter(mf.get_filter(NswLicense))
                       .order_by(NswLicense.update_type.desc(),NswLicense.ctime.desc(), NswLicense.mtime.desc())
                       .paginates(page=current, pageSize=size))

    for morLicense, user in aftLicense_user:
        resposne = {
            "id": morLicense.id,
            "username": user.username,
            "applyStatus": morLicense.apply_status,
            "applyNumber": morLicense.apply_number,
            "applyDate": morLicense.apply_date,
            "invoice": morLicense.invoice,
            "invoiceDate": morLicense.invoice_date.strftime(
                "%Y-%m-%d %H:%M:%S") if morLicense.ctime is not None else None,
            "passDate": morLicense.pass_date,
            "productNumber": morLicense.product_number,
            "updateType": morLicense.update_type,
            "rpgGroup": morLicense.rpg_group,
            "ctime": morLicense.ctime.strftime("%Y-%m-%d %H:%M:%S") if morLicense.ctime is not None else None,
            "mtime": morLicense.mtime.strftime("%Y-%m-%d %H:%M:%S") if morLicense.mtime is not None else None,
        }
        data.append(resposne)
    return table_api(data=data, total=aftLicense_user.total, current=current, size=size, msg='查询成功')
