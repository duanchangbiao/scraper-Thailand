import type { GeneratedRoute } from '@elegant-router/types';

export const generatedRoutes: GeneratedRoute[] = [
  {
    name: '403',
    path: '/403',
    component: 'layout.blank$view.403',
    meta: {
      title: '403',
      i18nKey: 'route.403',
      constant: true,
      hideInMenu: true
    }
  },
  {
    name: '404',
    path: '/404',
    component: 'layout.blank$view.404',
    meta: {
      title: '404',
      i18nKey: 'route.404',
      constant: true,
      hideInMenu: true
    }
  },
  {
    name: '500',
    path: '/500',
    component: 'layout.blank$view.500',
    meta: {
      title: '500',
      i18nKey: 'route.500',
      constant: true,
      hideInMenu: true
    }
  },
  {
    name: 'business',
    path: '/business',
    component: 'layout.base',
    meta: {
      title: 'business',
      i18nKey: 'route.business'
    },
    children: [
      {
        name: 'business_aft',
        path: '/business/aft',
        component: 'view.business_aft',
        meta: {
          title: 'business_aft',
          i18nKey: 'route.business_aft'
        }
      },
      {
        name: 'business_mor',
        path: '/business/mor',
        component: 'view.business_mor',
        meta: {
          title: 'business_mor',
          i18nKey: 'route.business_mor'
        }
      },
      {
        name: 'business_nsw',
        path: '/business/nsw',
        component: 'view.business_nsw',
        meta: {
          title: 'business_nsw',
          i18nKey: 'route.business_nsw'
        }
      }
    ]
  },
  {
    name: 'company-info',
    path: '/company-info',
    component: 'layout.base$view.company-info',
    meta: {
      title: 'company-info',
      i18nKey: 'route.company-info'
    }
  },
  {
    name: 'home',
    path: '/home',
    component: 'layout.base$view.home',
    meta: {
      title: 'home',
      i18nKey: 'route.home'
    }
  },
  {
    name: 'iframe-page',
    path: '/iframe-page/:url',
    component: 'layout.base$view.iframe-page',
    props: true,
    meta: {
      title: 'iframe-page',
      i18nKey: 'route.iframe-page',
      constant: false,
      hideInMenu: true,
      keepAlive: true
    }
  },
  {
    name: 'login',
    path: '/login/:module(pwd-login|code-login|register|reset-pwd|bind-wechat)?',
    component: 'layout.blank$view.login',
    props: true,
    meta: {
      title: 'login',
      i18nKey: 'route.login',
      constant: true,
      hideInMenu: true
    }
  },
  {
    name: 'manage',
    path: '/manage',
    component: 'layout.base',
    meta: {
      title: 'manage',
      i18nKey: 'route.manage'
    },
    children: [
      {
        name: 'manage_menu',
        path: '/manage/menu',
        component: 'view.manage_menu',
        meta: {
          title: 'manage_menu',
          i18nKey: 'route.manage_menu'
        }
      },
      {
        name: 'manage_role',
        path: '/manage/role',
        component: 'view.manage_role',
        meta: {
          title: 'manage_role',
          i18nKey: 'route.manage_role'
        }
      },
      {
        name: 'manage_user',
        path: '/manage/user',
        component: 'view.manage_user',
        meta: {
          title: 'manage_user',
          i18nKey: 'route.manage_user'
        }
      },
      {
        name: 'manage_user-detail',
        path: '/manage/user-detail/:id',
        component: 'view.manage_user-detail',
        meta: {
          title: 'manage_user-detail',
          i18nKey: 'route.manage_user-detail'
        }
      }
    ]
  },
  {
    name: 'task',
    path: '/task',
    component: 'layout.base',
    meta: {
      title: 'task',
      i18nKey: 'route.task'
    },
    children: [
      {
        name: 'task_job',
        path: '/task/job',
        component: 'view.task_job',
        meta: {
          title: 'task_job',
          i18nKey: 'route.task_job'
        }
      },
      {
        name: 'task_job-log',
        path: '/task/job-log',
        component: 'view.task_job-log',
        meta: {
          title: 'task_job-log',
          i18nKey: 'route.task_job-log'
        }
      }
    ]
  },
  {
    name: 'user-center',
    path: '/user-center',
    component: 'layout.base$view.user-center',
    meta: {
      title: 'user-center',
      i18nKey: 'route.user-center'
    }
  }
];
