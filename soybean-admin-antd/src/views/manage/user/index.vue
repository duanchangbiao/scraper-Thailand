<script setup lang="tsx">
import {Button, Popconfirm, Tag} from 'ant-design-vue';
import {deleteUserInfo, fetchGetUserList} from '@/service/api';
import {useTable, useTableOperate, useTableScroll} from '@/hooks/common/table';
import {$t} from '@/locales';
import {enableActiveRecord, enableStatusRecord, userGenderRecord, userTypeRecord} from '@/constants/business';
import UserOperateDrawer from './modules/user-operate-drawer.vue';
import UserSearch from './modules/user-search.vue';

const {tableWrapperRef, scrollConfig} = useTableScroll();

const {
  columns,
  columnChecks,
  data,
  getData,
  getDataByPage,
  loading,
  mobilePagination,
  searchParams,
  resetSearchParams
} = useTable({
  apiFn: fetchGetUserList,
  apiParams: {
    current: 1,
    size: 10,
    status: undefined,
    username: undefined,
    nickname: undefined,
    email: undefined,
    isActive: undefined,
  },
  columns: () => [
    {
      key: 'index',
      title: $t('common.index'),
      dataIndex: 'index',
      align: 'center',
      width: 64
    },
    {
      key: 'username',
      dataIndex: 'username',
      title: $t('page.manage.user.username'),
      align: 'center',
      minWidth: 100
    },
    // {
    //   key: 'userRole',
    //   dataIndex: 'userRole.roleName',
    //   title: $t('page.manage.user.userRole.roleName'),
    //   align: 'center',
    //   minWidth: 100
    // },
    {
      key: 'sex',
      title: $t('page.manage.user.sex'),
      align: 'center',
      dataIndex: 'sex',
      width: 100,
      customRender: ({record}) => {
        if (record.sex === null) {
          return null;
        }
        const tagMap: Record<Api.SystemManage.UserGender, string> = {
          1: 'processing',
          2: 'error'
        };

        const label = $t(userGenderRecord[record.sex]);

        return <Tag color={tagMap[record.sex]}>{label}</Tag>;
      }
    },
    {
      key: 'userType',
      dataIndex: 'userType',
      title: $t('page.manage.user.userType'),
      align: 'center',
      width: 100,
      customRender: ({record}) => {
        if (record.userType === null) {
          return null;
        }

        const tagMap: Record<Api.Common.UserType, string> = {
          '1': 'success',
          '2': 'pink'
        };

        const label = $t(userTypeRecord[record.userType]);

        return <Tag color={tagMap[record.userType]}>{label}</Tag>;
      }
    },
    {
      key: 'nickname',
      dataIndex: 'nickname',
      title: $t('page.manage.user.nickname'),
      align: 'center',
      minWidth: 100
    },
    {
      key: 'isActive',
      dataIndex: 'isActive',
      title: $t('page.manage.user.isActive'),
      align: 'center',
      minWidth: 100,
      customRender: ({record}) => {
        if (record.isActive === null) {
          return null;
        }

        const tagMap: Record<Api.Common.EnableActive, string> = {
          1: 'success',
          0: 'warning'
        };

        const label = $t(enableActiveRecord[record.isActive]);

        return <Tag color={tagMap[record.isActive]}>{label}</Tag>;
      }
    },
    {
      key: 'phone',
      dataIndex: 'phone',
      title: $t('page.manage.user.phone'),
      align: 'center',
      width: 120
    },
    {
      key: 'email',
      dataIndex: 'email',
      title: $t('page.manage.user.email'),
      align: 'center',
      minWidth: 200
    },
    {
      key: 'status',
      dataIndex: 'status',
      title: $t('page.manage.user.status'),
      align: 'center',
      width: 100,
      customRender: ({record}) => {
        if (record.status === null) {
          return null;
        }

        const tagMap: Record<Api.Common.EnableStatus, string> = {
          1: 'success',
          2: 'warning'
        };

        const label = $t(enableStatusRecord[record.status]);

        return <Tag color={tagMap[record.status]}>{label}</Tag>;
      }
    },
    {
      key: 'createTime',
      dataIndex: 'createTime',
      title: $t('page.manage.user.createTime'),
      align: 'center',
      minWidth: 200
    },
    {
      key: 'updateTime',
      dataIndex: 'updateTime',
      title: $t('page.manage.user.updateTime'),
      align: 'center',
      minWidth: 200
    },
    {
      key: 'operate',
      title: $t('common.operate'),
      align: 'center',
      width: 130,
      customRender: ({record}) => (
        <div class="flex-center gap-8px">
          <Button type="primary" ghost size="small" onClick={() => edit(record.id)}>
            {$t('common.edit')}
          </Button>
          <Popconfirm title={$t('common.confirmDelete')} onConfirm={() => handleDelete(record.id)}>
            <Button danger size="small">
              {$t('common.delete')}
            </Button>
          </Popconfirm>
        </div>
      )
    }
  ]
});

const {
  drawerVisible,
  operateType,
  editingData,
  handleAdd,
  handleEdit,
  checkedRowKeys,
  rowSelection,
  // closeDrawer
} = useTableOperate(data, getData);

async function handleDelete(id: number) {
  const {error, response} = await deleteUserInfo({id})
  if (!error) {
    if (response.data.success) {
      window.$message?.success($t(response.data.msg));
      await getData()
    } else {
      window.$message?.error($t(response.data.msg));
      await getData()
    }
  }
}

function edit(id: number) {
  handleEdit(id);
}
</script>

<template>
  <div class="min-h-500px flex-col-stretch gap-16px overflow-hidden lt-sm:overflow-auto">
    <UserSearch v-model:model="searchParams" @reset="resetSearchParams" @search="getDataByPage"/>
    <ACard
      :title="$t('page.manage.user.title')"
      :bordered="false"
      :body-style="{ flex: 1, overflow: 'hidden' }"
      class="flex-col-stretch sm:flex-1-hidden card-wrapper"
    >
      <template #extra>
        <TableHeaderOperation
          v-model:columns="columnChecks"
          :disabled-delete="checkedRowKeys.length === 0"
          :loading="loading"
          @add="handleAdd"
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

      <UserOperateDrawer
        v-model:visible="drawerVisible"
        :operate-type="operateType"
        :row-data="editingData"
        @submitted="getDataByPage"
      />
    </ACard>
  </div>
</template>

<style scoped></style>
