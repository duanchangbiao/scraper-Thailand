from sqlalchemy.orm import relationship

from app.extensions.init_sqlalchemy import db


class LicenseReport(db.Model):
    __tablename__ = 'sys_license_report'
    id = db.Column(db.Integer, primary_key=True)
    license_id = db.Column(db.String(128), comment='许可证编号')
    issuance_time = db.Column(db.String(128), comment='许可时间')
    license_type = db.Column(db.String(500), comment='TIS编号')
    license_company = db.Column(db.String(500), comment='持牌公司')
    license_category = db.Column(db.String(500), comment='类别')
    tax_identification_number = db.Column(db.Integer, comment='纳税人识别号')
    company_address = db.Column(db.String(500), comment='公司地址')
    company_name = db.Column(db.String(500), comment='公司名称')
    factory_registration_number = db.Column(db.String(500), comment='注册登记编号')
    factory_address = db.Column(db.String(500), comment='注册登记编号')
    details = db.Column(db.String(50000), comment='详细地址')
    ctime = db.Column(db.DateTime, comment='创建时间')
    mtime = db.Column(db.DateTime, comment='修改时间')
    __table_args__ = (
        db.UniqueConstraint('license_id', name='license_id_unique'),
    )

    def __str__(self):
        return (f"{self.id}, "
                f"{self.issuance_time}, "
                f"{self.license_id}, "
                f"{self.license_type}, "
                f"{self.license_company}, "
                f"{self.license_category}. "
                f"{self.tax_identification_number},"
                f"{self.company_address},"
                f"{self.factory_registration_number},"
                f"{self.factory_address}, "
                f"{self.details}, "
                f"{self.ctime},"
                f"{self.mtime}"
                )


class User(db.Model):
    __tablename__ = 'sys_user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(500), comment='用户名')
    password = db.Column(db.String(500), comment='密码')
    nickname = db.Column(db.String(500), comment='昵称')
    email = db.Column(db.String(500), comment='邮箱')
    phone = db.Column(db.String(500), comment='手机号')
    sex = db.Column(db.String(500), comment='性别')
    is_active = db.Column(db.Boolean, comment='是否监控', default=True)
    status = db.Column(db.Integer, default=1, comment='账号状态')
    ctime = db.Column(db.DateTime, comment='创建时间')
    mtime = db.Column(db.DateTime, comment='修改时间')
    remark = db.Column(db.String(500), comment='备注')

    def __str__(self):
        return (f"{self.id}, "
                f"{self.username}, "
                f"{self.password}, "
                f"{self.nickname}, "
                f"{self.email}, "
                f"{self.phone}, "
                f"{self.sex}, "
                f"{self.is_active}, "
                f"{self.status}, "
                f"{self.ctime}, "
                f"{self.mtime},"
                )


class Role(db.Model):
    __tablename__ = 'sys_role'
    role_id = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String(500), comment='角色名')
    role_code = db.Column(db.String(500), comment='角色编码')
    status = db.Column(db.Integer, default=1, comment='角色状态,1:启用,2:禁用')
    remark = db.Column(db.String(500), comment='备注')
    ctime = db.Column(db.DateTime, comment='创建时间')
    mtime = db.Column(db.DateTime, comment='修改时间')

    def __str__(self):
        return (f"{self.role_id}, "
                f"{self.role_name}, "
                f"{self.role_code}, "
                f"{self.remark}, "
                f"{self.ctime}, "
                f"{self.mtime}"
                )


class UserRole(db.Model):
    __tablename__ = 'sys_user_role'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, comment='用户id')
    role_id = db.Column(db.Integer, comment='角色id')
    ctime = db.Column(db.DateTime, comment='创建时间')
    mtime = db.Column(db.DateTime, comment='修改时间')

    def __str__(self):
        return (f"{self.id}, "
                f"{self.user_id}, "
                f"{self.role_id}, "
                f"{self.ctime}, "
                f"{self.mtime}"
                )
