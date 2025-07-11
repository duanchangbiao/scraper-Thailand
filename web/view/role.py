import datetime

from flask import Blueprint, request
from flask_jwt_extended import jwt_required

from web.common import curd
from web.common.helper import ModelFilter
from web.extensions import db
from web.models.models import Role, RoleMenu, UserRole
from web.schema.user_schema import RoleSchema
from web.utils.response import table_api, success_api, fail_api

app_router = Blueprint('role', __name__, url_prefix="/systemManage")


@app_router.route('/getRoleList', methods=['GET'])
@jwt_required()
def getRoleList():
    current = request.args.get('current', type=int)
    pageSize = request.args.get('pagesize', type=int)
    status = request.args.get('status', type=int)
    roleName = request.args.get('roleName', type=str)
    mf = ModelFilter()
    if status:
        mf.exact("status", status)
    if roleName:
        mf.like("role_name", roleName)

    role = (Role.query.filter(mf.get_filter(Role))
            .order_by(Role.role_id.asc())
            .paginates(page=current, pageSize=pageSize))
    total = role.total
    data = curd.model_to_dicts(schema=RoleSchema, data=role.items)
    return table_api(data=data, total=total, current=current, size=pageSize)


@app_router.route('getAllRoles', methods=['POST'])
@jwt_required()
def getRoleAll():
    mf = ModelFilter()
    mf.exact("status", 1)
    role = Role.query.filter(mf.get_filter(Role)).all()

    data = curd.model_to_dicts(schema=RoleSchema, data=role)
    return success_api(data=data)


@app_router.route("/saveRole", methods=['POST'])
@jwt_required()
def saveRoleInfo():
    try:
        roleName = request.get_json().get("roleName")
        roleCode = request.get_json().get("roleCode")
        status = request.get_json().get("status")
        remark = request.get_json().get("remark")
        role = Role(role_code=roleCode, role_name=roleName, status=status, remark=remark, ctime=datetime.datetime.now())
        if not bool(role.query.filter_by(role_code=roleCode).count()):
            db.session.add(role)
            db.session.commit()
    except Exception as e:
        return fail_api(msg=f"角色信息保存失败,请检查表单是否填写正确：{e}")
    return success_api(msg="添加成功!")


@app_router.route("/updateRole", methods=["POST"])
@jwt_required()
def updateRoleInfo():
    roleId = request.get_json().get("id")
    roleName = request.get_json().get("roleName")
    roleCode = request.get_json().get("roleCode")
    status = request.get_json().get("status")
    remark = request.get_json().get("remark")
    role = Role(role_id=roleId, role_code=roleCode, role_name=roleName, status=status, remark=remark,
                mtime=datetime.datetime.now())
    Role.query.filter_by(role_id=roleId).update({
        "role_name": role.role_name,
        "status": role.status,
        "role_code": role.role_code,
        "remark": role.remark,
        "mtime": datetime.datetime.now()
    })
    db.session.commit()
    return success_api(msg='更新成功!')


@app_router.route('/deleteRole', methods=['GET'])
@jwt_required()
def deleteRole():
    roleId = request.args.get("id")
    if roleId == "1":
        return fail_api(msg="该角色为超级管理员角色，无法删除")
    if bool(UserRole.query.filter_by(role_id=roleId).count()):
        return fail_api(msg="该角色已绑定用户,无法删除，请先解绑用户")
    if bool(RoleMenu.query.filter_by(role_id=roleId).count()):
        return fail_api(msg="该角色已绑定菜单,无法删除，请先解绑菜单")
    Role.query.filter_by(role_id=roleId).delete()
    db.session.commit()
    return success_api(msg="删除成功")


@app_router.post('/getCheckMenuInfo')
@jwt_required()
def getCheckMenuInfo():
    roleId = request.get_json().get('roleId')
    roleMenu = RoleMenu.query.filter_by(role_id=roleId).all()
    data = []
    for item in roleMenu:
        data.append(item.menu_id)
    return success_api(msg='查询成功', data=data)


@app_router.post('/updateRoleMenuInfo')
@jwt_required()
def updateRoleMenuInfo():
    menuList = request.get_json().get("menuIdList")
    roleId = request.get_json().get('roleId')
    if bool(RoleMenu.query.filter_by(role_id=roleId).count()):
        RoleMenu.query.filter_by(role_id=roleId).delete()
        db.session.commit()
    for menuId in menuList:
        roleMenu = RoleMenu(menu_id=menuId, role_id=roleId, ctime=datetime.datetime.now())
        db.session.add(roleMenu)
        db.session.commit()
    return success_api(msg='添加成功!')
