<script setup lang="tsx">
import {Button, Tag} from 'ant-design-vue';
import {$t} from "@/locales";
import {useTable, useTableOperate, useTableScroll} from "@/hooks/common/table";
import {fetchAftList, updateMorInfo} from "@/service/api/company-info";
import AftSearch from "@/views/business/aft/modules/aft-search.vue";
import {enableUpdateStatusRecord} from "@/constants/business";

const {tableWrapperRef, scrollConfig} = useTableScroll();
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
      title: $t('page.business_aft.applyNumber'),
      dataIndex: 'applyNumber',
      align: 'center',
      width: 100
    },
    {
      key: 'username',
      title: $t('page.business_aft.username'),
      dataIndex: 'username',
      align: 'center',
      width: 150
    },
    {
      key: 'tisCode',
      title: $t('page.business_aft.tisCode'),
      dataIndex: 'tisCode',
      align: 'center',
      width: 64
    },
    // {
    //   key: 'standardName',
    //   title: $t('page.business_aft.standardName'),
    //   dataIndex: 'standardName',
    //   align: 'center',
    //   width: 200
    // },
    {
      key: 'applyType',
      title: $t('page.business_aft.applyType'),
      dataIndex: 'applyType',
      align: 'center',
      width: 64
    },
    {
      key: 'applyDate',
      title: $t('page.business_aft.applyDate'),
      dataIndex: 'applyDate',
      align: 'center',
      width: 100
    },
    {
      key: 'updateType',
      title: $t('page.business_mor.updateType'),
      dataIndex: 'updateType',
      align: 'center',
      width: 150,
      customRender: ({record}) => {
        if (record.updateType === null) {
          return null;
        }

        const tagMap: Record<Api.Common.EnableStatus, string> = {
          2: 'success',
          1: 'warning'
        };

        const label = $t(enableUpdateStatusRecord[record.updateType]);

        return <Tag color={tagMap[record.updateType]}>{label}</Tag>;
      }
    },
    {
      key: 'applyStatus',
      title: $t('page.business_aft.applyStatus'),
      dataIndex: 'applyStatus',
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
          <Button danger size="small" onClick={() => handleSubmit(record.username, record.applyType)}>
            {$t('common.update')}
          </Button>
        </div>
      )
    }
  ],
  apiFn: fetchAftList,
  apiParams: {
    current: 1,
    size: 10,
    applyStatus: undefined,
    username: undefined,
    applyNumber: undefined
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
    <AftSearch v-model:model="searchParams" @reset="getData" @search="getDataByPage"/>
    <ACard
      :title="$t('page.business_aft.title')"
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

<style scoped>

</style>
