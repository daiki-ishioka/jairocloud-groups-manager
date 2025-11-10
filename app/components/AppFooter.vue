<script setup lang="ts">
import type { FooterColumn } from '@nuxt/ui'

const localePath = useLocalePath()

const columns = computed<FooterColumn[]>(() => [
  {
    label: $t('Management'),
    children: [
      { label: $t('repositories'), to: localePath('/repos') },
      { label: $t('groups'), to: localePath('/groups') },
      { label: $t('users'), to: localePath('/users') },
    ],
  },
  {
    label: $t('Others'),
    children: [
      { label: $t('history'), to: localePath('/history') },
      { label: $t('cache-groups-menu'), to: localePath('/cache') },
    ],
  },
])
</script>

<template>
  <USeparator icon="i-simple-icons-nuxtdotjs" class="h-px" />

  <UFooter :ui="{ top: 'border-b border-default' }">
    <template #top>
      <UContainer>
        <UFooterColumns :columns="columns" />
      </UContainer>
    </template>

    <template #left>
      <p class="text-muted text-sm">
        &copy; {{ new Date().getFullYear() }} National Institute of Informatics
      </p>
    </template>

    <template #right>
      <UColorModeButton />
    </template>
  </UFooter>
</template>
