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


class Menu(db.Model):
    __tablename__ = 'sys_menu'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    menu_name = db.Column(db.String(500), comment='菜单名')
    menu_type = db.Column(db.String(500), comment='菜单类型:1:目录,2:菜单,3:按钮')
    parent_id = db.Column(db.Integer, comment='父级id')
    router_key = db.Column(db.String(500), comment='路由模块')
    router_name = db.Column(db.String(500), comment='路由名称')
    router_path = db.Column(db.String(500), comment='路由地址')
    status = db.Column(db.Integer, default=1, comment='菜单状态,1:启用,2:禁用')
    component = db.Column(db.String(500), comment='路由组件')
    icon = db.Column(db.String(500), comment='icon图标')
    icon_type = db.Column(db.String(500), comment='icon类型')
    permit_name = db.Column(db.String(500), comment='权限名称')
    order = db.Column(db.Integer, comment='排序')
    ctime = db.Column(db.DateTime, comment='创建时间')
    mtime = db.Column(db.DateTime, comment='修改时间')
    remark = db.Column(db.String(500), comment='备注')
    __table_args__ = (
        db.UniqueConstraint('menu_name', name='menu_name_unique'),
    )

    def __str__(self):
        return (f"{self.id}, "
                f"{self.menu_name}, "
                f"{self.menu_type}, "
                f"{self.parent_id}, "
                f"{self.router_key}, "
                f"{self.router_name}, "
                f"{self.router_path}, "
                f"{self.status}, "
                f"{self.component}, "
                f"{self.icon}, "
                f"{self.icon_type}, "
                f"{self.order}, "
                f"{self.ctime}, "
                f"{self.mtime}, "
                f"{self.remark}"
                )
