from datetime import datetime

from flask import Blueprint, request

from app.common import curd
from app.common.helper import ModelFilter
from app.extensions import db
from app.models.models import User, UserRole, Role, UserBusiness, DictType
from app.schema.user_schema import DictTypeSchema
from app.utils.response import table_api, success_api, fail_api

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
    data = []
    for user, role in user:
        if UserBusiness.query.filter_by(user_id=user.id).count() > 0:
            mf = ModelFilter()
            mf.exact("user_id", user.id)
            userBusiness = (db.session.query(UserBusiness.business_id, DictType.dict_name)
                            .outerjoin(DictType, DictType.id == UserBusiness.business_id)
                            .filter(mf.get_filter(UserBusiness)).all())
        else:
            userBusiness = []
        print(f"用户信息:{user},角色信息：{role},角色信息：{userBusiness}")
        result = {
            'id': user.id,
            "username": user.username,
            "nickname": user.nickname,
            "email": user.email,
            "sex": user.sex,
            "phone": user.phone,
            "remark": user.remark,
            "status": str(user.status),
            'userType': str(user.user_type),
            "isActive": int(user.is_active),
            'userBusiness': [{'value': item[0], 'label': item[1]} for item in
                             userBusiness] if userBusiness else [],
            "userRole": {
                "roleName": role.role_name if role else None,
                "roleCode": role.role_code if role else None,
                "roleId": role.role_id if role else None,
            },
            'roleName': role.role_name if role else None,
            "createTime": user.ctime.strftime("%Y-%m-%d %H:%M:%S") if user.ctime is not None else None,
            "updateTime": user.mtime.strftime("%Y-%m-%d %H:%M:%S") if user.mtime is not None else None
        }
        data.append(result)

    return table_api(data=data, current=page, msg="查询成功", size=size, total=total)


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
    userType = request.get_json().get("userType")
    sex = request.get_json().get("sex")
    userBusiness = request.get_json().get("userBusiness")
    user = User(username=username, password=password, nickname=nickname, email=email, phone=phone, is_active=isActive,
                status=status, user_type=userType, ctime=datetime.now(), sex=sex)
    if bool(User.query.filter_by(username=username).count()):
        return fail_api("用户名已存在")
    db.session.add(user)
    db.session.flush()
    db.session.commit()
    if userType == '1':
        userRole = UserRole(user_id=user.id, role_id=userRole['roleId'], ctime=datetime.now())
        db.session.add(userRole)
        db.session.commit()
    if userType == '2':
        for item in userBusiness:
            userBusiness = UserBusiness(user_id=user.id, business_id=item, ctime=datetime.now())
            db.session.add(userBusiness)
            db.session.commit()

    return success_api()


@app_router.get("/getBusinessDict")
def getUserDictType():
    dictTypeInfo = DictType.query.filter_by(dict_type="business_user").all()
    data = curd.model_to_dicts(schema=DictTypeSchema, data=dictTypeInfo)
    return success_api(data=data)


@app_router.post("/updateUser")
def updateUserInfo():
    id = request.json["id"]
    username = request.get_json().get("username")
    password = request.get_json().get("password")
    nickname = request.get_json().get("nickname")
    email = request.get_json().get("email")
    phone = request.get_json().get("phone")
    isActive = request.get_json().get("isActive")
    status = request.get_json().get("status")
    userRole = request.get_json().get("userRole")
    userType = request.get_json().get("userType")
    sex = request.get_json().get("sex")
    userBusiness = request.get_json().get("userBusiness")
    if id == '1':
        return fail_api(msg="该用户为超级管理员，无法修改!")
    user = User(username=username, password=password, nickname=nickname, email=email, phone=phone, is_active=isActive,
                status=status, user_type=userType, mtime=datetime.now(), sex=sex, id=id)
    User.query.filter_by(id=id).update({"username": user.username,
                                        "password": user.password,
                                        "nickname": user.nickname,
                                        "email": user.email,
                                        'phone': user.phone,
                                        'sex': user.sex,
                                        "is_active": user.is_active,
                                        "status": user.status,
                                        "user_type": user.user_type,
                                        "mtime": user.mtime})
    if bool(UserRole.query.filter_by(user_id=user.id).count()):
        UserRole.query.filter_by(user_id=user.id).delete()
    if bool(UserBusiness.query.filter_by(user_id=user.id).count()):
        UserBusiness.query.filter_by(user_id=user.id).delete()
    if userType == '1':
        userRole = UserRole(user_id=user.id, role_id=userRole['roleId'], ctime=datetime.now())
        db.session.add(userRole)
    if userType == '2':
        for item in userBusiness:
            userBusiness = UserBusiness(user_id=user.id, business_id=item, ctime=datetime.now())
            db.session.add(userBusiness)
    db.session.commit()
    return success_api(msg='更新成功!')


@app_router.get("/deleteUser")
def deleteUserInfo():
    id = request.args.get("id")
    if id == 1:
        return fail_api(msg="超级管理员无法删除")
    User.query.filter_by(id=id).delete()
    db.session.commit()
    return success_api(msg="删除成功!")
