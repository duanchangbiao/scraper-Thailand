<script setup lang="tsx">
import {Button, Tag} from 'ant-design-vue';
import {$t} from '@/locales';
import {useTable, useTableOperate, useTableScroll} from '@/hooks/common/table';
import {fetchGetMorList, updateMorInfo} from "@/service/api/company-info";
import MorSearch from "@/views/business/mor/modules/mor-search.vue";
import {enableUpdateStatusRecord} from "@/constants/business";
import {type Ref, ref} from "vue";
import {useBoolean} from "~/packages/hooks";
import MorUpdateOperateModal, {OperateType} from "@/views/business/mor/modules/mor-operate-modal.vue";

const {tableWrapperRef, scrollConfig} = useTableScroll();
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
    {
      key: 'nickname',
      title: $t('page.business_mor.nickname'),
      dataIndex: 'nickname',
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
      key: 'applyType',
      title: $t('page.business_mor.applyType'),
      dataIndex: 'applyType',
      align: 'center',
      width: 64
    },
    {
      key: 'applyStatus',
      title: $t('page.business_mor.applyStatus'),
      dataIndex: 'applyStatus',
      align: 'center',
      width: 150
    },
    {
      key: 'remark',
      title: $t('page.business_aft.remark'),
      dataIndex: 'remark',
      align: 'center',
      width: 200
    },
    // {
    //   key: 'companyName',
    //   title: $t('page.business_mor.companyName'),
    //   dataIndex: 'companyName',
    //   align: 'center',
    //   width: 200
    // },
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
      width: 150,
      customRender: ({record}) => (
        <div class="flex-center gap-8px">
          <Button size="small" type="primary" ghost onClick={() => handleEdit(record)}>
            {$t('common.edit')}
          </Button>
          <Button size="small" type="primary" ghost onClick={() => handleSubmit(record.username, record.applyType)}>
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
    <MorUpdateOperateModal
      v-model:visible="visible"
      :operate-type="operateType"
      :row-data="editingData"
      :all-pages="allPages"
      @submitted="getDataByPage"
    />
  </div>
</template>

<style scoped></style>

