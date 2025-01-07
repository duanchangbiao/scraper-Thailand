from flask import Blueprint, request
from app.common.helper import ModelFilter
from app.extensions import db
from app.models.models import User, UserRole, Role
from app.utils.response import table_api, success_api

app_router = Blueprint('user', __name__, url_prefix="/systemManage")


@app_router.route("/getUserList", methods=["GET"])
def getUserList():
    page = request.args.get('current', type=int)
    size = request.args.get('size', type=int)
    username = request.args.get("username")
    nickname = request.args.get("nickname")
    email = request.args.get("email")
    active = request.args.get("isActive")
    status = request.args.get("status")
    mf = ModelFilter()
    if username:
        mf.like("username", username)
    if nickname:
        mf.like("nickname", nickname)
    if email:
        mf.like("email", email)
    if active:
        mf.exact("is_active", active)
    if status:
        mf.exact("status", status)

    user = (db.session.query(User, Role)
            .outerjoin(UserRole, UserRole.user_id == User.id)
            .outerjoin(Role, Role.role_id == UserRole.role_id)
            .filter(mf.get_filter(User)).order_by(User.ctime.desc(), User.mtime.desc())
            .paginates(page=page, pageSize=size))
    total = user.total
    return table_api(data=[{
        "username": user.username if user.username is not None else None,
        "nickname": user.nickname if user.nickname is not None else None,
        "email": user.email if user.email is not None else None,
        "sex": user.sex if user.sex is not None else None,
        "phone": user.phone if user.phone is not None else None,
        "remark": user.remark if user.remark is not None else None,
        "status": user.status if user.status is not None else None,
        "isActive": int(user.is_active),
        "userRole": {
            "roleName": role.role_name if role.role_name is not None else None,
            "roleCode": role.role_code if role.role_code is not None else None,
            "roleId": role.role_id if role.role_id is not None else None,
        },
        "createTime": user.ctime.strftime("%Y-%m-%d %H:%M:%S") if user.ctime is not None else None,
        "updateTime": user.mtime.strftime("%Y-%m-%d %H:%M:%S") if user.mtime is not None else None
    } for user, role in user.items], current=page, msg="查询成功", size=size, total=total)


@app_router.route("/saveUser", methods=["POST"])
def saveUser():
    username = request.get_json().get("username")
    password = request.get_json().get("password")
    nickname = request.get_json().get("nickname")
    email = request.get_json().get("email")
    phone = request.get_json().get("phone")
    isActive = request.get_json().get("isActive")
    status = request.get_json().get("status")
    userRole = request.get_json().get("userRole")
    print(userRole, username, password, nickname, email, phone, isActive, status)
    return success_api()


