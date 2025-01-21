from flask import Blueprint, request

from web.common.helper import ModelFilter
from web.extensions import db
from web.models.models import MorLicenses, User
from web.utils.response import table_api, success_api
from web.view.user import commonUpdateScraper

app_router = Blueprint('mor', __name__, url_prefix='/mor')


@app_router.get('/list')
def getMorList():
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
    morLicense_user = (db.session().query(MorLicenses, User)
                       .outerjoin(User, User.id == MorLicenses.user_id)
                       .filter(mf.get_filter(MorLicenses))
                       .order_by(MorLicenses.sort.desc(), MorLicenses.remark.desc(), MorLicenses.apply_status.desc())
                       .paginates(page=current, pageSize=size))

    for morLicense, user in morLicense_user:
        resposne = {
            "id": morLicense.id,
            "username": user.username,
            "applyStatus": morLicense.apply_status,
            "applyType": morLicense.mor_type,
            "applyNumber": morLicense.apply_number,
            "applyDate": morLicense.apply_date,
            "applyLicense": morLicense.apply_license,
            "applyTax": morLicense.apply_tax,
            "updateType": morLicense.update_type,
            "companyName": morLicense.operate_name,
            "standardName": morLicense.standard_name,
            "tisCode": morLicense.TIS_code,
            "sort": morLicense.sort,
            "remark": morLicense.remark,
            "ctime": morLicense.ctime.strftime("%Y-%m-%d %H:%M:%S") if morLicense.ctime is not None else None,
            "mtime": morLicense.mtime.strftime("%Y-%m-%d %H:%M:%S") if morLicense.mtime is not None else None,
        }
        data.append(resposne)
    return table_api(data=data, total=morLicense_user.total, current=current, size=size, msg='查询成功')


@app_router.post('/update')
def updateMor():
    username = request.get_json().get("username")
    morType = request.get_json().get("applyType")
    user = User.query.filter_by(username=username).first()
    commonUpdateScraper(user, [morType])
    return success_api(msg='更新成功!')


@app_router.post("/readStatus")
def updateReadStatus():
    id = request.get_json().get("id")
    updateType = request.get_json().get("updateType")
    sort = request.get_json().get("sort")
    remark = request.get_json().get("remark")

    MorLicenses.query.filter_by(id=id).update({"update_type": updateType, "remark": remark, "sort": sort})
    db.session.commit()
    return success_api(msg='操作成功')
