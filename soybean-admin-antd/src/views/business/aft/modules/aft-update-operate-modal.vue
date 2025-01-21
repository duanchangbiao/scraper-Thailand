<script setup lang="tsx">

import {$t} from "@/locales";
import {computed, ref, watch} from "vue";
import {updateReadInfo} from "@/service/api/company-info";

defineOptions({
  name: 'AftUpdateOperateModal'
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
    edit: $t('page.manage.menu.editMenu')
  };
  return titles[props.operateType];
});
const model = ref(createDefaultModel());

function createDefaultModel(): Api.Business.BusinessAftInfo {
  return {
    id: '',
    updateType: '',
    remark: '',
    sort: '',
  };
}

function closeDrawer() {
  visible.value = false;
}

function handleInitModel() {
  model.value = createDefaultModel();
  console.log(model)
  if (props.operateType === 'edit' && props.rowData) {
    Object.assign(model.value, props.rowData);
  }
}

async function handleSubmit() {
  const {error, response} = await updateReadInfo(model.value);
  if (!error) {
    // content must use function
    window.$message?.success($t('common.updateSuccess'));

  }
  closeDrawer();

}

const updateOptions = ref<CommonType.Option<string>[]>([]);

function getUpdateOptions() {
  updateOptions.value = [
    {
      label: '有更新',
      value: '2',
    },
    {
      label: '暂未更新',
      value: '1',
    },
    {
      label: '已处理',
      value: '3',
    },
  ];
}

watch(visible, () => {
  if (visible.value) {
    handleInitModel();
    getUpdateOptions();
  }
});
</script>

<template>
  <AModal v-model:open="visible" :title="title" width="500px">
    <div class="h-280px">
      <SimpleScrollbar>
        <AForm
          ref="formRef"
          layout="horizontal"
          :model="model"
          :label-col="{ span: 5 }"
          :wrapper-col="{ span: 15 }"
        >
          <AFormItem :label="$t('page.business_aft.updateType')" name="updateType">
            <a-select
              ref="select"
              v-model:value="model.updateType"
              style="width: 180px"
              :options="updateOptions"
            ></a-select>
          </AFormItem>
          <AFormItem :label="$t('page.business_aft.sort')" name="roleName">
            <AInput v-model:value="model.sort" :placeholder="$t('page.business_aft.form.sort')"/>
          </AFormItem>
          <AFormItem :label="$t('page.business_aft.remark')" name="roleName">
            <AInput v-model:value="model.remark" :placeholder="$t('page.business_aft.form.remark')"/>
          </AFormItem>
        </AForm>
      </SimpleScrollbar>
    </div>
    <template #footer>
      <ASpace justify="end" :size="16">
        <AButton @click="closeDrawer">{{ $t('common.cancel') }}</AButton>
        <AButton type="primary" @click="handleSubmit()">{{ $t('common.update') }}</AButton>
      </ASpace>
    </template>
  </AModal>
</template>

<style scoped>

</style>
