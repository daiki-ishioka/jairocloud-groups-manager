<script setup lang="ts">
import type { NavigationMenuItem } from '@nuxt/ui'

const rute = useRoute()
const localePath = useLocalePath()

const items = computed<NavigationMenuItem[]>(() => [
  {
    label: $t('Management'), type: 'label',
  },
  {
    label: $t('repositories'),
    icon: 'i-lucide-folder',
    to: localePath('/repos'),
    active: rute.path.startsWith(localePath('/repos')),
  },
  {
    label: $t('groups'),
    icon: 'i-lucide-users',
    to: localePath('/groups'),
    active: rute.path.startsWith(localePath('/groups')),
  },
  {
    label: $t('users'),
    icon: 'i-lucide-user',
    to: localePath('/users'),
    active: rute.path.startsWith(localePath('/users')),
  },
  {
    label: $t('Others'),
    type: 'label',
  },
  {
    label: $t('history'),
    icon: 'i-lucide-clock',
    to: localePath('/history'),
    active: rute.path.startsWith(localePath('/history')),
  },
  {
    label: $t('cache-groups-menu'),
    icon: 'i-lucide-database',
    to: localePath('/cache'),
    active: rute.path.startsWith(localePath('/cache')),
  },
])
</script>

<template>
  <UPageAside
    :class="[
      'hidden', 'lg:block', 'lg:w-50', 'shrink-0', 'border-e', 'border-default',
      'self-start', 'sticky', 'top-(--ui-header-height)]',
      'max-h-[calc(100vh-var(--ui-header-height))]', 'overflow-y-auto',
    ]"
  >
    <UNavigationMenu :items="items" orientation="vertical" />
  </UPageAside>
</template>
