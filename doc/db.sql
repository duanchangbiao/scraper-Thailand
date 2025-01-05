create table sys_license_report
(
    id                          int primary key auto_increment comment '主键',
    license_id                  varchar(500) comment '许可证编号',
    issuance_time               varchar(500) comment '发证时间',
    license_type                varchar(500) comment '许可证类型',
    license_company             varchar(500) comment '授权公司',
    license_category            varchar(500) comment '类别',
    tax_identification_number   varchar(500) comment '纳税人识别号',
    company_address             varchar(500) comment '公司地址',
    factory_registration_number varchar(500) comment '注册编号',
    factory_address             varchar(500) comment '注册地址',
    ctime                       datetime comment '创建时间',
    mtime                       datetime comment '修改时间'
) engine = innodb;


create table sys_user
(
    id        int primary key auto_increment comment '主键',
    username  varchar(500) comment '用户名',
    password  varchar(500) comment '密码',
    nickname  varchar(500) comment '昵称',
    email     varchar(500) comment '邮箱',
    phone     varchar(500) comment '手机号',
    sex       varchar(500) comment '性别',
    is_active tinyint(1) comment '是否激活',
    status    char(1) comment '状态',
    ctime     datetime comment '创建时间',
    mtime     datetime comment '修改时间',
    remark    varchar(500) comment '备注'
) engine = innodb;

CREATE TABLE `sys_role`
(
    `role_id`     bigint      NOT NULL AUTO_INCREMENT COMMENT '主键',
    `role_name`   varchar(20) NOT NULL COMMENT '角色名称',
    `role_code`   varchar(500) DEFAULT NULL COMMENT '角色编码',
    `remark`      varchar(255) DEFAULT NULL COMMENT '角色描述',
    `update_time` datetime    NOT NULL COMMENT '创建时间',
    `create_time` datetime    NOT NULL COMMENT '创建时间',
    PRIMARY KEY (`role_id`) USING BTREE,
    UNIQUE KEY `role_code_uni` (`role_code`) USING BTREE
) ENGINE = InnoDB;

CREATE TABLE `sys_user_role`
(
    `id`          bigint   NOT NULL AUTO_INCREMENT,
    `role_id`     bigint   NOT NULL COMMENT '角色id',
    `user_id`     bigint   NOT NULL COMMENT '员工id',
    `update_time` datetime NOT NULL COMMENT '更新时间',
    `create_time` datetime NOT NULL COMMENT '创建时间',
    PRIMARY KEY (`id`) USING BTREE,
    UNIQUE KEY `uk_role_employee` (`role_id`, `user_id`) USING BTREE
) ENGINE = InnoDB;

create table sys_menu
(
    id          bigint not null auto_increment comment '主键',
    menu_name   varchar(255) comment '菜单名称:',
    menu_type   int comment '菜单类型:1:目录,2:菜单,3:按钮',
    parent_id   bigint comment '父级Id',
    router_key  varchar(255) comment '路由模块',
    router_name varchar(255) comment '路由名称',
    router_path varchar(255) comment '路由路径',
    status      int comment '菜单状态',
    component   varchar(255) comment '路由组件',
    icon        varchar(255) comment '图标名称',
    icon_tye    int comment 'icon类型',
    order       int comment '排序',
    permit_name varchar(255) comment '权限名称',
    ctime       datetime comment '创建时间',
    mtime       datetime comment '修改时间',
    remark      varchar(500) comment '备注',
    PRIMARY KEY (`id`) USING BTREE,
    UNIQUE KEY `uk_role_employee` (`id`, `parent_id`) USING BTREE
) engine = InnoDB;


create table sys_role_menu
(
    `id`          bigint   NOT NULL AUTO_INCREMENT,
    `role_id`     bigint   NOT NULL COMMENT '角色id',
    `menu_id`     bigint   NOT NULL COMMENT '菜单id',
    `update_time` datetime NOT NULL COMMENT '更新时间',
    `create_time` datetime NOT NULL COMMENT '创建时间',
    PRIMARY KEY (`id`) USING BTREE,
    UNIQUE KEY `uk_role_menu` (`role_id`, `menu_id`) USING BTREE
)