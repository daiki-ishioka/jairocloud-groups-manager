<script setup lang="ts">
import { upperFirst } from 'scule'

import type { DropdownMenuItem, TableColumn, TableRow } from '@nuxt/ui'

import { UBadge, UButton, UCheckbox, UIcon, ULink } from '#components'

const { repositories, groups } = useDataStore()
const localePath = useLocalePath()
const data = ref<Group[]>(groups)

const columnNameMap = {
  displayName: $t('group.name-column'),
  publicStatus: $t('group.public-status'),
  joinCondition: $t('group.join-condition'),
  memberVisibility: $t('group.member-visibility'),
} as const

type GroupTableColumn = TableColumn<Group>
const columns = computed<GroupTableColumn[]>(() => [
  {
    id: 'select',
    header: ({ table }) =>
      h(UCheckbox, {
        'modelValue': table.getIsSomePageRowsSelected()
          ? 'indeterminate'
          : table.getIsAllPageRowsSelected(),
        'onUpdate:modelValue': value => table.toggleAllPageRowsSelected(!!value),
        'aria-label': 'Select all',
      }),
    cell: ({ row }) =>
      h(UCheckbox, {
        'modelValue': row.getIsSelected(),
        'onUpdate:modelValue': value => row.toggleSelected(!!value),
        'aria-label': 'Select row',
      }),
    enableHiding: false,
  },
  {
    accessorKey: 'id',
    header: ({ column }) => sortableHeader(column, '#'),
  },
  {
    accessorKey: 'displayName',
    header: ({ column }) => sortableHeader(column, columnNameMap.displayName),
    cell: ({ row }) => {
      const name = row.original.displayName
      return h(ULink,
        {
          to: localePath(`/groups/${row.original.id}`),
          class: 'font-bold hover:underline inline-flex items-center',
        },
        [
          h('span', name),
          h(UIcon, { name: 'i-lucide-chevron-right', class: 'size-5 shrink-0' }),
        ])
    },
    enableHiding: false,
  },
  {
    accessorKey: 'isPublic',
    header: ({ column }) => sortableHeader(column, columnNameMap.publicStatus),
    cell: ({ row }) => {
      return row.original.isPublic
        ? h(UBadge, { color: 'success', variant: 'solid', size: 'sm' }, $t('group.public-badge'))
        : h(UBadge, { color: 'error', variant: 'solid', size: 'sm' }, $t('group.private-badge'))
    },
  },
  {
    accessorKey: 'joinCondition',
    header: ({ column }) => sortableHeader(column, columnNameMap.joinCondition),
    cell: ({ row }) => {
      const condition = row.original.joinCondition
      const labelMap = {
        'open': $t('group.open-to-join'),
        'approval': $t('group.approval-required'),
        'invite-only': $t('group.invite-only'),
      } as const

      return labelMap[condition]
    },
  },
  {
    accessorKey: 'memberVisibility',
    header: ({ column }) => sortableHeader(column, columnNameMap.memberVisibility),
    cell: ({ row }) => {
      const visibility = row.original.memberVisibility
      const labelMap = {
        public: $t('group.members-public'),
        private: $t('group.members-private'),
        hidden: $t('group.members-hidden'),
      } as const

      return labelMap[visibility]
    },
  },
])

const table = useTemplateRef('table')

const columnVisibility = ref({ id: false })

type Column = Parameters<
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  Extract<GroupTableColumn['header'], (...arguments_: any) => any>
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

const page = ref(1)
const pageSize = ref(5)
const pageOptions = ref([5, 10, 20])

const globalFilter = ref('')
const filteredData = computed(() => {
  if (!globalFilter.value) return data.value
  const f = globalFilter.value.toLowerCase()
  return data.value.filter(item => item.displayName.toLowerCase().includes(f))
})
const pagedData = computed(() => {
  const start = (page.value - 1) * pageSize.value
  return filteredData.value.slice(start, start + pageSize.value)
})
const displayInfo = computed(() => {
  const total = filteredData.value.length
  const start = (page.value - 1) * pageSize.value + 1
  const end = Math.min(page.value * pageSize.value, total)

  return $t('table.display-info-text', { start, end, total })
})

const isNotZero = data.value.length > 0
const isCreatable = true

const filterStatus = reactive({
  repositoryFilter: false,
  publicStatusFilter: false,
  joinConditionFilter: false,
  memberVisibilityFilter: false,
})

const filterItems = computed<DropdownMenuItem[]>(() => [
  {
    label: $t('group.repository-filter'),
    type: 'checkbox' as const,
    checked: filterStatus.repositoryFilter,
    onUpdateChecked(checked: boolean) {
      filterStatus.repositoryFilter = checked
    },
  },
  {
    label: $t('group.public-status-filter'),
    type: 'checkbox' as const,
    checked: filterStatus.publicStatusFilter,
    onUpdateChecked(checked: boolean) {
      filterStatus.publicStatusFilter = checked
    },
  },
  {
    label: $t('group.join-condition-filter'),
    type: 'checkbox' as const,
    checked: filterStatus.joinConditionFilter,
    onUpdateChecked(checked: boolean) {
      filterStatus.joinConditionFilter = checked
    },
  },
  {
    label: $t('group.member-visibility-filter'),
    type: 'checkbox' as const,
    checked: filterStatus.memberVisibilityFilter,
    onUpdateChecked(checked: boolean) {
      filterStatus.memberVisibilityFilter = checked
    },
  },
])
const repositoryNames = ref(repositories.map(repo => repo.displayName))
const publicStatus = ref([$t('group.public-badge'), $t('group.private-badge')])
const joinConditions = ref([
  $t('group.open-to-join'), $t('group.approval-required'), $t('group.invite-only'),
])
const memberVisibilities = ref([
  $t('group.members-public'), $t('group.members-private'), $t('group.members-hidden'),
])

