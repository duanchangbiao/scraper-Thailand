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

export function updateMorStatusInfo(data?: Api.Business.BusinessMorInfo) {
  return request<Api.Business.BusinessMorInfo>({
    url: '/mor/readStatus',
    method: 'post',
    data
  })
}

export function updateReadInfo(data?: Api.Business.BusinessAftInfo) {
  return request<Api.Business.BusinessAftInfo>({
    url: '/aft/readStatus',
    method: 'post',
    data
  })
}

export function updateNswInfo(data?: Api.Business.BusinessNewInfo) {
  return request<Api.Business.BusinessNewInfo>({
    url: '/nsw/update',
    method: 'post',
    data
  })
}

export function fetchGetNSWList(params?: Api.Business.AFTSearchParams) {
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

export function fetchJobList(params?: Api.Job.JobSearchParams) {
  return request<Api.Job.jobInfo>({
    url: '/job/list',
    method: 'get',
    params
  })
}


export function executorRun(params?: { jobId: number }) {
  return request<Api.Job.jobInfo>({
    url: '/job/run',
    method: 'get',
    params
  })
}

export function deleteJob(params?: { jobId: number }) {
  return request<Api.Job.jobInfo>({
    url: '/job/delete',
    method: 'get',
    params
  })
}

export function updateJob(data?: Api.Job.JobUpdateParams) {
  return request<Api.Job.jobInfo>({
    url: '/job/update',
    method: 'post',
    data
  })
}
