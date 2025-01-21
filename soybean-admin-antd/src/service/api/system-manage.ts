import {request} from '../request';

/** get role list */
export function fetchGetRoleList(params?: Api.SystemManage.RoleSearchParams) {
  return request<Api.SystemManage.RoleList>({
    url: '/systemManage/getRoleList',
    method: 'get',
    params
  });
}

/**
 * get all roles
 *
 * these roles are all enabled
 */
export function fetchGetAllRoles() {
  return request<Api.SystemManage.AllRole[]>({
    url: '/systemManage/getAllRoles',
    method: 'post'
  });
}

export function fetchDictOptions() {
  return request<Api.SystemManage.DictType[]>({
    url: '/systemManage/getBusinessDict',
    method: 'get'
  })
}

/** get user list */
export function fetchGetUserList(params?: Api.SystemManage.UserSearchParams) {
  return request<Api.SystemManage.UserList>({
    url: '/systemManage/getUserList',
    method: 'get',
    params
  });
}

/** get menu list */
export function fetchGetMenuList() {
  return request<Api.SystemManage.MenuList>({
    url: '/systemManage/getMenuList',
    method: 'get'
  });
}

/** get all pages */
export function fetchGetAllPages() {
  return request<string[]>({
    url: '/systemManage/getAllPages',
    method: 'get'
  });
}

export function fetchGetAllButtons() {
  return request<string[]>({
    url: '/systemManage/getAllButtons',
    method: 'get'
  });
}

/** get menu tree */
export function fetchGetMenuTree() {
  return request<Api.SystemManage.MenuTree[]>({
    url: '/systemManage/getMenuTree',
    method: 'get'
  });
}

/** 保存用户信息 */
export function insertSaveUserInfo(data: Api.SystemManage.User) {
  return request<Api.SystemManage.User>({
    url: '/systemManage/saveUser',
    method: 'post',
    data
  });
}

export function updateUserInfo(data: Api.SystemManage.User) {
  return request<Api.SystemManage.User>({
    url: '/systemManage/updateUser',
    method: 'post',
    data
  })
}

export function insertSaveRoleInfo(data: Api.SystemManage.Role) {
  return request<Api.SystemManage.Role>({
    url: '/systemManage/saveRole',
    method: 'post',
    data
  })
}

export function updateRoleInfo(data: Api.SystemManage.Role) {
  return request<Api.SystemManage.Role>({
    url: '/systemManage/updateRole',
    method: 'post',
    data
  })
}

export function deleteRoleInfo(params: Api.SystemManage.RoleDeleteParams) {
  return request<Api.SystemManage.Role>({
    url: '/systemManage/deleteRole',
    method: 'get',
    params
  })
}

export function insertSaveMenuInfo(data: Api.SystemManage.Menu) {
  return request<Api.SystemManage.Menu>({
    url: '/systemManage/saveMenu',
    method: 'post',
    data
  })
}

export function updateMenuInfo(data: Api.SystemManage.Menu) {
  return request<Api.SystemManage.Menu>({
    url: '/systemManage/updateMenu',
    method: 'post',
    data
  })
}


export function getCheckMenuInfo(data: { roleId: number }) {
  return request<number[]>({
    url: '/systemManage/getCheckMenuInfo',
    method: 'post',
    data
  })
}


export function updateRoleMenuInfo(data: { roleId: number, menuIdList: number[] }) {
  return request<string>({
    url: '/systemManage/updateRoleMenuInfo',
    method: 'post',
    data
  })
}


export function deleteMenuInfo(params: { id: number }) {
  return request<Api.SystemManage.Menu>({
    url: '/systemManage/deleteMenu',
    method: 'get',
    params
  })
}

export function deleteUserInfo(params: { id: number, userType: string }) {
  return request<Api.SystemManage.User>({
    url: '/systemManage/deleteUser',
    method: 'get',
    params
  })
}

export function updateUserScraperInfo(params: { id: number, userType: number }) {
  return request<Api.SystemManage.User>({
    timeout: 1000 * 60 * 10,
    url: '/systemManage/updateUserScraper',
    method: 'get',
    params
  })
}
