<script setup lang="tsx">

import {$t} from "@/locales";
import {useTable, useTableOperate} from "@/hooks/common/table";
import {deleteJob, executorRun, fetchJobList} from "@/service/api/company-info";
import {Button, Tag} from "ant-design-vue";
import {enableStatusRecord} from "@/constants/business";
import JobSearch from "@/views/task/job/modules/job-search.vue";

const {
  columns,
  loading,
  mobilePagination,
  data,
  getData,
  getDataByPage,
  searchParams,
  columnChecks,
  scrollConfig
} = useTable({
  columns: () => [
    {
      key: 'index',
      title: $t('common.index'),
      dataIndex: 'index',
      align: 'center',
      width: 64
    },
    {
      key: 'jobName',
      dataIndex: 'jobName',
      title: $t('page.JobInfo.jobName'),
      align: 'center',
      minWidth: 60
    },
    {
      key: 'jobGroup',
      dataIndex: 'jobGroup',
      title: $t('page.JobInfo.jobGroup'),
      align: 'center',
      width: 100
    },
    {
      key: 'invokeTarget',
      dataIndex: 'invokeTarget',
      title: $t('page.JobInfo.invokeTarget'),
      align: 'center',
      minWidth: 100
    },
    {
      key: 'cronExpression',
      dataIndex: 'cronExpression',
      title: $t('page.JobInfo.cronExpression'),
      align: 'center',
      minWidth: 200
    },
    {
      key: 'jobStatus',
      title: $t('page.JobInfo.status'),
      align: 'center',
      width: 80,
      customRender: ({record}) => {
        if (record.jobStatus === null) {
          return null;
        }
        const tagMap: Record<Api.Common.EnableStatus, string> = {
          1: 'success',
          2: 'warning'
        };
        const label = $t(enableStatusRecord[record.jobStatus]);

        return <Tag color={tagMap[record.jobStatus]}>{label}</Tag>;
      }
    },
    {
      key: 'createTime',
      dataIndex: 'createTime',
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
      width: 160,
      customRender: ({record}) => (
        <div class="flex-center gap-8px">
          <Button type="primary" ghost size="small" onClick={() => updateJob(record.jobId)}>
            {$t('common.edit')}
          </Button>
          <Button type="primary" ghost size="small" onClick={() => excutorRun(record.jobId)}>
            {$t('common.execute')}
          </Button>
          <Button danger size="small" onClick={() => handleDelete(record.jobId)}>
            {$t('common.delete')}
          </Button>
        </div>
      )
    }
  ],
  apiFn: fetchJobList,
  apiParams: {
    current: 1,
    size: 10,
    jobName: undefined,
    JobGroup: undefined,
    status: undefined
  }
});

async function handleDelete(id: number) {
  const {error, response} = await deleteJob({jobId: id});
  if (!error) {
    if (response.data.success) {
      getDataByPage();
    }
  }

}

async function excutorRun(id: number) {
  const {error, response} = await executorRun({jobId: id});
  if (!error) {
    if (response.data.success) {
      getDataByPage();
    }
  }
  window.$message?.success("任务执行中.....");
}

const {checkedRowKeys, rowSelection} = useTableOperate(data, getData);
</script>

<template>
  <div class="min-h-500px flex-col-stretch gap-16px overflow-hidden lt-sm:overflow-auto">
    <JobSearch v-model:model="searchParams" @reset="getData" @search="getDataByPage"/>
    <ACard
      :title="$t('page.JobInfo.title')"
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

      <!--      <CompanyOperateModal-->
      <!--        v-model:visible="visible"-->
      <!--        :operate-type="operateType"-->
      <!--        :row-data="editingData"-->
      <!--        :all-pages="allPages"-->
      <!--        @submitted="getDataByPage"-->
      <!--      />-->
    </ACard>
  </div>
</template>

<style scoped>

</style>
