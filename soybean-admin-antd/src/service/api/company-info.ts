import {request} from '@/service/request';

//
export function fetchGetCompanyList(params?: Api.Company.CompanySearchParams) {
  return request<Api.Company.CompanyInfoList>({
    url: '/license/list',
    method: 'get',
    params
  });
}

// 更新信息
export function updateCompanyInfo(data?: Api.Company.CompanyUpdateParams) {
  return request<Api.Company.CompanyInfo>({
    url: '/license/save_report',
    method: 'post',
    data
  });
}

export function fetchGetMorList(params?: Api.Business.MorSearchParams) {
  return request<Api.Business.BusinessMorInfo>({
    url: '/mor/list',
    method: 'get',
    params
  })
}

export function updateMorInfo(data?: Api.Business.MorSearchParams) {
  return request<Api.Business.BusinessMorInfo>({
    timeout: 1000 * 60 * 3,
    url: '/mor/update',
    method: 'post',
    data
  })
}

export function fetchGetNSWList(params?: Api.Business.NswSearchParams) {
  return request<Api.Business.BusinessNewInfo>({
    url: '/nsw/list',
    method: 'get',
    params
  })
}

export function fetchAftList(params?: Api.Business.MorSearchParams) {
  return request<Api.Business.BusinessAftInfo>({
    url: '/aft/list',
    method: 'get',
    params
  })
}
