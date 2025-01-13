import {transformRecordToOption} from '@/utils/common';

export const enableStatusRecord: Record<Api.Common.EnableStatus, App.I18n.I18nKey> = {
  '1': 'page.manage.common.status.enable',
  '2': 'page.manage.common.status.disable'
};


export const userTypeRecord: Record<Api.Common.UserType, App.I18n.I18nKey> = {
  '1': 'page.manage.common.userType.admin',
  '2': 'page.manage.common.userType.common'
};

export const enableMorStatusRecord: Record<Api.Common.EnableMorStatus, App.I18n.I18nKey> = {
  'Mor5': 'page.business_mor.status.mor5',
  'Mor9': 'page.business_mor.status.mor9'
};
export const enableATFStatusRecord: Record<Api.Common.EnableATFStatus, App.I18n.I18nKey> = {
  'AFT': 'page.business_aft.status.aft',
  'AFFA': 'page.business_aft.status.affa'
}
export const userTypeOptions = transformRecordToOption(userTypeRecord);
export const enableActiveRecord: Record<Api.Common.EnableActive, App.I18n.I18nKey> = {
  1: 'page.manage.common.active.enable',
  0: 'page.manage.common.active.disable'
};

export const enableStatusOptions = transformRecordToOption(enableStatusRecord);
export const enableMorStatusOptions = transformRecordToOption(enableMorStatusRecord);
export const enableATFStatusOptions = transformRecordToOption(enableATFStatusRecord);

export const userGenderRecord: Record<Api.SystemManage.UserGender, App.I18n.I18nKey> = {
  '1': 'page.manage.user.gender.male',
  '2': 'page.manage.user.gender.female'
};

export const userGenderOptions = transformRecordToOption(userGenderRecord);

export const userActiveOptions = transformRecordToOption(enableActiveRecord);

export const menuTypeRecord: Record<Api.SystemManage.MenuType, App.I18n.I18nKey> = {
  '1': 'page.manage.menu.type.directory',
  '2': 'page.manage.menu.type.menu'
};

export const menuTypeOptions = transformRecordToOption(menuTypeRecord);

export const menuIconTypeRecord: Record<Api.SystemManage.IconType, App.I18n.I18nKey> = {
  '1': 'page.manage.menu.iconType.iconify',
  '2': 'page.manage.menu.iconType.local'
};

export const menuIconTypeOptions = transformRecordToOption(menuIconTypeRecord);
