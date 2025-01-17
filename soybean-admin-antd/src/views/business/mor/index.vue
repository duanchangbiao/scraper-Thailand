<script setup lang="tsx">
import {Button} from 'ant-design-vue';
import {$t} from '@/locales';
import {useTable, useTableOperate, useTableScroll} from '@/hooks/common/table';
import {fetchGetMorList, updateMorInfo} from "@/service/api/company-info";
import MorSearch from "@/views/business/mor/modules/mor-search.vue";

const {tableWrapperRef, scrollConfig} = useTableScroll();
// const allPages = ref<string[]>([]);
// const {bool: visible, setTrue: openModal} = useBoolean();
// 获取列表信息
const {columns, loading, data, getData, mobilePagination, columnChecks, searchParams, getDataByPage} = useTable({
  columns: () => [
    {
      key: 'index',
      title: $t('common.index'),
      dataIndex: 'index',
      align: 'center',
      width: 64
    },
    {
      key: 'applyNumber',
      title: $t('page.business_mor.applyNumber'),
      dataIndex: 'applyNumber',
      align: 'center',
      width: 100
    },
    {
      key: 'username',
      title: $t('page.business_mor.username'),
      dataIndex: 'username',
      align: 'center',
      width: 150
    },
    // {
    //   key: 'tisCode',
    //   title: $t('page.business_mor.tisCode'),
    //   dataIndex: 'tisCode',
    //   align: 'center',
    //   width: 64
    // },
    // {
    //   key: 'standardName',
    //   title: $t('page.business_mor.standardName'),
    //   dataIndex: 'standardName',
    //   align: 'center',
    //   width: 200
    // },
    // {
    //   key: 'applyLicense',
    //   title: $t('page.business_mor.applyLicense'),
    //   dataIndex: 'applyLicense',
    //   align: 'center',
    //   width: 64
    // },
    {
      key: 'applyDate',
      title: $t('page.business_mor.applyDate'),
      dataIndex: 'applyDate',
      align: 'center',
      width: 100
    },
    // {
    //   key: 'applyTaxNumber',
    //   title: $t('page.business_mor.applyTaxNumber'),
    //   dataIndex: 'applyTaxNumber',
    //   align: 'center',
    //   width: 100
    // },
    {
      key: 'applyStatus',
      title: $t('page.business_mor.applyStatus'),
      dataIndex: 'applyStatus',
      align: 'center',
      width: 150
    },
    {
      key: 'applyType',
      title: $t('page.business_mor.applyType'),
      dataIndex: 'applyType',
      align: 'center',
      width: 64
    },
    {
      key: 'companyName',
      title: $t('page.business_mor.companyName'),
      dataIndex: 'companyName',
      align: 'center',
      width: 200
    },
    {
      key: 'ctime',
      title: $t('page.business_mor.ctime'),
      dataIndex: 'ctime',
      align: 'center',
      width: 150
    },
    {
      key: 'operate',
      title: $t('common.operate'),
      align: 'center',
      width: 130,
      customRender: ({record}) => (
        <div class="flex-center gap-8px">
          <Button type="primary" ghost size="small">
            {$t('common.details')}
          </Button>
          <Button danger size="small"  onClick={() => handleSubmit(record.username, record.applyType)}>
            {$t('common.update')}
          </Button>
        </div>
      )
    }
  ],
  apiFn: fetchGetMorList,
  apiParams: {
    current: 1,
    size: 10,
    applyStatus: undefined,
    username: undefined,
    applyType: undefined
  }
});
const {checkedRowKeys, rowSelection} = useTableOperate(data, getData);


async function handleSubmit(username: string, applyType: string) {

  const {error, response} = await updateMorInfo({username, applyType});
  if (!error) {
    if (response.data.success) {
      window.$message?.success($t(response.data.msg))
    }
  }
}
</script>

<template>
  <div class="min-h-500px flex-col-stretch gap-16px overflow-hidden lt-sm:overflow-auto">
    <MorSearch v-model:model="searchParams" @reset="getData" @search="getDataByPage"/>
    <ACard
      :title="$t('page.business_mor.title')"
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
    </ACard>
  </div>
</template>

<style scoped></style>

