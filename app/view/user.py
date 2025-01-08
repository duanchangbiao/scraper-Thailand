from datetime import datetime

from flask import Blueprint, request
from app.common.helper import ModelFilter
from app.extensions import db
from app.models.models import User, UserRole, Role
from app.utils.response import table_api, success_api, fail_api

app_router = Blueprint('user', __name__, url_prefix="/systemManage")


@app_router.route("/getUserList", methods=["GET"])
def getUserList():
    page = request.args.get('current', type=int)
    size = request.args.get('size', type=int)
    username = request.args.get("userName")
    nickname = request.args.get("nickName")
    email = request.args.get("userEmail")
    active = request.args.get("isActive")
    status = request.args.get("userStatus")
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
        'id': user.id if user.id is not None else None,
        "userName": user.username,
        "nickName": user.nickname,
        "userEmail": user.email,
        "userGender": user.sex,
        "userPhone": user.phone,
        "remark": user.remark,
        "status": str(user.status),
        "isActive": int(user.is_active),
        "userRole": {
            "roleName": role.role_name,
            "roleCode": role.role_code,
            "roleId": role.role_id,
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


@app_router.route("/updateUser", methods=["POST"])
def updateUserInfo():
    id = request.get_json().get("id")
    username = request.get_json().get("userName")
    password = request.get_json().get("password")
    nickname = request.get_json().get("nickName")
    email = request.get_json().get("userEmail")
    phone = request.get_json().get("userPhone")
    isActive = request.get_json().get("isActive")
    status = int(request.get_json().get("status"))
    userRoleParams = request.get_json().get("userRoles")
    user = User(id=id, username=username, password=password, nickname=nickname, email=email, phone=phone,
                is_active=isActive, status=status)
    if bool(UserRole.query.filter_by(user_id=id).count()):
        UserRole.query.filter_by(user_id=id).delete()
    User.query.filter_by(id=id).update({"is_active": user.is_active,
                                        "status": user.status,
                                        'username': user.username,
                                        'email': user.email,
                                        'phone': user.phone,
                                        'nickname': user.nickname,
                                        'password': user.password,
                                        'mtime': datetime.now()
                                        })
    userRole = UserRole(user_id=id, role_id=userRoleParams[0], ctime=user.ctime)
    db.session.add(userRole)
    db.session.commit()
    return success_api(msg='修改成功!')
