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
