from marshmallow import fields

from web.extensions.init_sqlalchemy import ma


class UserRoleSchema(ma.Schema):
    ctime = fields.Str(attribute='ctime')
    id = fields.Int(dump_only=True, attribute='id')
    username = fields.Str(attribute='username')
    applyNumber = fields.Str(attribute='apply_number')
    applyLicense = fields.Str(attribute='apply_license')
    applyStatus = fields.Str(attribute='apply_status')
    applyDate = fields.Str(attribute='apply_date')
    applyTax = fields.Str(attribute='apply_tax')
    operateName = fields.Str(attribute='operate_name')
    standardName = fields.Str(attribute='standard_name')
    morType = fields.Str(attribute='mor_type')
    mtime = fields.Str(attribute='mtime')
    tisCode = fields.Str(attribute='tisCode')
