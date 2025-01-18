<script setup lang="tsx">
import {$t} from '@/locales';
import {useAntdForm} from '@/hooks/common/form';
import {translateOptions} from "@/utils/common";
import {enableATFStatusOptions, enableStatusOptions} from "@/constants/business";

defineOptions({
  name: 'JobSearch'
});

interface Emits {
  (e: 'reset'): void;

  (e: 'search'): void;
}

const emit = defineEmits<Emits>();

const {formRef, validate, resetFields} = useAntdForm();

const model = defineModel<Api.Job.JobSearchParams>('model', {required: true});


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
        <ACol :span="24" :md="12" :lg="6">
          <AFormItem :label="$t('page.JobInfo.jobName')" name="jobName" class="m-0">
            <AInput v-model:value="model.jobName" :placeholder="$t('page.JobInfo.form.jobName')"/>
          </AFormItem>
        </ACol>
        <ACol :span="24" :md="12" :lg="6">
          <AFormItem :label="$t('page.JobInfo.jobGroup')" name="jobGroup" class="m-0">
            <AInput v-model:value="model.jobGroup" :placeholder="$t('page.JobInfo.form.jobGroup')"/>
          </AFormItem>
        </ACol>
        <ACol :span="24" :md="12" :lg="6">
          <AFormItem :label="$t('page.JobInfo.status')" name="applyType" class="m-0">
            <ASelect
              v-model:value="model.status"
              :placeholder="$t('page.JobInfo.form.status')"
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

<style scoped></style>
