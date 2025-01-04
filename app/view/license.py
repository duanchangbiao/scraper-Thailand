import datetime

from flask import Blueprint, request
from pymysql import DataError

from app.common import curd
from app.common.helper import ModelFilter
from app.extensions.init_sqlalchemy import db
from app.models.models import LicenseReport
from app.schema.license_report_schema import LicenseReportSchema
from app.utils.response import table_api, success_api
from app.utils.scraper_license import scraper_license

app_router = Blueprint('license', __name__, url_prefix='/license')


@app_router.get('/list')
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
def save_license():
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
        print(license_report.__str__())
        if not bool(license_report.query.filter_by(license_id=license.license_id).count()):
            db.session.add(license_report)
            db.session.commit()

    return success_api(msg="添加成功")


@app_router.post('/save_report')
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
