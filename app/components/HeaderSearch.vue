<script setup lang="ts">
import type { CommandPaletteGroup, CommandPaletteItem } from '@nuxt/ui'

const router = useRouter()

const searchTerm = ref('')

const localePath = useLocalePath()
const dataStore = useDataStore()

const { data: result, status, execute } = await useFetch('/api/search', {
  method: 'GET',
  query: () => ({ q: searchTerm.value }),
  transform: (data: typeof dataStore) => {
    data = dataStore
    const items: Record<string, CommandPaletteItem[]> = {
      repos: data.repositories?.map(x => ({
        id: x.id,
        label: x.displayName,
        suffix: x.url,
        icon: 'i-lucide-folder',
        to: localePath(`/repo/${x.id}`),
      })) || [],
      users: data.users?.map(x => ({
        id: x.id,
        label: x.displayName,
        suffix: x.email,
        icon: 'i-lucide-user',
        to: localePath(`/user/${x.id}`),
      })) || [],
      groups: data.groups?.map(x => ({
        id: x.id,
        label: x.displayName,
        suffix: `${x.members?.length || 0} members`,
        icon: 'i-lucide-users',
        to: localePath(`/group/${x.id}`),
      })) || [],
    }
    return items
  },
  lazy: true,
})

const groups = computed<CommandPaletteGroup[]>(() => [
  {
    id: 'repos',
    label: searchTerm.value
      ? $t(`header.search-matching`, { query: searchTerm.value, group: $t('repositories') })
      : $t('repositories'),
    items: result.value?.repos || [],
    ignoreFilter: true,
  },
  {
    id: 'users',
    label: searchTerm.value
      ? $t(`header.search-matching`, { query: searchTerm.value, group: $t('users') })
      : $t('users'),
    items: result.value?.users || [],
    ignoreFilter: true,
  },
  {
    id: 'groups',
    label: searchTerm.value
      ? $t(`header.search-matching`, { query: searchTerm.value, group: $t('groups') })
      : $t('groups'),
    items: result.value?.groups || [],
    ignoreFilter: true,
  },
])

const onSubmit = async () => {
  if (!searchTerm.value) return
  await execute()
}

const onSelect = (item: CommandPaletteItem) => {
  if (item.to) router.push(item.to)
}

const isOpen = ref(false)
defineShortcuts({
  '/': () => isOpen.value = !isOpen.value,
})
</script>

<template>
  <UInput
    ref="input" color="neutral"
    icon="i-lucide-search" variant="outline"
    :placeholder="$t('search-placeholder')" class="w-50" @click="isOpen = true"
  >
    <template #trailing>
      <UKbd value="/" class="pointer-events-none" />
    </template>
  </UInput>

  <UModal v-model:open="isOpen">
    <template #content>
      <div class="relative">
        <UCommandPalette
          v-model:search-term="searchTerm"
          :loading="status === 'pending'" :groups="groups"
          :placeholder="$t('header.search-placeholder')"
          class="h-80" @submit="onSubmit" @select="onSelect"
        >
          <template #empty>
            <div v-if="searchTerm.length === 0">
              {{ $t('header.search-empty') }}
            </div>
            <div v-else>
              {{ $t('header.search-not-found', { query: searchTerm }) }}
            </div>
          </template>
          <template #close>
            <UKbd value="enter" />
          </template>
        </UCommandPalette>
      </div>
    </template>
  </UModal>
</template>
