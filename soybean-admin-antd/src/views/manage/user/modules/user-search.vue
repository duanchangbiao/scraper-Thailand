<script setup lang="ts">
import {computed} from 'vue';
import {$t} from '@/locales';
import {useAntdForm, useFormRules} from '@/hooks/common/form';
import {enableStatusOptions, userActiveOptions} from '@/constants/business';
import {translateOptions} from '@/utils/common';

defineOptions({
  name: 'UserSearch'
});

interface Emits {
  (e: 'reset'): void;

  (e: 'search'): void;
}

const emit = defineEmits<Emits>();

const {formRef, validate, resetFields} = useAntdForm();

const model = defineModel<Api.SystemManage.UserSearchParams>('model', {required: true});

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
  <ACard :title="$t('common.search')" :bordered="false" class="card-wrapper">
    <AForm
      ref="formRef"
      :model="model"
      :rules="rules"
      :label-col="{
        span: 5,
        md: 7
      }"
    >
      <ARow :gutter="[16, 16]" wrap>
        <ACol :span="24" :md="12" :lg="6">
          <AFormItem :label="$t('page.manage.user.username')" name="username" class="m-0">
            <AInput v-model:value="model.username" :placeholder="$t('page.manage.user.form.username')"/>
          </AFormItem>
        </ACol>
        <ACol :span="24" :md="12" :lg="6">
          <AFormItem :label="$t('page.manage.user.isActive')" name="isActive" class="m-0">
            <ASelect
              v-model:value="model.isActive"
              :placeholder="$t('page.manage.user.form.isActive')"
              :options="translateOptions(userActiveOptions)"
              clearable
            />
          </AFormItem>
        </ACol>
        <ACol :span="24" :md="12" :lg="6">
          <AFormItem :label="$t('page.manage.user.email')" name="email" class="m-0">
            <AInput v-model:value="model.email" :placeholder="$t('page.manage.user.form.email')"/>
          </AFormItem>
        </ACol>
        <ACol :span="24" :md="12" :lg="6">
          <AFormItem :label="$t('page.manage.user.status')" name="status" class="m-0">
            <ASelect
              v-model:value="model.status"
              :placeholder="$t('page.manage.user.form.status')"
              :options="translateOptions(enableStatusOptions)"
              clearable
            />
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

<style scoped lang="scss">
@media (min-width: 992px) {
  :where(.css-dev-only-do-not-override-19kkpcr).ant-col-lg-6 {
    display: block;
    flex: 0 0 25%;
    max-width: 20%;
  }
}
</style>
