<script setup lang="ts">
import { upperFirst } from 'scule'

import type { TableColumn } from '@nuxt/ui'

import { UButton, UIcon, ULink } from '#components'

const localePath = useLocalePath()
const { repositories } = useDataStore()
const data = ref<Repository[]>(repositories)

const columnNameMap = {
  displayName: $t('repository.name-column'),
  url: $t('repository.url-column'),
  entityIds: $t('sp-connecter-column'),
} as const

type RepositoryTableColumn = TableColumn<Repository>
const columns = computed<RepositoryTableColumn[]>(() => [
  {
    accessorKey: 'id',
    header: ({ column }) => sortableHeader(column, '#'),
  },
  {
    accessorKey: 'displayName',
    header: ({ column }) => sortableHeader(column, columnNameMap.displayName),
    cell: ({ row }) => {
      const name: string = row.original.displayName
      return h(ULink, {
        to: localePath(`/repos/${row.original.id}`),
        class: 'font-bold hover:underline inline-flex items-center',
      }, [
        h('span', name),
        h(UIcon, { name: 'i-lucide-chevron-right', class: 'size-5 shrink-0' }),
      ])
    },
    enableHiding: false,
  },
  {
    accessorKey: 'url',
    header: ({ column }) => sortableHeader(column, columnNameMap.url),
    cell: ({ row }) => {
      const url = row.original.url
      return h(ULink, {
        to: url,
        target: '_blank',
        class: 'hover:underline inline-flex items-center gap-1',
      }, [
        h('span', url),
        h(UIcon, { name: 'i-lucide-external-link', class: 'size-4 shrink-0' }),
      ])
    },
    meta: {},
  },
  {
    accessorKey: 'entityIds',
    header: ({ column }) => sortableHeader(column, columnNameMap.entityIds),
  },
])

const table = useTemplateRef('table')

const columnVisibility = ref({ id: false })

type Column = Parameters<
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  Extract<RepositoryTableColumn['header'], (...arguments_: any) => any>
>[0]['column']

function sortableHeader(column: Column, label: string) {
  const sortDirection = column.getIsSorted()
  const iconSet = {
    asc: 'i-lucide-arrow-up-narrow-wide',
    desc: 'i-lucide-arrow-down-wide-narrow',
    none: 'i-lucide-arrow-up-down',
  } as const

  return h(UButton, {
    color: sortDirection ? 'primary' : 'neutral',
    variant: 'ghost',
    size: 'xs',
    label,
    icon: sortDirection ? iconSet[sortDirection] : iconSet.none,
    class: 'font-medium cursor-pointer',
    onClick() {
      if (sortDirection === 'asc') column.toggleSorting(true) // to desc
      else if (sortDirection === 'desc') column.clearSorting() // to default
      else column.toggleSorting(false) // to asc
    },
  })
}

const sorting = ref([{ id: 'id', desc: false }])
const isTableView = ref(true)

const page = ref(1)
const pageSize = ref(20)
const pageOptions = ref([20, 50, 100])

const globalFilter = ref('')
const filteredData = computed(() => {
  if (!globalFilter.value) return data.value
  const f = globalFilter.value.toLowerCase()
  return data.value.filter(
    item =>
      item.displayName.toLowerCase().includes(f)
      || item.url.toLowerCase().includes(f)
      || item.entityIds.toLowerCase().includes(f),
  )
})
const pagedData = computed(() => {
  const start = (page.value - 1) * pageSize.value
  return filteredData.value.slice(start, start + pageSize.value)
})

const displayInfo = computed(() => {
  const total = filteredData.value.length

  if (total === 0) {
    return '0件を表示（全0件）'
  }

  const start = (page.value - 1) * pageSize.value + 1
  const end = Math.min(page.value * pageSize.value, total)

  return $t('table.display-info-text', { start, end, total })
})

const isCreatable = true
</script>

<template>
  <div class="flex justify-center p-6">
    <UCard class="w-full max-w-6xl">
      <h2 class="text-2xl font-semibold">
        {{ $t('repository.list-title') }}
      </h2>

      <div class="flex justify-between items-center mt-4">
        <UButton
          v-if="isCreatable"
          :label="$t('repository.new-button')"
          color="primary"
          variant="solid"
          :to="'/service/new'"
          icon="i-lucide-plus"
          class="mb-4"
        />

        <UButton
          class="mb-4 ml-auto"
          color="neutral"
          variant="soft"
          :label="isTableView ? $t('table.switch-to-card-view') : $t('table.switch-to-table-view')"
          :icon="isTableView ? 'i-lucide-layout-grid' : 'i-lucide-list'"
          @click="isTableView = !isTableView"
        />
      </div>

      <div class="flex justify-between mb-4">
        <UInput
          v-model="globalFilter"
          class="max-w-sm"
          :placeholder="$t('search-placeholder')"
          icon="i-lucide-search"
        />

        <div class="flex justify-end items-center space-x-2 mb-2">
          <UDropdownMenu
            v-if="isTableView"
            :items="
              table?.tableApi
                ?.getAllColumns()
                .filter((column) => column.getCanHide())
                .map((column) => ({
                  label: upperFirst(column.id),
                  type: 'checkbox' as const,
                  checked: column.getIsVisible(),
                  onUpdateChecked(checked: boolean) {
                    table?.tableApi?.getColumn(column.id)?.toggleVisibility(!!checked)
                  },
                  onSelect(e: Event) {
                    e.preventDefault()
                  },
                }))
            "
            :content="{ align: 'end' }"
          >
            <UButton
              :label="$t('table.display-item-label')"
              color="neutral"
              variant="outline"
              trailing-icon="i-lucide-chevron-down"
            />
          </UDropdownMenu>

          <div class="flex items-center space-x-2">
            <span class="text-sm text-gray-600">{{ $t('table.display-count-label') }}</span>
            <USelect
              v-model="pageSize"
              :items="pageOptions"
              class="w-24"
            />
          </div>
        </div>
      </div>

      <div v-if="isTableView">
        <UTable
          ref="table"
          v-model:column-visibility="columnVisibility"
          v-model:sorting="sorting"
          v-model:global-filter="globalFilter"
          :data="pagedData"
          :columns="columns"
        />
      </div>

      <div v-else class="grid grid-cols-3 gap-4">
        <UCard v-for="item in filteredData" :key="item.entityIds" class="p-4">
          <h3 class="font-bold text-lg mb-2">
            <ULink
              :to="`repos/${item.id}`"
              class="font-bold hover:underline inline-flex items-center"
            >
              {{ item.displayName }}
              <span><UIcon name="i-lucide-chevron-right" class="size-5 shrink-0" /></span>
            </ULink>
          </h3>
          <p class="text-sm text-gray-600 mb-1">
            {{ $t('repository.url-label') }}
            <a :href="item.url" target="_blank" class="text-blue-600 hover:underline">
              {{ item.url }}
            </a>
          </p>
          <p class="text-sm text-gray-600 mb-1">
            {{ $t('sp-connector-label') }} {{ item.entityIds }}
          </p>
        </UCard>
      </div>

      <div class="flex items-center mt-4">
        <div class="flex-1 text-gray-500 text-sm">
          {{ displayInfo }}
        </div>
        <div class="flex-2 flex justify-center">
          <UPagination
            v-model:page="page"
            :items-per-page="pageSize"
            :total="filteredData.length"
          />
        </div>
        <div class="flex-1" />
      </div>
    </UCard>
  </div>
</template>
