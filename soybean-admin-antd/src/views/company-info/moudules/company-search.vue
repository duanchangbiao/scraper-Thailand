<script setup lang="ts">
import {computed} from 'vue';
import {$t} from '@/locales';
import {useAntdForm, useFormRules} from '@/hooks/common/form';

defineOptions({
  name: 'CompanySearch'
});

interface Emits {
  (e: 'reset'): void;

  (e: 'search'): void;
}

const emit = defineEmits<Emits>();

const {formRef, validate, resetFields} = useAntdForm();

const model = defineModel<Api.Company.CompanySearchParams>('model', {required: true});

type RuleKey = Extract<keyof Api.SystemManage.UserSearchParams, 'userEmail' | 'userPhone'>;

const rules = computed<Record<RuleKey, App.Global.FormRule>>(() => {
  const {patternRules} = useFormRules(); // inside computed to make locale reactive

  return {
    userEmail: patternRules.email,
    userPhone: patternRules.phone
  };
});

async function reset() {
  await resetFields();
  emit('reset');
}

async function search() {
  await validate();
  emit('search');
}
</script>

<template>
  <!--  <ACard :title="$t('common.search')" :bordered="false" class="card-wrapper">-->
  <ACard :title="$t('common.search')" :bordered="false" class="card-wrapper">
    <AForm ref="formRef" :model="model" :rules="rules" :label-col="{ span: 5, md: 7 }">
      <ARow :gutter="[16, 16]" wrap>
        <ACol :span="24" :md="12" :lg="6">
          <AFormItem :label="$t('page.company_info.licenseId')" name="licenseId" class="m-0">
            <AInput v-model:value="model.licenseId" :placeholder="$t('page.company_info.form.licenseId')"/>
          </AFormItem>
        </ACol>
        <ACol :span="24" :md="12" :lg="6">
          <AFormItem :label="$t('page.company_info.companyName')" name="companyName" class="m-0">
            <AInput v-model:value="model.companyName" :placeholder="$t('page.company_info.form.companyName')"/>
          </AFormItem>
        </ACol>
        <ACol :span="24" :md="12" :lg="6">
          <AFormItem :label="$t('page.company_info.taxIdentificationNumber')" name="taxIdentificationNumber"
                     class="m-0">
            <AInput v-model:value="model.taxIdentificationNumber" :placeholder="$t('page.company_info.form.taxIdentificationNumber')"/>
          </AFormItem>
        </ACol>
        <div class="flex-1">
          <AFormItem class="m-0">
            <div class="w-full flex-y-center justify-end gap-12px">
              <AButton @click="reset">
                <template #icon>
                  <icon-ic-round-refresh class="align-sub text-icon"/>
                </template>
                <span class="ml-8px">{{ $t('common.reset') }}</span>
              </AButton>
              <AButton type="primary" ghost @click="search">
                <template #icon>
                  <icon-ic-round-search class="align-sub text-icon"/>
                </template>
                <span class="ml-8px">{{ $t('common.search') }}</span>
              </AButton>
            </div>
          </AFormItem>
        </div>
      </ARow>
    </AForm>
  </ACard>
</template>

<style scoped></style>
