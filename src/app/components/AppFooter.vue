<!--
 Copyright (C) 2026 National Institute of Informatics.
-->

<script setup lang="ts">
import { author } from '@@/package.json'

import type { FooterColumn } from '@nuxt/ui'

const { management, other } = useMenu()

const columns = ref<FooterColumn[]>([
  {
    label: 'Management',
    children: management,
  },
  {
    label: 'Other',
    children: other,
  },
])
</script>

<template>
  <USeparator icon="i-lucide-ellipsis" class="h-px" />

  <UFooter :ui="{ top: 'border-b border-default' }">
    <template #top>
      <UContainer>
        <UPage>
          <template #left>
            <UPageAside />
          </template>

          <UPageBody class="pb-0 px-10">
            <UFooterColumns :columns="columns" :ui="{ root: 'xl:grid-cols-2' }" />
          </UPageBody>
        </UPage>
      </UContainer>
    </template>

    <template #left>
      <p class="text-muted text-sm">
        &copy; {{ new Date().getFullYear() }} {{ author.name }}
      </p>
    </template>

    <template #right>
      <ULink to="" class="text-sm hover:underline inline-flex items-center gap-1">
        Privacy Policy
        <UIcon name="i-lucide-external-link" class="size-3 shrink-0" /></ULink>
      |
      <ULink to="" class="text-sm hover:underline inline-flex items-center gap-1">
        Terms of Use
        <UIcon name="i-lucide-external-link" class="size-3 shrink-0" /></ULink>
    </template>
  </UFooter>
</template>
