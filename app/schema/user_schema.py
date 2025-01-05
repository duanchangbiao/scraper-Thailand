from marshmallow import fields

from app.extensions.init_sqlalchemy import ma


class UserRoleSchema(ma.Schema):
    id = fields.Int(dump_only=True, attribute='id')
    username = fields.Str(required=True, attribute='username')
    # password = fields.Str(required=True, attribute='password')
    nickname = fields.Str(required=True, attribute='nickname')
    email = fields.Email(required=True, attribute='email')
    phone = fields.Str(attribute='phone')
    sex = fields.Str(attribute='sex')
    status = fields.Int(required=True, attribute='status')
    isActive = fields.Int(required=True, attribute='is_active')
    createTime = fields.Str(required=True, attribute='ctime')
    updateTime = fields.Str(required=True, attribute='mtime')
    remark = fields.Str(attribute='remark')
    roleId = fields.Int(required=True, attribute='role_id')
    roleName = fields.Str(required=True, attribute='role_name')
    roleCode = fields.Str(required=True, attribute='role_code')


class RoleSchema(ma.Schema):
    id = fields.Int(dump_only=True, attribute='role_id')
    roleName = fields.Str(required=True, attribute='role_name')
    roleCode = fields.Str(required=True, attribute='role_code')
    status = fields.Str(required=True, attribute='status')
    remark = fields.Str(attribute='remark')
    createTime = fields.Str(required=True, attribute='ctime')
    updateTime = fields.Str(required=True, attribute='mtime')
