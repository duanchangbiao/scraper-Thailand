import time
from datetime import timedelta, datetime, timezone
from flask import Blueprint, request
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, jwt_required, get_jwt
from sqlalchemy import and_
from werkzeug.security import check_password_hash

from web.config import BaseConfig
from web.extensions import db
from web.models.models import User, Menu, UserRole, Role, RoleMenu
from web.utils.response import success_api, fail_api

app_router = Blueprint('auth', __name__, url_prefix='/auth')


def build_route_tree(menus: list[Menu], parent_id: int = 0, simple: bool = False, roleCode: str = None) -> list[dict]:
    """
    递归生成路由树
    :param menus:
    :param parent_id:
    :param simple: 是否简化返回数据
    :return:
    """
    tree = []
    for menu in menus:
        # 预加载关联的Role对象
        if menu.parent_id == parent_id:
            children = build_route_tree(menus, menu.id, simple, roleCode=roleCode)
            if simple:
                menu_dict = {
                    "name": menu.router_key,
                    "path": menu.router_path,
                    "component": menu.component,
                    "meta": {
                        "title": menu.menu_name,
                        "i18nKey": menu.menu_name,
                        "order": menu.order,
                        "roles": roleCode,  # todo roles
                        "icon": menu.icon,
                        "iconType": menu.icon_type,
                        "layout": menu.component,
                    }
                }
                # if menu.redirect:
                #     menu_dict["redirect"] = menu.redirect
                if menu.component:
                    menu_dict["meta"]["layout"] = menu.component.split("$", maxsplit=1)[0]
                if menu.hide_menu:
                    menu_dict["meta"]["hideInMenu"] = menu.hide_in_menu
            else:
                menu_dict = menu.to_dict()
            if children:
                menu_dict["children"] = children
            tree.append(menu_dict)
    return tree


@app_router.route('/login', methods=['POST'])
def login_required():
    username = request.get_json().get('userName')
    password = request.get_json().get('password')
    user_role = (db.session().query(User, Role)
                 .outerjoin(UserRole, User.id == UserRole.user_id)
                 .outerjoin(Role, UserRole.role_id == Role.role_id)
                 .filter(User.username == username).first())
    if not user_role:
        return fail_api(msg='用户不存在!')
    if not check_password_hash(user_role[0].password, password):
        return fail_api(msg='密码错误!')
    if user_role[0].status == 2:
        return fail_api(msg='用户已被禁用!')
    access_payload = {
        "data": {
            "userId": user_role[0].id,
            "userName": user_role[0].username,
            "nickName": user_role[0].nickname,
            "tokenType": "access_token",
            "roleName": user_role[1].role_name,
            "roleCode": user_role[1].role_code,
        },
        "exp": datetime.now(timezone.utc) + timedelta(hours=BaseConfig.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    }
    refresh_payload = access_payload
    refresh_payload["data"]["tokenType"] = "refresh_token"
    refresh_payload["exp"] = datetime.now(timezone.utc) + timedelta(hours=BaseConfig.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    data = {
        "token": create_access_token(identity=username, additional_claims=access_payload),
        "refreshToken": create_refresh_token(identity=username, additional_claims=refresh_payload),
    }
    return success_api(msg='登陆成功!', data=data)


@app_router.route('/getUserInfo', methods=['GET'])
@jwt_required()
def getUserInfo():
    current_user = get_jwt()
    roleCode = current_user["data"]["roleCode"]
    role = Role.query.filter_by(role_code=roleCode).first()
    menu_role = (db.session().query(RoleMenu, Menu)
                 .outerjoin(Menu, RoleMenu.menu_id == Menu.id)
                 .filter(RoleMenu.role_id == role.role_id).all())
    permit_list = []
    for menu in menu_role:
        permit_list.append(menu.Menu.permit_name)
    data = {
        "userId": current_user["data"]["userId"],
        "userName": current_user["data"]["userName"],
        "nickName": current_user["data"]["nickName"],
        "avatar": "",
        "roles": [current_user["data"]["roleCode"]],
        "permit": permit_list
    }
    return success_api(data=data)


@app_router.get("/getRouter")
@jwt_required()
def getRouter():
    current_user = get_jwt()
    roleCode = current_user["data"]["roleCode"]
    role = Role.query.filter_by(role_code=roleCode).first()
    menu_role = (db.session().query(RoleMenu, Menu)
                 .outerjoin(Menu, RoleMenu.menu_id == Menu.id)
                 .filter(and_(RoleMenu.role_id == role.role_id, Menu.status == "1", Menu.constant == "0")).order_by(
        Menu.order.asc()).all())
    menus = []
    for menu in menu_role:
        menus.append(menu[1])

    data = {"routes": build_route_tree(menus, simple=True, roleCode=roleCode)}
    return success_api(data=data, msg="查询成功")


@app_router.get("/isRouteExist")
@jwt_required()
def isExistRouter():
    routerName = request.args.get("routeName")
    menu = Menu.query.filter_by(router_name=routerName)
    if not bool(menu.count()):
        return fail_api(msg="该路由不存在")

    return success_api(data=menu.first().to_dict(), msg="查询成功")
