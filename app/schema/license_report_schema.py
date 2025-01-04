from marshmallow import fields

from app.extensions.init_sqlalchemy import ma


class LicenseReportSchema(ma.Schema):
    id = fields.Int(dump_only=True, attribute='id')
    licenseId = fields.Str(required=True, attribute='license_id')
    issuanceTime = fields.Str(required=True, attribute='issuance_time')
    licenseType = fields.Str(required=True, attribute='license_type')
    licenseCategory = fields.Str(required=True, attribute='license_category')
    licenseCompany = fields.Str(required=True, attribute='license_company')
    companyName = fields.Str(required=True, attribute='company_name')
    taxIdentificationNumber = fields.Str(required=True, attribute='tax_identification_number')
    factoryRegistrationNumber = fields.Str(required=True, attribute='factory_registration_number')
    factoryAddress = fields.Str(required=True, attribute='factory_address')
    companyAddress = fields.Str(required=True, attribute='company_address')
    details = fields.Str(required=True, attribute='details')
    ctime = fields.Str(required=True, attribute='ctime')
    mtime = fields.Str(required=True, attribute='mtime')
