from datetime import datetime

from flask import Blueprint, jsonify, request
from sqlalchemy import or_

from web.common import curd
from web.common.helper import ModelFilter
from web.extensions import db
from web.models.models import Menu, RoleMenu
from web.schema.menu_schema import ButtonSchema
from web.utils.response import success_api, table_api, fail_api

app_router = Blueprint('menu', __name__, url_prefix="/systemManage")


def build_category_tree(menus: list[Menu]):
    menus_map = {category.id: category for category in menus}
    tree = []

    for category in menus:
        if category.parent_id:
            parent = menus_map.get(category.parent_id)
            if parent:
                if not hasattr(parent, 'children'):
                    parent.children = []
                parent.children.append(category)
        else:
            tree.append(category)

    return tree


@app_router.get("/getMenuList")
def getMenuList():
    menuList = Menu.query.order_by(Menu.order.asc()).all()
    tree_list = build_category_tree(menuList)

    def category_to_dict(category):
        return {
            'id': category.id,
            'menuName': category.menu_name,
            'menuType': str(category.menu_type),
            'parentId': category.parent_id,
            'permitName': category.permit_name,
            'remark': category.remark,
            'i18nKey': category.router_key,
            'routePath': category.router_path,
            'routeName': category.router_key,
            'menuStatus': str(category.status),
            'hideInMenu': str(category.hide_menu),
            'icon': category.icon,
            'iconType': str(category.icon_type),
            'order': category.order,
            'component': category.component,
            'children': [category_to_dict(child) for child in getattr(category, 'children', [])]
        }

    tree_dict = [category_to_dict(root) for root in tree_list]
    return table_api(data=tree_dict, total=len(tree_dict), current=1, size=10)


@app_router.post("/saveMenu")
def saveMenuInfo():
    component = request.get_json().get('component')
    icon = request.get_json().get('icon')
    icon_type = request.get_json().get('iconType')
    menu_type = request.get_json().get('menuType')
    menu_name = request.get_json().get('menuName')
    parentId = request.get_json().get('parentId')
    permit_name = request.get_json().get('permitName')
    remark = request.get_json().get('remark')
    hideInMenu = request.get_json().get('hideInMenu')
    order = request.get_json().get('order')
    routeName = request.get_json().get('routeName')
    routePath = request.get_json().get('routePath')
    status = request.get_json().get('status')
    menu = Menu(component=component, icon=icon, icon_type=icon_type, menu_name=menu_name, menu_type=menu_type,
                parent_id=parentId, permit_name=permit_name, remark=remark, order=order, router_key=routeName,
                router_name=menu_name, router_path=routePath, hide_menu=hideInMenu, status=status, ctime=datetime.now())
    # if bool(Menu.query.filter_by(component=component).count()):
    #     return fail_api("路由已存在")
    db.session.add(menu)
    db.session.commit()
    return success_api(msg="保存成功")


@app_router.get("/getAllPages")
def getAllPage():
    menuList = db.session.query(Menu.router_key).filter(or_(Menu.menu_type == 1, Menu.menu_type == 2)).all()
    menus = []
    for menu in menuList:
        menus.append(menu.router_key)
    return success_api(data=menus)


@app_router.get("/getAllButtons")
def getAllButtons():
    menuList = db.session.query(Menu.router_key, Menu.id, Menu.menu_name, Menu.permit_name).filter_by(menu_type=3).all()
    data = curd.model_to_dicts(schema=ButtonSchema, data=menuList)
    return success_api(data=data)


@app_router.get("/getMenuTree")
def getMenuTree():
    menuList = Menu.query.all()
    tree_list = build_category_tree(menuList)

    def category_to_dict(category):
        return {
            'id': category.id,
            'label': category.menu_name,
            'pId': category.parent_id,
            'children': [category_to_dict(child) for child in getattr(category, 'children', [])]
        }

    tree_dict = [category_to_dict(root) for root in tree_list]

    return success_api(data=tree_dict)


@app_router.get("/deleteMenu")
def deleteMenuInfo():
    menuId = request.args.get('id')
    if bool(RoleMenu.query.filter_by(menu_id=menuId).count()):
        return fail_api(msg="该路由菜单绑定角色信息,无法删除，请先解绑角色信息")
    Menu.query.filter_by(id=menuId).delete()
    db.session.commit()
    return success_api(msg="删除成功")


@app_router.post("/updateMenu")
def updateMenuInfo():
    menuId = request.get_json().get('id')
    component = request.get_json().get('component')
    icon = request.get_json().get('icon')
    icon_type = request.get_json().get('iconType')
    menu_type = request.get_json().get('menuType')
    menu_name = request.get_json().get('menuName')
    parentId = request.get_json().get('parentId')
    permit_name = request.get_json().get('permitName')
    remark = request.get_json().get('remark')
    hideInMenu = request.get_json().get('hideInMenu')
    order = request.get_json().get('order')
    routeName = request.get_json().get('routeName')
    routePath = request.get_json().get('routePath')
    status = request.get_json().get('status')
    Menu.query.filter_by(id=menuId).update(
        {
            "component": component,
            "icon": icon,
            "icon_type": icon_type,
            "menu_name": menu_name,
            "menu_type": menu_type,
            "parent_id": parentId,
            "permit_name": permit_name,
            "remark": remark,
            "order": order,
            "router_key": routeName,
            "router_name": menu_name,
            "router_path": routePath,
            "hide_menu": hideInMenu,
            "status": status
        }
    )
    db.session.commit()
    return success_api(msg="修改成功")
