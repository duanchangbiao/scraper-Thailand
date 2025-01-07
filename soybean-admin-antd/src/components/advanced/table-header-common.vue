<script setup lang="ts">
import {$t} from '@/locales';

defineOptions({
  name: 'TableHeaderCommon'
});

interface Props {
  disabledUpdate?: boolean;
  loading?: boolean;
}

defineProps<Props>();

interface Emits {
  (e: 'refresh'): void;

  (e: 'batchUpdate'): void;
}

const emit = defineEmits<Emits>();

const columns = defineModel<AntDesign.TableColumnCheck[]>('columns', {
  default: () => []
});

function refresh() {
  emit('refresh');
}

function batchUpdate() {
  console.log()
  emit('batchUpdate');
}
</script>

<template>
  <div class="flex flex-wrap justify-end gap-x-12px gap-y-8px lt-sm:(w-200px py-12px)">
    <slot name="prefix"></slot>
    <AButton size="small" @click="refresh">
      <template #icon>
        <icon-mdi-refresh class="align-sub text-icon" :class="{ 'animate-spin': loading }"/>
      </template>
      <span class="ml-8px">{{ $t('common.refresh') }}</span>
    </AButton>
    <AButton size="small" danger :disabled="disabledUpdate">
      <template #icon>
<!--        <icon-mdi-refresh class="align-sub text-icon"/>-->
        <icon-ant-design-plus-square-outlined class="align-sub text-icon"/>
      </template>
      <span class="ml-8px">{{ $t('common.batchUpdate') }}</span>
    </AButton>
    <TableColumnSetting v-model:columns="columns"/>
    <slot name="suffix"></slot>

  </div>
</template>

<style scoped></style>

