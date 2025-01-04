from flask import Blueprint, request

from app.common import curd
from app.common.helper import ModelFilter
from app.models.models import Role
from app.schema.user_schema import RoleSchema
from app.utils.response import table_api, success_api

app_router = Blueprint('role', __name__, url_prefix="/systemManage")


@app_router.route('/getRoleList', methods=['GET'])
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

    role = (Role.filter(mf.get_filter(Role))
            .order_by(Role.role_id.asc())
            .paginates(page=current,pageSize=pageSize))
    total = role.total
    data = curd.model_to_dicts(schema=RoleSchema, data=role.items)
    return table_api(data=data, total=total, current=current, size=pageSize)


@app_router.route('getAllRoles', methods=['POST'])
def getRoleAll():
    mf = ModelFilter()
    mf.exact("status", 1)
    role = Role.query.filter(mf.get_filter(Role)).all()

    data = curd.model_to_dicts(schema=RoleSchema, data=role)
    return success_api(data=data)
