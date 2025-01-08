import {transformRecordToOption} from '@/utils/common';

export const yesOrNoRecord: Record<CommonType.YesOrNo, App.I18n.I18nKey> = {
  '1': 'common.yesOrNo.yes',
  '0': 'common.yesOrNo.no'
};

export const yesOrNoOptions = transformRecordToOption(yesOrNoRecord);
