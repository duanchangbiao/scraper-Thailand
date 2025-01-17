<script setup lang="ts">
import { computed } from 'vue';
import { $t } from '@/locales';

defineOptions({
  name: 'ProjectNews'
});

interface NewsItem {
  id: number;
  content: string;
  time: string;
}

const newses = computed<NewsItem[]>(() => [
]);
</script>

<template>
  <ACard :title="$t('page.home.JobNews.title')" :bordered="false" size="small" class="card-wrapper">
    <template #extra>
      <a class="text-primary" href="javascript:;">{{ $t('page.home.JobNews.moreNews') }}</a>
    </template>
    <AList :data-source="newses">
      <template #renderItem="{ item }">
        <AListItem>
          <AListItemMeta :title="item.content" :description="item.time">
            <template #avatar>
              <SoybeanAvatar class="size-48px!" />
            </template>
          </AListItemMeta>
        </AListItem>
      </template>
    </AList>
  </ACard>
</template>

<style scoped></style>
