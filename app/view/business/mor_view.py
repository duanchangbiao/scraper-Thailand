from flask import Blueprint, request

from app.common.helper import ModelFilter
from app.models.models import MorLicenses

app_router = Blueprint('mor', __name__, url_prefix='/mor')


@app_router.get('/list')
def getMorList():
    size = request.args.get("size", type=int)
    current = request.args.get("current", type=int)
    username = request.args.get("username", type=str)
    applyStatus = request.args.get("applyStatus", type=str)
    applyType = request.args.get("applyType", type=str)

    mf = ModelFilter()
    if username:
        mf.like("operate_name", username)
    if applyStatus:
        mf.exact("apply_status", applyStatus)
    if applyType:
        mf.exact("mor_type", applyType)
    morLicense = MorLicenses.query.filter(mf.get_filter(MorLicenses)).paginate(current=current, size=size)

