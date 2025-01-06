<script setup lang="tsx">
import { Button, message } from 'ant-design-vue';
import { type Ref, ref } from 'vue';
import { $t } from '@/locales';
import { useTable, useTableOperate, useTableScroll } from '@/hooks/common/table';
import { fetchGetCompanyList, updateCompanyInfo } from '@/service/api/company-info';
import CompanySearch from '@/views/company-info/moudules/company-search.vue';
import type { OperateType } from '@/views/company-info/moudules/company-operate-modal.vue';
import CompanyOperateModal from '@/views/company-info/moudules/company-operate-modal.vue';
import { useBoolean } from '~/packages/hooks';

const { tableWrapperRef, scrollConfig } = useTableScroll();
const allPages = ref<string[]>([]);
const { bool: visible, setTrue: openModal } = useBoolean();
// 获取列表信息
const { columns, loading, mobilePagination, data, getData, getDataByPage, searchParams, columnChecks } = useTable({
  columns: () => [
    {
      key: 'index',
      title: $t('common.index'),
      dataIndex: 'index',
      align: 'center',
      width: 64
    },
    {
      key: 'licenseId',
      dataIndex: 'licenseId',
      title: $t('page.company_info.licenseId'),
      align: 'center',
      minWidth: 60
    },
    {
      key: 'issuanceTime',
      dataIndex: 'issuanceTime',
      title: $t('page.company_info.issuanceTime'),
      align: 'center',
      width: 100
    },
    // {
    //   key: 'licenseType',
    //   dataIndex: 'licenseType',
    //   title: $t('page.company_info.licenseType'),
    //   align: 'center',
    //   minWidth: 100
    // },
    // {
    //   key: 'licenseCompany',
    //   dataIndex: 'licenseCompany',
    //   title: $t('page.company_info.licenseCompany'),
    //   align: 'center',
    //   width: 150
    // },
    {
      key: 'companyName',
      dataIndex: 'companyName',
      title: $t('page.company_info.companyName'),
      align: 'center',
      minWidth: 200
    },
    // {
    //   key: 'companyAddress',
    //   dataIndex: 'companyAddress',
    //   title: $t('page.company_info.companyAddress'),
    //   align: 'center',
    //   width: 200
    // },
    // {
    //   key: 'factoryAddress',
    //   dataIndex: 'factoryAddress',
    //   title: $t('page.company_info.factoryAddress'),
    //   align: 'center',
    //   width: 200
    // },
    {
      key: 'factoryRegistrationNumber',
      dataIndex: 'factoryRegistrationNumber',
      title: $t('page.company_info.factoryRegistrationNumber'),
      align: 'center',
      width: 150
    },
    {
      key: 'taxIdentificationNumber',
      dataIndex: 'taxIdentificationNumber',
      title: $t('page.company_info.taxIdentificationNumber'),
      align: 'center',
      width: 120
    },
    {
      key: 'ctime',
      dataIndex: 'ctime',
      title: $t('page.company_info.ctime'),
      align: 'center',
      width: 150
    },
    {
      key: 'mtime',
      dataIndex: 'mtime',
      title: $t('page.company_info.mtime'),
      align: 'center',
      width: 150
    },
    {
      key: 'operate',
      title: $t('common.operate'),
      align: 'center',
      width: 130,
      customRender: ({ record }) => (
        <div class="flex-center gap-8px">
          <Button type="primary" ghost size="small" onClick={() => details(record)}>
            {$t('common.details')}
          </Button>
          <Button danger size="small" onClick={() => updateCompany(record.licenseId)}>
            {$t('common.update')}
          </Button>
        </div>
      )
    }
  ],
  apiFn: fetchGetCompanyList,
  apiParams: {
    current: 1,
    size: 10,
    licenseId: undefined,
    taxIdentificationNumber: undefined,
    companyName: undefined
  }
});
const { checkedRowKeys, rowSelection } = useTableOperate(data, getData);

const operateType = ref<OperateType>('details');
const editingData: Ref<Api.Company.CompanyInfo | null> = ref(null);

// 更新信息
async function updateCompany(licenseId: string) {
  const { error, data } = await updateCompanyInfo({ licenseId });
  if (!error) {
    // content must use function
    message.success('更新成功!');
    await getDataByPage()
  }
}

function details(item: Api.Company.CompanyInfo) {
  operateType.value = 'details';
  editingData.value = { ...item };
  openModal();
}
</script>

<template>
  <div class="min-h-500px flex-col-stretch gap-16px overflow-hidden lt-sm:overflow-auto">
    <CompanySearch v-model:model="searchParams" @reset="getData" @search="getDataByPage" />
    <ACard
      :title="$t('page.company_info.title')"
      :bordered="false"
      :body-style="{ flex: 1, overflow: 'hidden' }"
      class="flex-col-stretch sm:flex-1-hidden card-wrapper"
    >
      <template #extra>
        <TableHeaderCommon
          v-model:columns="columnChecks"
          :loading="loading"
          :disabled-update="checkedRowKeys.length === 0"
          @refresh="getData"
        />
      </template>
      <ATable
        ref="tableWrapperRef"
        :columns="columns"
        :data-source="data"
        size="small"
        :row-selection="rowSelection"
        :scroll="scrollConfig"
        :loading="loading"
        row-key="id"
        :pagination="mobilePagination"
        class="h-full"
      />

      <CompanyOperateModal
        v-model:visible="visible"
        :operate-type="operateType"
        :row-data="editingData"
        :all-pages="allPages"
        @submitted="getDataByPage"
      />
    </ACard>
  </div>
</template>

<style scoped></style>