const rowSelection = ref<Record<string, boolean>>({})
const selectedGroups = computed(() => {
  const selectedIds = new Set(Object.entries(rowSelection.value)
    .filter(([, isSelected]) => isSelected)
    .map(([id]) => id))

  return data.value.filter((group, index) => selectedIds.has(index.toString()))
})

function onSelect(first: Event | TableRow<Group>, second: Event | TableRow<Group>) {
  const row = 'original' in first ? first : second as TableRow<Group>
  row.toggleSelected(!row.getIsSelected())
}
</script>

<template>
  <div class="flex justify-center p-6">
    <UCard class="w-full max-w-6xl">
      <h2 class="text-2xl font-semibold">
        {{ $t('group.list-title') }}
      </h2>
      <div v-if="isNotZero">
        <div class="flex justify-between items-center mt-4">
          <UButton
            v-if="isCreatable"
            color="primary" :label="$t('group.create-button')"
            variant="solid" icon="i-lucide-plus" :to="localePath('/groups/create')" class="mb-4"
          />

          <UModal
            v-if="selectedGroups.length > 0"
            :title="$t('group.delete-confirmation-title', { count: selectedGroups.length })"
            :description="$t('group.delete-confirmation-description')"
            :ui="{ footer: 'justify-end' }" :close="false"
          >
            <UButton
              color="error" variant="outline" class="mb-4 ml-auto"
              :label="$t('group.delete-selected-groups-button')"
            />
            <template #body>
              <div class="flex flex-col justify-between items-center mt-4">
                <div class="gap-4 text-center">
                  <div v-for="group in selectedGroups" :key="group.id" class="mb-2">
                    <p>
                      {{ group.displayName }}
                      ({{ $t('group.members-count', { count: group.members?.length || 0 }) }})
                    </p>
                  </div>
                </div>
              </div>
            </template>
            <template #footer="{ close }">
              <div class="flex gap-2">
                <UButton
                  color="neutral" :label="$t('modal.cancel-button')"
                  variant="subtle" @click="close"
                />
                <UButton color="error" :label="$t('modal.delete-button')" @click="close" />
              </div>
            </template>
          </UModal>
        </div>

        <div class="flex justify-between mb-4">
          <div>
            <div>
              <UInput
                v-model="globalFilter" :placeholder="$t('search-placeholder')"
                icon="i-lucide-search" class="max-w-sm pr-4"
              />
              <UDropdownMenu :items="filterItems">
                <UButton
                  :label="$t('table.add-filter-button')" color="neutral"
                  trailing-icon="i-lucide-chevron-down" variant="outline"
                />
              </UDropdownMenu>
            </div>
            <div class="flex flex-col">
              <USelectMenu
                v-if="filterStatus.repositoryFilter"
                :placeholder="$t('group.repository-filter')"
                icon="i-lucide-folder" :items="repositoryNames" class="mt-2" multiple
              />
              <USelectMenu
                v-if="filterStatus.publicStatusFilter"
                :placeholder="$t('group.public-status')"
                :items="publicStatus" :search-input="false" class="mt-2" multiple
              />
              <USelectMenu
                v-if="filterStatus.joinConditionFilter"
                :placeholder="$t('group.join-condition-filter')"
                :items="joinConditions" :search-input="false" class="mt-2" multiple
              />
              <USelectMenu
                v-if="filterStatus.memberVisibilityFilter"
                :placeholder="$t('group.member-visibility-filter')"
                :items="memberVisibilities" :search-input="false" class="mt-2" multiple
              />
            </div>
          </div>

          <div class="flex justify-end items-center space-x-2 mb-2">
            <UDropdownMenu
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
                color="neutral" variant="outline"
                trailing-icon="i-lucide-chevron-down" :label="$t('table.display-item-label')"
              />
            </UDropdownMenu>

            <div class="flex items-center space-x-2">
              <span class="text-sm text-gray-600">{{ $t('table.display-count-label') }}</span>
              <USelect v-model="pageSize" :items="pageOptions" class="w-24" />
            </div>
          </div>
        </div>

        <div>
          <UTable
            ref="table"
            v-model:column-visibility="columnVisibility"
            v-model:sorting="sorting"
            v-model:global-filter="globalFilter"
            v-model:row-selection="rowSelection"
            :data="pagedData" :columns="columns" @select="onSelect"
          />

          <div class="flex justify-center mt-4">
            <div class="flex-1 text-gray-500 text-sm">
              {{ displayInfo }}
            </div>
            <div class="flex-2 flex justify-center">
              <UPagination
                v-model:page="page"
                :items-per-page="pageSize"
                :total="data.length"
              />
            </div>
            <div class="flex-1" />
          </div>
        </div>
      </div>
      <div v-if="!isNotZero">
        <UEmpty
          :title="$t('group.no-users-title')"
          :actions="[{
            icon: 'i-lucide-plus',
            label: $t('group.create-button'),
            to: 'groups/create',
          }, {
            icon: 'i-lucide-refresh-cw',
            label: $t('reload-button'),
            color: 'neutral',
            variant: 'subtle',
          }]"
        />
      </div>
    </UCard>
  </div>
</template>
