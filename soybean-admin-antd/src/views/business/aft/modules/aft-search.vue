<script setup lang="ts">
import {$t} from '@/locales';
import {useAntdForm} from '@/hooks/common/form';
import {translateOptions} from "@/utils/common";
import {enableATFStatusOptions, enableMorStatusOptions} from "@/constants/business";

defineOptions({
  name: 'AftSearch'
});

interface Emits {
  (e: 'reset'): void;

  (e: 'search'): void;
}

const emit = defineEmits<Emits>();

const {formRef, validate, resetFields} = useAntdForm();

const model = defineModel<Api.Business.AFTSearchParams>('model', {required: true});


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
    <AForm ref="formRef" :model="model" :label-col="{ span: 5, md: 7 }">
      <ARow :gutter="[16, 16]" wrap>
        <ACol :span="24" :md="8" :lg="4">
          <AFormItem :label="$t('page.business_mor.applyNumber')" name="applyNumber" class="m-0">
            <AInput v-model:value="model.applyNumber" :placeholder="$t('page.business_mor.form.applyNumber')"/>
          </AFormItem>
        </ACol>
        <ACol :span="24" :md="8" :lg="4">
          <AFormItem :label="$t('page.business_mor.username')" name="username" class="m-0">
            <AInput v-model:value="model.username" :placeholder="$t('page.business_mor.form.username')"/>
          </AFormItem>
        </ACol>
        <ACol :span="24" :md="8" :lg="4">
          <AFormItem :label="$t('page.business_mor.applyStatus')" name="applyStatus" class="m-0">
            <AInput v-model:value="model.applyStatus" :placeholder="$t('page.business_mor.form.applyStatus')"/>
          </AFormItem>
        </ACol>
        <ACol :span="24" :md="8" :lg="5">
          <AFormItem :label="$t('page.business_mor.applyType')" name="applyType" class="m-0">
            <ASelect
              v-model:value="model.applyType"
              :placeholder="$t('page.business_mor.form.applyType')"
              :options="translateOptions(enableATFStatusOptions)"
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

<style scoped></style>

