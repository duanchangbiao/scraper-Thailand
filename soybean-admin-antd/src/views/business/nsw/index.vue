<script setup lang="tsx">
import {Button, Tag} from 'ant-design-vue';
import {$t} from "@/locales";
import {useTable, useTableOperate, useTableScroll} from "@/hooks/common/table";
import {fetchGetNSWList, updateMorInfo} from "@/service/api/company-info";
import NswSearch from "@/views/business/nsw/modules/nsw-search.vue";
import {enableUpdateStatusRecord} from "@/constants/business";
import {type Ref, ref} from "vue";
import {useBoolean} from "~/packages/hooks";
import {OperateType} from "@/views/manage/menu/modules/menu-operate-modal.vue";
import NswUpdateOperateModal from "@/views/business/nsw/modules/nsw-operate-modal.vue";

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
      title: $t('page.business_nsw.applyNumber'),
      dataIndex: 'applyNumber',
      align: 'center',
      width: 100
    },
    {
      key: 'username',
      title: $t('page.business_nsw.username'),
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
      title: $t('page.business_nsw.applyDate'),
      dataIndex: 'applyDate',
      align: 'center',
      width: 150
    },
    {
      key: 'invoice',
      title: $t('page.business_nsw.invoice'),
      dataIndex: 'invoice',
      align: 'center',
      width: 150
    },
    // {
    //   key: 'invoiceDate',
    //   title: $t('page.business_nsw.invoiceDate'),
    //   dataIndex: 'invoiceDate',
    //   align: 'center',
    //   width: 150
    // },
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
      title: $t('page.business_nsw.applyStatus'),
      dataIndex: 'applyStatus',
      align: 'center',
      width: 200
    },
    // {
    //   key: 'passDate',
    //   title: $t('page.business_nsw.passDate'),
    //   dataIndex: 'passDate',
    //   align: 'center',
    //   width: 200
    // },
    // {
    //   key: 'sort',
    //   title: $t('page.business_aft.sort'),
    //   dataIndex: 'sort',
    //   align: 'center',
    //   width: 50
    // },
    {
      key: 'remark',
      title: $t('page.business_aft.remark'),
      dataIndex: 'remark',
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
          <Button size="small" type="primary" ghost onClick={() => handleEdit(record)}>
            {$t('common.edit')}
          </Button>
          <Button size="small" type="primary" ghost onClick={() => handleSubmit(record.username)}>
            {$t('common.update')}
          </Button>
          <Button danger size="small">
            {$t('common.delete')}
          </Button>
        </div>
      )
    }
  ],
  apiFn: fetchGetNSWList,
  apiParams: {
    current: 1,
    size: 10,
    applyStatus: undefined,
    username: undefined,
    applyNumber: undefined
  }
});
const {checkedRowKeys, rowSelection} = useTableOperate(data, getData);

async function handleSubmit(username: string) {
  const applyType = "NSW"
  const {error, response} = await updateMorInfo({username, applyType});
  if (!error) {
    if (response.data.success) {
      window.$message?.success($t(response.data.msg))
    }
  }
}

function handleEdit(item: Api.Business.BusinessAftInfo) {
  operateType.value = 'edit';
  editingData.value = {...item};
  openModal();
}
const operateType = ref<OperateType>('edit');
const allPages = ref<string[]>([]);
const editingData: Ref<Api.Business.BusinessAftInfo | null> = ref(null);
const {bool: visible, setTrue: openModal} = useBoolean();
</script>

<template>
  <div class="min-h-500px flex-col-stretch gap-16px overflow-hidden lt-sm:overflow-auto">
    <NswSearch v-model:model="searchParams" @reset="getData" @search="getDataByPage"/>
    <ACard
      :title="$t('page.business_nsw.title')"
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
    <NswUpdateOperateModal
      v-model:visible="visible"
      :operate-type="operateType"
      :row-data="editingData"
      :all-pages="allPages"
      @submitted="getDataByPage"
    />
  </div>
</template>

<style scoped>

</style>
