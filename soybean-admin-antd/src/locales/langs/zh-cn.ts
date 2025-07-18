const local: App.I18n.Schema = {
  system: {
    title: 'Soybean 管理系统',
    updateTitle: '系统版本更新通知',
    updateContent: '检测到系统有新版本发布，是否立即刷新页面？',
    updateConfirm: '立即刷新',
    updateCancel: '稍后再说'
  },
  common: {
    action: '操作',
    add: '新增',
    addSuccess: '添加成功',
    backToHome: '返回首页',
    batchDelete: '批量删除',
    cancel: '取消',
    close: '关闭',
    check: '勾选',
    read: '已读',
    columnSetting: '列设置',
    config: '配置',
    confirm: '确认',
    delete: '删除',
    deleteSuccess: '删除成功',
    confirmDelete: '确认删除吗？',
    batchUpdate: '批量更新',
    edit: '编辑',
    execute: '执行',
    details: '详情',
    updateInfo: '更新',
    error: '错误',
    index: '序号',
    keywordSearch: '请输入关键词搜索',
    logout: '退出登录',
    logoutConfirm: '确认退出登录吗？',
    lookForward: '敬请期待',
    modify: '修改',
    modifySuccess: '修改成功',
    noData: '无数据',
    operate: '操作',
    pleaseCheckValue: '请检查输入的值是否合法',
    refresh: '刷新',
    reset: '重置',
    search: '搜索',
    switch: '切换',
    tip: '提示',
    trigger: '触发',
    update: '更新',
    isActive: "是否监控",
    updateSuccess: '更新成功',
    userCenter: '个人中心',
    yesOrNo: {
      yes: '是',
      no: '否'
    },
  },
  request: {
    logout: '请求失败后登出用户',
    logoutMsg: '用户状态失效，请重新登录',
    logoutWithModal: '请求失败后弹出模态框再登出用户',
    logoutWithModalMsg: '用户状态失效，请重新登录',
    refreshToken: '请求的token已过期，刷新token',
    tokenExpired: 'token已过期'
  },
  theme: {
    themeSchema: {
      title: '主题模式',
      light: '亮色模式',
      dark: '暗黑模式',
      auto: '跟随系统'
    },
    grayscale: '灰色模式',
    colourWeakness: '色弱模式',
    layoutMode: {
      title: '布局模式',
      vertical: '左侧菜单模式',
      'vertical-mix': '左侧菜单混合模式',
      horizontal: '顶部菜单模式',
      'horizontal-mix': '顶部菜单混合模式',
      reverseHorizontalMix: '一级菜单与子级菜单位置反转'
    },
    recommendColor: '应用推荐算法的颜色',
    recommendColorDesc: '推荐颜色的算法参照',
    themeColor: {
      title: '主题颜色',
      primary: '主色',
      info: '信息色',
      success: '成功色',
      warning: '警告色',
      error: '错误色',
      followPrimary: '跟随主色'
    },
    scrollMode: {
      title: '滚动模式',
      wrapper: '外层滚动',
      content: '主体滚动'
    },
    page: {
      animate: '页面切换动画',
      mode: {
        title: '页面切换动画类型',
        'fade-slide': '滑动',
        fade: '淡入淡出',
        'fade-bottom': '底部消退',
        'fade-scale': '缩放消退',
        'zoom-fade': '渐变',
        'zoom-out': '闪现',
        none: '无'
      }
    },
    fixedHeaderAndTab: '固定头部和标签栏',
    header: {
      height: '头部高度',
      breadcrumb: {
        visible: '显示面包屑',
        showIcon: '显示面包屑图标'
      }
    },
    tab: {
      visible: '显示标签栏',
      cache: '标签栏信息缓存',
      height: '标签栏高度',
      mode: {
        title: '标签栏风格',
        chrome: '谷歌风格',
        button: '按钮风格'
      }
    },
    sider: {
      inverted: '深色侧边栏',
      width: '侧边栏宽度',
      collapsedWidth: '侧边栏折叠宽度',
      mixWidth: '混合布局侧边栏宽度',
      mixCollapsedWidth: '混合布局侧边栏折叠宽度',
      mixChildMenuWidth: '混合布局子菜单宽度'
    },
    footer: {
      visible: '显示底部',
      fixed: '固定底部',
      height: '底部高度',
      right: '底部局右'
    },
    watermark: {
      visible: '显示全屏水印',
      text: '水印文本'
    },
    themeDrawerTitle: '主题配置',
    pageFunTitle: '页面功能',
    resetCacheStrategy: {
      title: '重置缓存策略',
      close: '关闭页面',
      refresh: '刷新页面'
    },
    configOperation: {
      copyConfig: '复制配置',
      copySuccessMsg: '复制成功，请替换 src/theme/settings.ts 中的变量 themeSettings',
      resetConfig: '重置配置',
      resetSuccessMsg: '重置成功'
    }
  },
  route: {
    login: '登录',
    403: '无权限',
    404: '页面不存在',
    500: '服务器错误',
    'iframe-page': '外链页面',
    home: '首页',
    'user-center': '个人中心',
    manage: '系统管理',
    manage_user: '用户管理',
    'manage_user-detail': '用户详情',
    manage_role: '角色管理',
    manage_menu: '菜单管理',
    exception: '异常页',
    exception_403: '403',
    exception_404: '404',
    exception_500: '500',
    'company-info': '公司地址查询',
    'business': '数据分析',
    business_mor: '数据分析模块-MOR',
    business_aft: '数据分析模块-AFT',
    business_nsw: '数据分析模块-NSW',
    'task_job-log': '任务日志',
    task_job: '定时任务',
    task: '定时任务管理',
  },
  page: {
    login: {
      common: {
        loginOrRegister: '登录 / 注册',
        userNamePlaceholder: '请输入用户名',
        phonePlaceholder: '请输入手机号',
        codePlaceholder: '请输入验证码',
        passwordPlaceholder: '请输入密码',
        confirmPasswordPlaceholder: '请再次输入密码',
        codeLogin: '验证码登录',
        confirm: '确定',
        back: '返回',
        validateSuccess: '验证成功',
        loginSuccess: '登录成功',
        welcomeBack: '欢迎回来，{userName} ！'
      },
      pwdLogin: {
        title: '密码登录',
        rememberMe: '记住我',
        forgetPassword: '忘记密码？',
        register: '注册账号',
        otherAccountLogin: '其他账号登录',
        otherLoginMode: '其他登录方式',
        superAdmin: '超级管理员',
        admin: '管理员',
        user: '普通用户'
      },
      codeLogin: {
        title: '验证码登录',
        getCode: '获取验证码',
        reGetCode: '{time}秒后重新获取',
        sendCodeSuccess: '验证码发送成功',
        imageCodePlaceholder: '请输入图片验证码'
      },
      register: {
        title: '注册账号',
        agreement: '我已经仔细阅读并接受',
        protocol: '《用户协议》',
        policy: '《隐私权政策》'
      },
      resetPwd: {
        title: '重置密码'
      },
      bindWeChat: {
        title: '绑定微信'
      }
    },
    home: {
      greeting: '早安，{userName}, 今天又是充满活力的一天!',
      weatherDesc: '今日多云转晴，20℃ - 25℃!',
      projectCount: '用户量',
      todo: '更新情况',
      message: '消息',
      downloadCount: '监控用户',
      registerCount: '监控总量',
      schedule: '作息安排',
      study: '学习',
      work: '工作',
      rest: '休息',
      entertainment: '娱乐',
      visitCount: '总量',
      turnover: '更新量',
      dealCount: '用户量',
      JobNews: {
        title: '定时任务完成情况',
        moreNews: '更多',
        jobName: '任务名称',
        complete: '任务完成情况',
        completeTime: '任务完成时间',
        jobMessage: '耗时'
      },
      creativity: '通知'
    },
    manage: {
      common: {
        status: {
          enable: '启用',
          disable: '禁用'
        },
        active: {
          enable: '监控中',
          disable: '等待监控'
        },
        userType: {
          admin: '管理员',
          common: '业务账号'
        },
        updateType: {
          enable: '有更新',
          disable: '暂未更新',
          completed: '已处理'
        }
      },
      role: {
        title: '角色列表',
        roleName: '角色名称',
        roleCode: '角色编码',
        status: '角色状态',
        remark: '角色描述',
        menuAuth: '菜单权限',
        buttonAuth: '按钮权限',
        form: {
          roleName: '请输入角色名称',
          roleCode: '请输入角色编码',
          status: '请选择角色状态',
          remark: '请输入角色描述'
        },
        addRole: '新增角色',
        editRole: '编辑角色'
      },
      user: {
        title: '用户列表',
        id: '用户id',
        username: '用户名',
        sex: '性别',
        nickname: '昵称',
        phone: '手机号',
        password: '密码',
        email: '邮箱',
        status: '用户状态',
        userType: '账号类型',
        createTime: '创建时间',
        isActive: '监控',
        businessType: '业务类型',
        updateTime: '更新时间',
        userRole: {
          roleId: '角色Id',
          roleName: '角色名称',
          roleCode: '角色CODE'
        },
        form: {
          username: '请输入用户名',
          password: '请输入密码',
          sex: '请选择性别',
          nickname: '请输入昵称',
          phone: '请输入手机号',
          email: '请输入邮箱',
          userType: '请选择账号类型',
          status: '请选择用户状态',
          isActive: '请选择监控状态',
          userRole: {
            roleId: '角色Id',
            roleName: '角色名称',
            roleCode: '角色CODE'
          }
        },
        addUser: '新增用户',
        editUser: '编辑用户',
        gender: {
          male: '男',
          female: '女'
        }
      },
      menu: {
        home: '首页',
        title: '菜单列表',
        id: 'ID',
        parentId: '父级菜单ID',
        menuType: '菜单类型',
        menuName: '菜单名称',
        routeName: '路由名称',
        query: '路由参数',
        routePath: '路由路径',
        pathParam: '路径参数',
        layout: '布局',
        page: '页面组件',
        i18nKey: '国际化key',
        icon: '图标',
        localIcon: '本地图标',
        iconTypeTitle: '图标类型',
        order: '排序',
        keepAlive: '缓存路由',
        href: '外链',
        hideInMenu: '隐藏菜单',
        activeMenu: '高亮的菜单',
        multiTab: '支持多页签',
        fixedIndexInTab: '固定在页签中的序号',
        button: '按钮',
        buttonCode: '按钮编码',
        buttonDesc: '按钮描述',
        menuStatus: '菜单状态',
        constant: '常量路由',
        form: {
          home: '请选择首页',
          menuType: '请选择菜单类型',
          menuName: '请输入菜单名称',
          routeName: '请输入路由名称',
          routePath: '请输入路由路径',
          pathParam: '请输入路径参数',
          page: '请选择页面组件',
          layout: '请选择布局组件',
          i18nKey: '请输入国际化key',
          icon: '请输入图标',
          queryKey: '请输入路由参数Key',
          queryValue: '请输入路由参数Value',
          localIcon: '请选择本地图标',
          order: '请输入排序',
          keepAlive: '请选择是否缓存路由',
          href: '请输入外链',
          hideInMenu: '请选择是否隐藏菜单',
          activeMenu: '请输入高亮的菜单的路由名称',
          multiTab: '请选择是否支持多标签',
          fixedInTab: '请选择是否固定在页签中',
          fixedIndexInTab: '请输入固定在页签中的序号',
          button: '请选择是否按钮',
          buttonCode: '请输入按钮编码',
          buttonDesc: '请输入按钮描述',
          menuStatus: '请选择菜单状态'
        },
        addMenu: '新增菜单',
        editMenu: '编辑菜单',
        addChildMenu: '新增子菜单',
        type: {
          directory: '目录',
          menu: '菜单'
        },
        iconType: {
          iconify: 'iconify图标',
          local: '本地图标'
        }
      }
    },
    company_info: {
      title: '工业产品标准许可证信息',
      companyName: '工厂名称',
      companyAddress: '公司地址',
      factoryAddress: '工厂地址',
      factoryRegistrationNumber: '工厂注册号',
      issuanceTime: '发放日期',
      licenseCategory: '类别',
      licenseCompany: '授权公司',
      licenseId: '许可证编号',
      licenseType: 'TIS编号',
      taxIdentificationNumber: '纳税人标识',
      ctime: '创建时间',
      mtime: '修改时间',
      details: '说明',
      form: {
        companyName: '请输入工厂名称',
        licenseId: '请输入许可证编号',
        taxIdentificationNumber: '请输入纳税人标识'
      },
      detailsInfo: '详情信息'
    },
    business_mor: {
      id: '编号',
      title: 'MOR 模块数据中心',
      companyName: '操作人',
      applyNumber: '申请编号',
      tisCode: 'TIS CODE',
      standardName: '标准信息',
      applyLicense: '申请许可证',
      applyDate: '申请日期',
      applyTaxNumber: '税号',
      updateType: '更新状态',
      applyStatus: '申请状态',
      username: '账号信息',
      applyType: '类型',
      ctime: '创建时间',
      mtime: '更新时间',
      status: {
        mor5: 'Mor5',
        mor9: 'Mor9',
      },
      remark: '备注',
      nickname: '昵称',
      form: {
        companyName: '请输入操作人信息',
        applyNumber: '请输入申请编号',
        tisCode: '请输入TIS Code 信息',
        standardName: '请输入标准信息',
        applyLicense: '请输入申请许可证',
        applyDate: '请输入申请日期',
        applyTaxNumber: '请输入税号',
        applyStatus: '请输入申请状态',
        applyType: '请选择类型',
        username: '请输入账号信息',
        remark: '请输入备注信息'
      },
    },
    business_nsw: {
      id: '编号',
      title: 'NSW 模块数据中心',
      operateName: '操作人',
      applyNumber: '申请编号',
      invoice: '发票',
      invoiceDate: '发票日期',
      productNumber: '产品数量',
      applyDate: '申请日期',
      rpg_group: '责任小组',
      applyStatus: '申请状态',
      username: '账号信息',
      nickname: '昵称',
      passDate: '通过时间',
      ctime: '创建时间',
      mtime: '更新时间',
      form: {
        operateName: '请输入操作人信息',
        applyNumber: '请输入申请编号',
        invoice: '请输入TIS Code 信息',
        productName: '请输入标准信息',
        invoiceDate: '请输入申请许可证',
        applyDate: '请输入申请日期',
        rpg_group: '请输入税号',
        applyStatus: '请输入申请状态',
        username: '请输入账号信息',
      },
    },
    business_aft: {
      id: '编号',
      title: 'AFT/AFFA 模块数据中心',
      applyNumber: '申请编号',
      tisCode: 'TIS CODE',
      standardName: '标准信息',
      applyLicense: '申请许可证',
      applyDate: '申请日期',
      applyStatus: '申请状态',
      username: '账号信息',
      nickname: '昵称',
      applyType: '类型',
      updateType: '更新状态',
      sort: '排序数字',
      remark: '备注信息',
      passTime: '通过时间',
      ctime: '创建时间',
      mtime: '更新时间',
      status: {
        affa: 'AFFA',
        aft: 'AFT',
      },
      form: {
        applyStatus: '请输入申请状态',
        applyType: '请选择类型',
        username: '请输入账号信息',
        sort: '请输入排序数字',
        updateType: '请选择更新内容',
        remark: '请输入备注信息',
      },
    },
    JobInfo: {
      title: "任务中心",
      jobName: "任务名称",
      jobId: '任务id',
      jobGroup: '任务组',
      status: '任务状态',
      invokeTarget: '目标函数',
      cronExpression: 'cron表达式',
      form: {
        jobName: '请输入任务名称',
        jobGroup: '请输入任务组',
        status: '请输入任务状态',
        invokeTarget: '请输入目标函数',
        cronExpression: '请输入cron表达式',
      }
    },
    JobLog: {
      title: '任务日志',
      jobName: '任务名称',
      jobGroup: '任务组',
      jobLogId: '任务日志id',
      jobMessage: '任务消息',
      status: '状态',
      invokeTarget: '目标函数',
      exceptionInfo: "异常信息",
      createTime: '创建时间',
    }
  },
  form: {
    required: '不能为空',
    userName: {
      required: '请输入用户名',
      invalid: '用户名格式不正确'
    },
    phone: {
      required: '请输入手机号',
      invalid: '手机号格式不正确'
    },
    pwd: {
      required: '请输入密码',
      invalid: '密码格式不正确，6-18位字符，包含字母、数字、下划线'
    },
    confirmPwd: {
      required: '请输入确认密码',
      invalid: '两次输入密码不一致'
    },
    code: {
      required: '请输入验证码',
      invalid: '验证码格式不正确'
    },
    email: {
      required: '请输入邮箱',
      invalid: '邮箱格式不正确'
    }
  },
  dropdown: {
    closeCurrent: '关闭',
    closeOther: '关闭其它',
    closeLeft: '关闭左侧',
    closeRight: '关闭右侧',
    closeAll: '关闭所有'
  },
  icon: {
    themeConfig: '主题配置',
    themeSchema: '主题模式',
    lang: '切换语言',
    fullscreen: '全屏',
    fullscreenExit: '退出全屏',
    reload: '刷新页面',
    collapse: '折叠菜单',
    expand: '展开菜单',
    pin: '固定',
    unpin: '取消固定'
  }
};

export default local;
