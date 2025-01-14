/**
 * Namespace Api
 *
 * All backend api type
 */
declare namespace Api {
  namespace Common {
    import UserActive = Api.SystemManage.UserActive;

    /** common params of paginating */
    interface PaginatingCommonParams {
      /** current page number */
      current: number;
      /** page size */
      size: number;
      /** total count */
      total: number;
    }

    /** common params of paginating query list data */
    interface PaginatingQueryRecord<T = any> extends PaginatingCommonParams {
      records: T[];
    }

    /** common search params of table */
    type CommonSearchParams = Pick<Common.PaginatingCommonParams, 'current' | 'size'>;

    /**
     * enable status
     *
     * - "1": enabled
     * - "2": disabled
     */
    type EnableStatus = '1' | '2';

    type EnableMorStatus = 'Mor5' | 'Mor9';

    type EnableATFStatus = 'AFT' | 'AFFA'

    type UserType = '1' | '2';

    type EnableActive = 1 | 0;

    /** common record */
    type CommonRecord<T = any> = {
      /** record id */
      id: number;
      /** record creator */
      createBy: string;
      /** record create time */
      createTime: string;
      /** record updater */
      updateBy: string;
      /** record update time */
      updateTime: string;
      isActive: UserActive;
      /** record status */
      status: EnableStatus;
    } & T;
  }

  /**
   * Namespace Auth
   *
   * Backend api module: "auth"
   */
  namespace Auth {
    interface LoginToken {
      token: string;
      refreshToken: string;
    }

    interface UserInfo {
      userId: string;
      userName: string;
      roles: string[];
      buttons: string[];
    }
  }

  /**
   * Namespace Route
   *
   * Backend api module: "route"
   */
  namespace Route {
    type ElegantConstRoute = import('@elegant-router/types').ElegantConstRoute;

    interface MenuRoute extends ElegantConstRoute {
      id: string;
    }

    interface UserRoute {
      routes: MenuRoute[];
      home: import('@elegant-router/types').LastLevelRouteKey;
    }
  }

  /**
   * namespace SystemManage
   *
   * backend api module: "systemManage"
   */
  namespace SystemManage {
    /** role */
    type Role = Common.CommonRecord<{
      /** role name */
      roleName: string;
      /** role code */
      roleCode: string;
      /** role description */
      remark: string;
      status: string
      roleId: number;
    }>;

    /** role search params */
    type RoleSearchParams = Partial<
      Pick<Api.SystemManage.Role, 'roleName' | 'roleCode' | 'status'> & Common.CommonSearchParams
    >;

    type DictType = Common.CommonRecord<{
      /** role name */
      dictName: string;
      /** role code */
      id: string;
    }>;


    type RoleDeleteParams = Partial<
      Pick<Api.SystemManage.Role, 'roleId'> & Common.CommonSearchParams
    >;
    /** role list */
    type RoleList = Common.PaginatingQueryRecord<Role>;

    /** all role */
    type AllRole = Pick<Role, 'roleId' | 'roleName' | 'roleCode' | 'status'>;

    /**
     * user gender
     *
     * - "1": "male"
     * - "2": "female"
     */
    type UserGender = '1' | '2';

    type UserActive = true | false;

    /** user */
    type User = Common.CommonRecord<{
      id: number;
      username: string;
      password: string;
      nickname: string;
      email: string;
      userType: string;
      phone: string;
      sex: UserGender;
      isActive: UserActive;
      createTime: string;
      updateTime: string;
      userBusiness: [];
      userRole: {
        roleId: number;
        roleName: string;
        roleCode: string;
      };
    }>;

    /** user search params */
    type UserSearchParams = Partial<
      Pick<Api.SystemManage.User, 'username' | 'email' | 'isActive' | 'status' | 'nickname'> &
      Common.CommonSearchParams
    >;

    /** user list */
    type UserList = Common.PaginatingQueryRecord<User>;

    /**
     * menu type
     *
     * - "1": directory
     * - "2": menu
     */
    type MenuType = '1' | '2';

