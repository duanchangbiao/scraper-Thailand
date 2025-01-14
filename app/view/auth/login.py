import time
from datetime import timedelta, datetime, timezone
from flask import Blueprint, request
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, jwt_required, get_jwt
from werkzeug.security import check_password_hash

from app import BaseConfig
from app.common.helper import ModelFilter
from app.extensions import db
from app.models.models import User, Menu, UserRole, Role, RoleMenu
from app.utils.response import success_api, fail_api

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
                        "keepAlive": True,
                        "layout": menu.component,
                        "href":None,
                        "multiTab":False,
                        "activeMenu": None,
                        "fixedIndexInTab": None,
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
                 .filter(RoleMenu.role_id == role.role_id).order_by(Menu.order.asc()).all())
    menus = []
    for menu in menu_role:
        menus.append(menu[1])

    data = {"routes": build_route_tree(menus, simple=True, roleCode=roleCode)}

    # data= {"home": "home", "routes": [
    #     {"name": "home", "path": "/home", "component": "layout.base$view.home",
    #      "meta": {"title": "首页", "i18nKey": "route.home", "order": 1, "keepAlive": False,
    #               "icon": "mdi:monitor-dashboard", "iconType": "1", "href": None, "activeMenu": None, "multiTab": False,
    #               "fixedIndexInTab": None, "layout": "layout.base"}},
    #     {"name": "function", "path": "/function", "component": "layout.base",
    #      "meta": {"title": "功能", "i18nKey": "route.function", "order": 2, "keepAlive": False,
    #               "icon": "icon-park-outline:all-application", "iconType": "1", "href": None, "activeMenu": None,
    #               "multiTab": False, "fixedIndexInTab": None, "layout": "layout.base"}, "children": [
    #         {"name": "function_toggle-auth", "path": "/function/toggle-auth", "component": "view.function_toggle-auth",
    #          "meta": {"title": "切换权限", "i18nKey": "route.function_toggle-auth", "order": 4, "keepAlive": False,
    #                   "icon": "ic:round-construction", "iconType": "1", "href": None, "activeMenu": None,
    #                   "multiTab": False, "fixedIndexInTab": None, "layout": "view.function_toggle-auth"}},
    #         {"name": "function_request", "path": "/function/request", "component": "view.function_request",
    #          "meta": {"title": "请求", "i18nKey": "route.function_request", "order": 3, "keepAlive": False,
    #                   "icon": "carbon:network-overlay", "iconType": "1", "href": None, "activeMenu": None,
    #                   "multiTab": False, "fixedIndexInTab": None, "layout": "view.function_request"}},
    #         {"name": "function_super-page", "path": "/function/super-page", "component": "view.function_super-page",
    #          "meta": {"title": "超级管理员可见", "i18nKey": "route.function_super-page", "order": 5, "keepAlive": False,
    #                   "icon": "ic:round-supervisor-account", "iconType": "1", "href": None, "activeMenu": None,
    #                   "multiTab": False, "fixedIndexInTab": None, "layout": "view.function_super-page"}},
    #         {"name": "function_multi-tab", "path": "/function/multi-tab", "component": "view.function_multi-tab",
    #          "meta": {"title": "多标签页", "i18nKey": "route.function_multi-tab", "order": 1, "keepAlive": False,
    #                   "icon": "ic:round-tab", "iconType": "1", "href": None, "activeMenu": "function_tab",
    #                   "multiTab": True, "fixedIndexInTab": None, "layout": "view.function_multi-tab",
    #                   "hideInMenu": True}},
    #         {"name": "function_tab", "path": "/function/tab", "component": "view.function_tab",
    #          "meta": {"title": "标签页", "i18nKey": "route.function_tab", "order": 2, "keepAlive": False,
    #                   "icon": "ic:round-tab", "iconType": "1", "href": None, "activeMenu": None, "multiTab": False,
    #                   "fixedIndexInTab": None, "layout": "view.function_tab"}},
    #         {"name": "function_hide-child", "path": "/function/hide-child", "component": None,
    #          "meta": {"title": "隐藏子菜单", "i18nKey": "route.function_hide-child", "order": 2, "keepAlive": False,
    #                   "icon": "material-symbols:filter-list-off", "iconType": "1", "href": None, "activeMenu": None,
    #                   "multiTab": False, "fixedIndexInTab": None}, "redirect": "/function/hide-child/one", "children": [
    #             {"name": "function_hide-child_one", "path": "/function/hide-child/one",
    #              "component": "view.function_hide-child_one",
    #              "meta": {"title": "隐藏子菜单1", "i18nKey": "route.function_hide-child_one", "order": 1,
    #                       "keepAlive": False, "icon": "material-symbols:filter-list-off", "iconType": "1", "href": None,
    #                       "activeMenu": "function_hide-child", "multiTab": False, "fixedIndexInTab": None,
    #                       "layout": "view.function_hide-child_one", "hideInMenu": True}},
    #             {"name": "function_hide-child_two", "path": "/function/hide-child/two",
    #              "component": "view.function_hide-child_two",
    #              "meta": {"title": "隐藏子菜单2", "i18nKey": "route.function_hide-child_two", "order": 2,
    #                       "keepAlive": False, "icon": None, "iconType": None, "href": None,
    #                       "activeMenu": "function_hide-child", "multiTab": False, "fixedIndexInTab": None,
    #                       "layout": "view.function_hide-child_two", "hideInMenu": True}},
    #             {"name": "function_hide-child_three", "path": "/function/hide-child/three",
    #              "component": "view.function_hide-child_three",
    #              "meta": {"title": "隐藏子菜单3", "i18nKey": "route.function_hide-child_three", "order": 3,
    #                       "keepAlive": False, "icon": None, "iconType": None, "href": None,
    #                       "activeMenu": "function_hide-child", "multiTab": False, "fixedIndexInTab": None,
    #                       "layout": "view.function_hide-child_three", "hideInMenu": True}}]}]},
    #     {"name": "exception", "path": "/exception", "component": "layout.base",
    #      "meta": {"title": "异常页", "i18nKey": "route.exception", "order": 3, "keepAlive": False,
    #               "icon": "ant-design:exception-outlined", "iconType": "1", "href": None, "activeMenu": None,
    #               "multiTab": False, "fixedIndexInTab": None, "layout": "layout.base"}, "children": [
    #         {"name": "exception_403", "path": "/exception/403", "component": "view.403",
    #          "meta": {"title": "403", "i18nKey": "route.exception_403", "order": 1, "keepAlive": False,
    #                   "icon": "ic:baseline-block", "iconType": "1", "href": None, "activeMenu": None, "multiTab": False,
    #                   "fixedIndexInTab": None, "layout": "view.403"}},
    #         {"name": "exception_404", "path": "/exception/404", "component": "view.404",
    #          "meta": {"title": "404", "i18nKey": "route.exception_404", "order": 2, "keepAlive": False,
    #                   "icon": "ic:baseline-web-asset-off", "iconType": "1", "href": None, "activeMenu": None,
    #                   "multiTab": False, "fixedIndexInTab": None, "layout": "view.404"}},
    #         {"name": "exception_500", "path": "/exception/500", "component": "view.500",
    #          "meta": {"title": "500", "i18nKey": "route.exception_500", "order": 3, "keepAlive": False,
    #                   "icon": "ic:baseline-wifi-off", "iconType": "1", "href": None, "activeMenu": None,
    #                   "multiTab": False, "fixedIndexInTab": None, "layout": "view.500"}}]},
    #     {"name": "manage", "path": "/manage", "component": "layout.base",
    #      "meta": {"title": "系统管理", "i18nKey": "route.manage", "order": 5, "keepAlive": False,
    #               "icon": "carbon:cloud-service-management", "iconType": "1", "href": None, "activeMenu": None,
    #               "multiTab": False, "fixedIndexInTab": None, "layout": "layout.base"}, "children": [
    #         {"name": "manage_user", "path": "/manage/user", "component": "view.manage_user",
    #          "meta": {"title": "用户管理", "i18nKey": "route.manage_user", "order": 3, "keepAlive": False,
    #                   "icon": "ic:round-manage-accounts", "iconType": "1", "href": None, "activeMenu": None,
    #                   "multiTab": False, "fixedIndexInTab": None, "layout": "view.manage_user"}},
    #         {"name": "manage_role", "path": "/manage/role", "component": "view.manage_role",
    #          "meta": {"title": "角色管理", "i18nKey": "route.manage_role", "order": 4, "keepAlive": False,
    #                   "icon": "carbon:user-role", "iconType": "1", "href": None, "activeMenu": None, "multiTab": False,
    #                   "fixedIndexInTab": None, "layout": "view.manage_role"}},
    #         {"name": "manage_menu", "path": "/manage/menu", "component": "view.manage_menu",
    #          "meta": {"title": "菜单管理", "i18nKey": "route.manage_menu", "order": 5, "keepAlive": False,
    #                   "icon": "material-symbols:route", "iconType": "1", "href": None, "activeMenu": None,
    #                   "multiTab": False, "fixedIndexInTab": None, "layout": "view.manage_menu"}},
    #         {"name": "manage_user-detail", "path": "/manage/user-detail/:id", "component": "view.manage_user-detail",
    #          "meta": {"title": "用户详情", "i18nKey": "route.manage_user-detail", "order": 6, "keepAlive": False,
    #                   "icon": None, "iconType": None, "href": None, "activeMenu": None, "multiTab": False,
    #                   "fixedIndexInTab": None, "layout": "view.manage_user-detail", "hideInMenu": True}}]},
    #     {"name": "about", "path": "/about", "component": "layout.base$view.about",
    #      "meta": {"title": "关于", "i18nKey": "route.about", "order": 6, "keepAlive": False,
    #               "icon": "fluent:book-information-24-regular", "iconType": "1", "href": None, "activeMenu": None,
    #               "multiTab": False, "fixedIndexInTab": None, "layout": "layout.base"}}]}
    return success_api(data=data, msg="查询成功")


@app_router.get("/isRouteExist")
def isExistRouter():
    routerName = request.args.get("routeName")
    menu = Menu.query.filter_by(router_name=routerName)
    if not bool(menu.count()):
        return fail_api(msg="该路由不存在")

    return success_api(data=menu.first().to_dict(), msg="查询成功")
