<script setup lang="ts">
import {computed, ref, watch} from "vue";
import {$t} from "@/locales";
import {enableStatusOptions, menuIconTypeOptions, menuTypeOptions} from "@/constants/business";
import SimpleScrollbar from "~/packages/materials/src/libs/simple-scrollbar/index.vue";
import {updateCompanyInfo} from "@/service/api/company-info";
import {message} from "ant-design-vue";

defineOptions({
  name: 'CompanyOperateModal'
});
const visible = defineModel<boolean>('visible', {
  default: false
});
export type OperateType = AntDesign.TableOperateType | 'detailsChild';

interface Props {
  /** the type of operation */
  operateType: OperateType;
  /** the edit menu data or the parent menu data when adding a child menu */
  rowData?: Api.SystemManage.Menu | null;
  /** all pages */
  allPages: string[];
}

const props = defineProps<Props>();
const title = computed(() => {
  const titles: Record<OperateType, string> = {
    add: $t('page.manage.menu.addMenu'),
    details: $t('page.company_info.detailsInfo'),
    edit: $t('page.manage.menu.editMenu')
  };
  return titles[props.operateType];
});
type Model = Pick<
  Api.Company.CompanyInfo,
  'companyName' | 'companyAddress' | 'factoryAddress' | 'factoryRegistrationNumber' | 'issuanceTime' | 'licenseCategory' |
  'licenseCompany' | 'licenseId' | 'licenseType' | 'taxIdentificationNumber' | 'details'
>;
const model = ref(createDefaultModel());

function createDefaultModel(): Model {
  return {
    companyName: '',
    companyAddress: '',
    factoryAddress: '',
    factoryRegistrationNumber: '',
    issuanceTime: '',
    licenseCategory: '',
    licenseCompany: '',
    licenseId: '',
    licenseType: '',
    taxIdentificationNumber: '',
    details: ''
  };
}

// 关闭弹框
function closeDrawer() {
  visible.value = false;
}

function handleInitModel() {
  model.value = createDefaultModel();
  if (props.operateType === 'details' && props.rowData) {
    Object.assign(model.value, props.rowData);
  }
}

// 更新表单
async function handleSubmit(licenseId:string) {
  const { error, data } = await updateCompanyInfo({ licenseId });
  if (!error) {
    // content must use function
    window.$message?.success($t('common.updateSuccess'));
  }
  closeDrawer();

}

watch(visible, () => {
  if (visible.value) {
    handleInitModel();
  }
});
</script>

<template>
  <AModal v-model:open="visible" :title="title" width="800px">
    <div class="h-480px">
      <SimpleScrollbar>
        <a-descriptions bordered>
          <a-descriptions-item :label="$t('page.company_info.licenseId')" :span="2">
            {{ model.licenseId }}
          </a-descriptions-item>
          <a-descriptions-item :label="$t('page.company_info.issuanceTime')">
            {{ model.issuanceTime }}
          </a-descriptions-item>
          <a-descriptions-item :label="$t('page.company_info.licenseType')" :span="3">
            {{ model.licenseType }}
          </a-descriptions-item>
          <a-descriptions-item :label="$t('page.company_info.licenseCategory')" :span="3">
            {{ model.licenseCategory }}
          </a-descriptions-item>
          <a-descriptions-item :label="$t('page.company_info.licenseCompany')" :span="3">
            {{ model.licenseCompany }}
          </a-descriptions-item>
          <a-descriptions-item :label="$t('page.company_info.taxIdentificationNumber')" :span="3">
            {{ model.taxIdentificationNumber }}
          </a-descriptions-item>
          <a-descriptions-item :label="$t('page.company_info.companyAddress')" :span="3">
            {{ model.companyAddress }}
          </a-descriptions-item>
          <a-descriptions-item :label="$t('page.company_info.companyName')" :span="3">
            {{ model.companyName }}
          </a-descriptions-item>
          <a-descriptions-item :label="$t('page.company_info.factoryRegistrationNumber')" :span="3">
            {{ model.factoryRegistrationNumber }}
          </a-descriptions-item>
          <a-descriptions-item :label="$t('page.company_info.factoryAddress')" :span="3">
            {{ model.factoryAddress }}
          </a-descriptions-item>
          <a-descriptions-item :label="$t('page.company_info.details')" :span="3">
            {{ model.details }}
          </a-descriptions-item>
        </a-descriptions>
      </SimpleScrollbar>
    </div>
    <template #footer>
      <ASpace justify="end" :size="16">
        <AButton @click="closeDrawer">{{ $t('common.cancel') }}</AButton>
        <AButton type="primary" @click="handleSubmit(model.licenseId)">{{ $t('common.update') }}</AButton>
      </ASpace>
    </template>
  </AModal>
</template>

<style scoped>

</style>
