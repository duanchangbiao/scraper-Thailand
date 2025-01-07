<script setup lang="ts">
import {computed, shallowRef} from 'vue';
import type {DataNode} from 'ant-design-vue/es/tree';
import {$t} from '@/locales';
import {fetchGetAllButtons} from "@/service/api";

defineOptions({
  name: 'ButtonAuthModal'
});

interface Props {
  /** the roleId */
  roleId: number;
}

const props = defineProps<Props>();

const visible = defineModel<boolean>('visible', {
  default: false
});

function closeModal() {
  visible.value = false;
}

const title = computed(() => $t('common.edit') + $t('page.manage.role.buttonAuth'));

const tree = shallowRef<DataNode[]>([]);

async function getAllButtons() {
  // request
  const {error, data} = await fetchGetAllButtons()
  if (!error) {
    console.log(data)
    tree.value = [
      {key: 1, title: 'button1', code: 'code1'}
    ];
  }

}

const checks = shallowRef<number[]>([]);

async function getChecks() {
  console.log(props.roleId);
  // request
  checks.value = [1, 2, 3, 4, 5];
}

function handleSubmit() {
  console.log(checks.value, props.roleId);
  // request

  window.$message?.success?.($t('common.modifySuccess'));

  closeModal();
}

function init() {
  getAllButtons();
  getChecks();
}

// init
init();
</script>

<template>
  <AModal v-model:open="visible" :title="title" class="w-480px">
    <ATree v-model:checked-keys="checks" :tree-data="tree" checkable :height="280" class="h-280px"/>
    <template #footer>
      <AButton size="small" class="mt-16px" @click="closeModal">
        {{ $t('common.cancel') }}
      </AButton>
      <AButton type="primary" size="small" class="mt-16px" @click="handleSubmit">
        {{ $t('common.confirm') }}
      </AButton>
    </template>
  </AModal>
</template>

<style scoped></style>
