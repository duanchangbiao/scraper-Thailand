import datetime

from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from pymysql import DataError


from web.common import curd
from web.common.helper import ModelFilter
from web.extensions.init_sqlalchemy import db
from web.models.models import LicenseReport
from web.schema.license_report_schema import LicenseReportSchema
from web.utils.response import table_api, success_api
from web.utils.scraper_license import scraper_license

app_router = Blueprint('license', __name__, url_prefix='/license')


@app_router.get('/list')
@jwt_required()
def get_license():
    size = request.args.get("size", type=int)
    current = request.args.get("current", type=int)
    licenseId = request.args.get("licenseId")
    companyName = request.args.get("companyName")
    taxIdentificationNumber = request.args.get("taxIdentificationNumber")
    mf = ModelFilter()
    if licenseId:
        mf.exact("license_id", licenseId)
    if companyName:
        mf.like("company_name", companyName)
    if taxIdentificationNumber:
        mf.exact('tax_identification_number', taxIdentificationNumber)

    license_report = LicenseReport.query.filter(mf.get_filter(LicenseReport)).order_by(
        LicenseReport.mtime.desc()).paginates(page=current, pageSize=size)
    count = license_report.total
    data = curd.model_to_dicts(schema=LicenseReportSchema, data=license_report.items)
    return table_api(data=data, current=current, msg="查询成功", size=size, total=count)


@app_router.route('/save', methods=["POST"])
@jwt_required()
def save_license():
    from app import app
    data = {
        'data': 'permit',
        'txt_tis': '/',
    }
    scraper = scraper_license()
    file_path = scraper.post_request(data)
    licenses = scraper.parse_html(file_path)
    for license in licenses:
        license_report = LicenseReport(
            license_id=license.license_id,
            license_company=license.license_company,
            license_type=license.license_type,
            issuance_time=license.issuance_time.strip(),
            ctime=datetime.datetime.now()
        )
        if not bool(license_report.query.filter_by(license_id=license.license_id).count()):
            db.session.add(license_report)
            db.session.commit()
        app.logger.info(f"save success:{license_report}")
    return success_api(msg="添加成功")


@app_router.post('/save_report')
@jwt_required()
def save_license_report():
    licenseId = request.get_json().get("licenseId")
    scraper = scraper_license()
    licenses = scraper.get_license_detail({
        'n': licenseId,
    })
    try:
        LicenseReport.query.filter_by(license_id=licenseId).update({
            "license_category": licenses.license_category,
            "factory_address": licenses.factory_address,
            "factory_registration_number": licenses.factory_registration_number,
            "company_address": licenses.company_address,
            "company_name": licenses.company_name,
            "tax_identification_number": licenses.tax_identification_number,
            "details": licenses.details,
            "mtime": datetime.datetime.now()
        })
        db.session.commit()
        result = db.session.query(LicenseReport).filter_by(license_id=licenseId)
        response = curd.model_to_dicts(schema=LicenseReportSchema, data=result)
    except DataError as e:
        print(f"数据更新产生异常:{e}")
        raise

    return success_api(msg="修改成功", data=response)
