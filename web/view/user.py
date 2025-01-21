from datetime import datetime

from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from flask_mail import Message
from werkzeug.security import generate_password_hash

from web.common import curd
from web.common.helper import ModelFilter
from web.extensions import db
from web.extensions.init_mail import mail
from web.models.models import User, UserRole, Role, UserBusiness, DictType, AftLicense, NswLicense, MorLicenses
from web.schema.user_schema import DictTypeSchema
from web.utils.response import table_api, success_api, fail_api
from web.utils.scraper_passport import ScraperPassport

app_router = Blueprint('user', __name__, url_prefix="/systemManage")


@app_router.route("/getUserList", methods=["GET"])
@jwt_required()
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
@jwt_required()
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
    if userType == "1":
        password = generate_password_hash(password)
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

    return success_api(msg='新增成功')


@app_router.get("/getBusinessDict")
@jwt_required()
def getUserDictType():
    dictTypeInfo = DictType.query.filter_by(dict_type="business_user").all()
    data = curd.model_to_dicts(schema=DictTypeSchema, data=dictTypeInfo)
    return success_api(data=data)


@app_router.post("/updateUser")
@jwt_required()
def updateUserInfo():
    id = request.json["id"]
    username = request.get_json().get("username")
    nickname = request.get_json().get("nickname")
    email = request.get_json().get("email")
    phone = request.get_json().get("phone")
    isActive = request.get_json().get("isActive")
    status = request.get_json().get("status")
    userRoleDict = request.get_json().get("userRole")
    userType = request.get_json().get("userType")
    sex = request.get_json().get("sex")
    userBusinessDict = request.get_json().get("userBusiness")
    if id == '1':
        return fail_api(msg="该用户为超级管理员，无法修改!")
    user = User(username=username, nickname=nickname, email=email, phone=phone, is_active=isActive,
                status=status, user_type=userType, mtime=datetime.now(), sex=sex, id=id)
    User.query.filter_by(id=id).update({"username": user.username,
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
        userRole = UserRole(user_id=user.id, role_id=userRoleDict['roleId'], ctime=datetime.now())
        db.session.add(userRole)
    if userType == '2':
        for item in userBusinessDict:
            userBusiness = UserBusiness(user_id=user.id, business_id=item["value"], ctime=datetime.now())
            db.session.add(userBusiness)
    db.session.commit()
    return success_api(msg='更新成功!')


@app_router.get("/deleteUser")
@jwt_required()
def deleteUserInfo():
    id = request.args.get("id")
    userType = request.args.get("userType")
    if id == 1:
        return fail_api(msg="超级管理员无法删除")
    if userType == '1' and bool(UserRole.query.filter_by(user_id=id).count()):
        UserRole.query.filter_by(user_id=id).delete()
    if userType == '2' and bool(UserBusiness.query.filter_by(user_id=id).count()):
        UserBusiness.query.filter_by(user_id=id).delete()
    User.query.filter_by(id=id).delete()
    db.session.commit()
    return success_api(msg="删除成功!")


@app_router.get("/updateUserScraper")
@jwt_required()
def updateUserScraper():
    id = request.args.get("id")
    userType = request.args.get("userType")
    if userType == '1':
        return fail_api(msg="该用户为类型不支持更新!")
    if not bool(UserBusiness.query.filter_by(user_id=id).count()):
        return fail_api(msg="该用户未绑定业务,无法更新!")
    user = User.query.filter_by(id=id).first()
    mf = ModelFilter()
    mf.exact("user_id", id)
    dict_list = (db.session.query(UserBusiness.user_id, DictType.dict_name)
                 .outerjoin(DictType, DictType.id == UserBusiness.business_id)
                 .filter(mf.get_filter(UserBusiness)).all())
    args = []
    for item in dict_list:
        args.append(item[1])
    commonUpdateScraper(user, args)

    return success_api(msg="更新成功!")


def commonUpdateScraper(user: User, args: list):
    scraper_list = []
    data = {}
    try:
        scrapyer = ScraperPassport(username=user.username, password=user.password, action_type=args)
        scrapyer.login()
        data = scrapyer.close()
        print(data)
    except Exception as e:
        print(f"打印异常信息:{e}")
    if data:
        for key, value in data.items():
            for item in value:
                match key:
                    case "AFFA":
                        aFFtLicense = AftLicense(user_id=user.id,
                                                 apply_number=item['AFFA_appId'],
                                                 apply_status=item['status'] if item['status'] else '',
                                                 TIS_code=item['AFFA_TIS_CODE'],
                                                 standard_name=item['AFFA_APP_NAME'],
                                                 apply_license=item['AFFA_APP_LICENSE'],
                                                 apply_date=item['applicationDate'],
                                                 aft_type=key,
                                                 ctime=datetime.now()
                                                 )
                        scraper_list.append(aFFtLicense)
                    case "AFT":
                        aftLicense = AftLicense(user_id=user.id,
                                                apply_number=item['ATF_appId'],
                                                apply_status=item['status'] if item['status'] else '',
                                                TIS_code=item['ATF_TIS_CODE'],
                                                standard_name=item['ATF_APP_NAME'],
                                                apply_license=item['AFT_APP_LICENSE'],
                                                apply_date=item['applicationDate'],
                                                aft_type=key,
                                                ctime=datetime.now()
                                                )
                        scraper_list.append(aftLicense)
                    case "NSW":
                        nswLicense = NswLicense(user_id=user.id,
                                                apply_number=item['NSW_CODE'],
                                                apply_status=item['NSW_APPLY_STATUS'] if item[
                                                    'NSW_APPLY_STATUS'] else '',
                                                apply_date=item['NSW_APPLY_DATE'],
                                                invoice=item['NSW_INVOICE'],
                                                invoice_date=item['NSW_INVOICE_DATE'],
                                                product_number=item['NSW_PRO_NUMBER'],
                                                rpg_group=item['NSW_RPG'],
                                                pass_date=item['NSW_APPLY_PASS_DATE'],
                                                ctime=datetime.now()
                                                )
                        scraper_list.append(nswLicense)
                    case "Mor5":
                        mor5Licenses = MorLicenses(user_id=user.id,
                                                   mor_type=key,
                                                   apply_number=item['id'],
                                                   apply_status=item['status'] if item['status'] else '',
                                                   apply_date=item['applicationDate'],
                                                   apply_tax=item['taxNumber'],
                                                   TIS_code=item['mokId'],
                                                   standard_name=item['standardName'],
                                                   ctime=datetime.now(),
                                                   operate_name=item['companyName'],
                                                   )
                        scraper_list.append(mor5Licenses)
                    case "Mor9":
                        morLicenses = MorLicenses(user_id=user.id,
                                                  mor_type=key,
                                                  apply_number=item['MOR9_APPLY_CODE'],
                                                  apply_status=item['MOR9_STATUS'] if item['MOR9_STATUS'] else '',
                                                  apply_date=item['MOR9_APPLY_DATE'],
                                                  apply_tax=item['MOR9_TAX'],
                                                  TIS_code=item['MOR9_TIS_CODE'],
                                                  standard_name=item['MOR9_STANDARD_NAME'],
                                                  apply_license=item['MOR9_LICENSE_CODE'],
                                                  ctime=datetime.now(),
                                                  )
                        scraper_list.append(morLicenses)

        for item in scraper_list:
            mfs = ModelFilter()
            if item.apply_status:
                mfs.exact("apply_status", item.apply_status)
            if item.apply_number:
                mfs.exact("apply_number", item.apply_number)
            if not bool(db.session.query(item.__class__).filter(mfs.get_filter(item.__class__)).count()):
                # 添加数据库,发送更新消息
                db.session.query(item.__class__).filter_by(apply_number=item.apply_number).update({
                    "mtime": datetime.now(),
                    "apply_status": item.apply_status,
                    "apply_date": item.apply_date,
                    "update_type": "2"
                })
                # 发送邮件
                sendEmail(user, item)

            if not bool(db.session.query(item.__class__).filter_by(apply_number=item.apply_number).count()):
                db.session.add(item)
            db.session.query(item.__class__).filter_by(apply_number=item.apply_number).update({
                item.__class__.ctime: datetime.now(),
            })
            db.session.commit()


def sendEmail(user, result):
    if result.__class__ == AftLicense:
        title = f'TISI Alert:{result.aft_type}/{user.nickname} Adaptor have update!'
        body = (f'----------------------------\n'
                f'Client :{user.nickname}\n '
                f'{result.aft_type} No : {result.apply_number} \n'
                f'Account Number: {user.username}, \n'
                f'Current Status : {result.apply_status} \n'
                f'Current Date : {datetime.now()} \n'
                f'Quickly Check : https://sso.tisi.go.th/login')
    elif result.__class__ == MorLicenses:
        title = f'TISI Alert:{result.mor_type}/{user.nickname} Mor have update!'
        body = (f'----------------------------\n'
                f'Client :{user.nickname}\n '
                f'{result.mor_type} No : {result.apply_number} \n'
                f'----------------------------\n'
                f'Account Number: {user.username}, \n'
                f'Current Status : {result.apply_status} \n'
                f'Current Date : {datetime.now()} \n'
                f'Quickly Check : https://sso.tisi.go.th/login')
    else:
        title = f'TISI Alert:NSW/{user.nickname} have update!'
        body = (f'----------------------------\n'
                f'Client :{user.nickname}\n '
                f'NSW No : {result.apply_number} \n'
                f'----------------------------\n'
                f'Account Number: {user.username}, \n'
                f'Current Status : {result.apply_status} \n'
                f'Current Date : {datetime.now()} \n'
                f'Quickly Check : https://sso.tisi.go.th/login \n')

    message = Message(subject=title, recipients=[user.email], body=body)
    mail.send(message)
