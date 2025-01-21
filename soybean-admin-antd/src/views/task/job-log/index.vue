<script setup lang="tsx">

import {$t} from "@/locales";
import {useTable} from "@/hooks/common/table";
import {fetchJobLogList} from "@/service/api/company-info";

const {
  columns,
  loading,
  mobilePagination,
  data,
  getData,
  columnChecks,
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
      title: $t('page.JobLog.jobName'),
      align: 'center',
      minWidth: 60
    },
    {
      key: 'jobGroup',
      dataIndex: 'jobGroup',
      title: $t('page.JobLog.jobGroup'),
      align: 'center',
      width: 100
    },
    {
      key: 'invokeTarget',
      dataIndex: 'invokeTarget',
      title: $t('page.JobLog.invokeTarget'),
      align: 'center',
      minWidth: 100
    },
    {
      key: 'jobMessage',
      dataIndex: 'jobMessage',
      title: $t('page.JobLog.jobMessage'),
      align: 'center',
      minWidth: 200
    },
    {
      key: 'exceptionInfo',
      dataIndex: 'exceptionInfo',
      title: $t('page.JobLog.exceptionInfo'),
      align: 'center',
      minWidth: 200
    },
    // {
    //   key: 'jobStatus',
    //   title: $t('page.JobInfo.status'),
    //   align: 'center',
    //   width: 80,
    //   customRender: ({record}) => {
    //     if (record.jobStatus === null) {
    //       return null;
    //     }
    //     const tagMap: Record<Api.Common.EnableStatus, string> = {
    //       1: 'success',
    //       2: 'warning'
    //     };
    //     const label = $t(enableStatusRecord[record.jobStatus]);
    //
    //     return <Tag color={tagMap[record.jobStatus]}>{label}</Tag>;
    //   }
    // },
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
    /*{
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
    }*/
  ],
  apiFn: fetchJobLogList,
  apiParams: {
    current: 1,
    size: 10,
  }
});
</script>

<template>
  <div class="min-h-500px flex-col-stretch gap-16px overflow-hidden lt-sm:overflow-auto">
    <ACard
      :title="$t('page.JobLog.title')"
      :bordered="false"
      :body-style="{ flex: 1, overflow: 'hidden' }"
      class="flex-col-stretch sm:flex-1-hidden card-wrapper"
    >
      <template #extra>
        <TableHeaderCommon
          v-model:columns="columnChecks"
          :loading="loading"
          @refresh="getData"
        />
      </template>
      <ATable
        ref="tableWrapperRef"
        :columns="columns"
        :data-source="data"
        size="small"
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
