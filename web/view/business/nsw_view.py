from datetime import datetime

from flask import request, Blueprint

from web.common.helper import ModelFilter
from web.extensions import db
from web.models.models import User, AftLicense, NswLicense
from web.utils.response import table_api, success_api

app_router = Blueprint("nsw", __name__, url_prefix="/nsw")


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
        mf.exact("mor_type", applyType)
    if applyNumber:
        mf.like("apply_number", applyNumber)
    nswLicense_user = (db.session().query(NswLicense, User)
                       .outerjoin(User, User.id == NswLicense.user_id)
                       .filter(mf.get_filter(NswLicense))
                       .order_by(NswLicense.sort.desc(), NswLicense.remark.desc(), NswLicense.ctime.desc())
                       .paginates(page=current, pageSize=size))

    for nswLicense, user in nswLicense_user:
        resposne = {
            "id": nswLicense.id,
            "username": user.username,
            "applyStatus": nswLicense.apply_status,
            "applyNumber": nswLicense.apply_number,
            "applyDate": nswLicense.apply_date,
            "invoice": nswLicense.invoice,
            "invoiceDate": nswLicense.invoice_date.strftime(
                "%Y-%m-%d %H:%M:%S") if nswLicense.ctime is not None else None,
            "passDate": nswLicense.pass_date,
            "productNumber": nswLicense.product_number,
            "updateType": nswLicense.update_type,
            "rpgGroup": nswLicense.rpg_group,
            "sort": nswLicense.sort,
            "remark": nswLicense.remark,
            "ctime": nswLicense.ctime.strftime("%Y-%m-%d %H:%M:%S") if nswLicense.ctime is not None else None,
            "mtime": nswLicense.mtime.strftime("%Y-%m-%d %H:%M:%S") if nswLicense.mtime is not None else None,
        }
        data.append(resposne)
    return table_api(data=data, total=nswLicense_user.total, current=current, size=size, msg='查询成功')


@app_router.post('/update')
def updateNsw():
    id = request.get_json().get("id")
    updateType = request.get_json().get("updateType")
    sort = request.get_json().get("sort")
    remark = request.get_json().get("remark")
    NswLicense.query.filter_by(id=id).update({"update_type": updateType, "remark": remark, "sort": sort})
    db.session.commit()
    return success_api(msg='操作成功')
