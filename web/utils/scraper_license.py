import os
from datetime import datetime

import requests
from flask_mail import Message
from lxml import etree

from web.extensions.init_mail import mail
from web.models.models import LicenseReport, AftLicense, MorLicenses


def init_header() -> dict:
    return {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'https://appdb.tisi.go.th',
        'Referer': 'https://appdb.tisi.go.th/tis_dev/p4_license_report/p4license_report.php',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0',
    }


class scraper_license:

    def __init__(self):
        self.init_url = "https://appdb.tisi.go.th/tis_dev/p4_license_report/p4license_report.php"
        self.headers = init_header()

    def post_request(self, data: dict) -> str:
        response = requests.post(self.init_url, headers=self.headers, data=data)
        if response.status_code == 200:
            file_path = os.path.dirname(os.getcwd())

            download_file = os.path.join(file_path, "file", "p4license_report.php")
            with open(download_file, "w", encoding="utf-8") as fp:
                fp.write(response.text)
                fp.close()
        return download_file

    """
      解析首页数据信息
    """

    def parse_html(self, filePath: str) -> list[LicenseReport]:
        with open(filePath, "r", encoding="utf-8") as file:  # 替换为文件实际编码，如 'gbk'
            content = file.read()
        # 使用 lxml 的 HTML 解析器解析内容
        parser = etree.HTMLParser()
        tree = etree.HTML(content, parser)
        tr_list = tree.xpath('//*[@id="table1"]/tbody/tr')
        license_list = []
        for tr in tr_list:
            license_id = tr.xpath('./td[1]/text()')[0]  # 许可证
            issuance_time = tr.xpath('./td[3]/text()')[0]  # 许可证发布时间
            license_type = tr.xpath('./td[4]/text()')[0]  # 编号
            license_company = tr.xpath('./td[5]/text()')[0]  # 编号
            licenses = LicenseReport(license_id=license_id, issuance_time=issuance_time, license_type=license_type,
                                     license_company=license_company)
            license_list.append(licenses)
        return license_list

    """
      解析详情页数据信息
    """

    def get_license_detail(self, data: dict) -> LicenseReport:
        response = requests.post('https://a.tisi.go.th/l/', headers=self.headers, data=data, timeout=5)
        if response.status_code != 200:
            return LicenseReport()
        tree = etree.HTML(response.text, etree.HTMLParser())
        license_category = tree.xpath("//div[@class='panel panel-success']//div[4]/font/text()")
        tax_identification_number = tree.xpath("//div[@class='panel panel-success']//div[6]/font/text()")
        company_address = tree.xpath("//div[@class='panel panel-success']//div[7]/font/text()")
        company_name = tree.xpath("//div[@class='panel panel-success']//div[8]/font/text()")
        factory_registration_number = tree.xpath("//div[@class='panel panel-success']//div[9]/font/text()")
        factory_address = tree.xpath("//div[@class='panel panel-success']//div[10]/font/text()")
        detail = tree.xpath("//div[@class='panel panel-success']//div[13]/font//text()")
        text = []
        if detail is not None:
            for i in detail:
                if i.find("\t") == -1:
                    text.append(i.replace("\r\n", " ").replace("\r", " "))
        licenses_detail = "\n".join(text)
        print(
            f"类别:{license_category},税号:{tax_identification_number},公司名称:{company_name},公司地址:{company_address},注册地址：{factory_registration_number},工厂地址:{factory_address}")
        return LicenseReport(license_category=license_category if len(license_category) != 0 else None,
                             tax_identification_number=tax_identification_number if len(
                                 tax_identification_number) != 0 else None,
                             company_name=company_name if len(company_name) != 0 else None,
                             company_address=company_address if len(company_address) != 0 else None,
                             factory_address=factory_address[0] if len(factory_address) != 0 else None,
                             factory_registration_number=factory_registration_number[0] if len(
                                 factory_registration_number) != 0 else None,
                             details=licenses_detail if licenses_detail is not None else None
                             )


def sendEmail(user, result):
    from app import app
    if result.__class__ == AftLicense:
        title = f'TISI Alert:{result.aft_type}/{user.nickname} Adaptor have update!'
        body = (f'----------------------------\n'
                f'Remark : {result.remark} \n'
                f'Client :{user.nickname}\n '
                f'{result.aft_type} No : {result.apply_number} \n'
                f'Current Status : {result.apply_status} \n'
                f'Current Date : {datetime.now()} \n'
                f'Quickly Check : https://sso.tisi.go.th/login \n'
                f'Account Number: {user.username}, \n')
    elif result.__class__ == MorLicenses:
        title = f'TISI Alert:{result.mor_type}/{user.nickname} Mor have update!'
        body = (f'----------------------------\n'
                f'Remark : {result.remark} \n'
                f'Client :{user.nickname}\n '
                f'{result.mor_type} No : {result.apply_number} \n'
                f'----------------------------\n'
                f'Current Status : {result.apply_status} \n'
                f'Current Date : {datetime.now()} \n'
                f'Quickly Check : https://sso.tisi.go.th/login \n'
                f'Account Number: {user.username}, \n'
                )
    else:
        title = f'TISI Alert:NSW/{user.nickname} have update!'
        body = (f'----------------------------\n'
                f'Remark : {result.remark} \n'
                f'Client :{user.nickname}\n '
                f'NSW No : {result.apply_number} \n'
                f'----------------------------\n'
                f'Current Status : {result.apply_status} \n'
                f'Current Date : {datetime.now()} \n'
                f'Quickly Check : https://sso.tisi.go.th/login \n'
                f'Account Number: {user.username}, \n'
                )
    app.logger.info(f"邮件发送成功信息:{title},{body}")
    message = Message(subject=title, recipients=[user.email], body=body)
    mail.send(message)