    type MenuButton = {
      /**
       * button code
       *
       * it can be used to control the button permission
       */
      code: string;
      /** button description */
      desc: string;
    };

    /**
     * icon type
     *
     * - "1": iconify icon
     * - "2": local icon
     */
    type IconType = '1' | '2';

    type MenuPropsOfRoute = Pick<
      import('vue-router').RouteMeta,
      | 'i18nKey'
      | 'keepAlive'
      | 'constant'
      | 'order'
      | 'href'
      | 'hideInMenu'
      | 'activeMenu'
      | 'multiTab'
      | 'fixedIndexInTab'
      | 'query'
    >;

    type Menu = Common.CommonRecord<{
      /** parent menu id */
      parentId: number;
      /** menu type */
      menuType: MenuType;
      /** menu name */
      menuName: string;
      /** route name */
      routeName: string;
      /** route path */
      routePath: string;
      /** component */
      component?: string;
      /** iconify icon name or local icon name */
      icon: string;
      /** icon type */
      iconType: IconType;
      menuStatus: string;
      /** buttons */
      buttons?: MenuButton[] | null;
      /** children menu */
      children?: Menu[];
    }> &
      MenuPropsOfRoute;

    /** menu list */
    type MenuList = Common.PaginatingQueryRecord<Menu>;

    type MenuTree = {
      id: number;
      label: string;
      pId: number;
      children?: MenuTree[];
    };
  }

  namespace Company {

    import EnableStatus = Api.Common.EnableStatus;
    type CustomizeRecord<T = any> = {
      /** record id */
      id: number;
      /** record create time */
      ctime: string;
      /** record update time */
      mtime: string;
      /** record status */
      status: EnableStatus;
    } & T;
    type CompanyInfo = Company.CustomizeRecord<{
      title: string;
      companyName: string;
      companyAddress: string;
      factoryAddress: string;
      factoryRegistrationNumber: string;
      issuanceTime: string;
      licenseCategory: string;
      licenseCompany: string;
      licenseId: string;
      licenseType: string;
      taxIdentificationNumber: string;
      details: string;
      ctime: string,
      mtime: string
    }>;

    type CompanyInfoList = Common.PaginatingQueryRecord<CompanyInfo>;
    type CompanySearchParams = Partial<
      Pick<Api.Company.CompanyInfo, 'licenseId' | 'companyName' | 'taxIdentificationNumber'> &
      Common.CommonSearchParams
    >;
    type CompanyUpdateParams = Partial<Pick<Api.Company.CompanyInfo, 'licenseId'> & Common.CommonSearchParams>;
  }

  namespace Business {
    type BusinessMorInfo = Common.CommonRecord<{
      id: number;
      companyName: string;
      applyNumber: string;
      tisCode: string;
      standardName: string;
      applyLicense: string;
      applyDate: string;
      applyTaxNumber: string;
      applyStatus: string
      username: string;
      applyType: string;
      ctime: string;
      mtime: string;
    }>;

    type BusinessNewInfo = Common.CommonRecord<{
      id: string;
      operateName: string;
      applyNumber: string;
      invoice: string;
      invoiceDate: string;
      productName: string;
      rpg_group: string;
      applyStatus: string;
      applyDate: string;
      username: string;
      passTime: string;
      ctime: string;
      mtime: string;
    }>;

    type BusinessAftInfo = Common.CommonRecord<{
      id: number;
      applyNumber: string;
      tisCode: string;
      standardName: string;
      applyLicense: string;
      applyDate: string;
      applyStatus: string
      username: string;
      applyType: string;
      ctime: string;
      mtime: string;
    }>;

    type MorSearchParams = Partial<
      Pick<Api.Business.BusinessMorInfo, 'username' | 'applyStatus' | 'applyType'> &
      Common.CommonSearchParams
    >;
    type NswSearchParams = Partial<
      Pick<Api.Business.BusinessMorInfo, 'username' | 'applyStatus' | 'applyNumber'> &
      Common.CommonSearchParams
    >;
  }
}
