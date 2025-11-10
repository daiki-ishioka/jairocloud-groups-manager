<script setup lang="ts">
import { upperFirst } from 'scule'
import { DateFormatter, getLocalTimeZone } from '@internationalized/date'

import type { CalendarDate } from '@internationalized/date'
import type { DropdownMenuItem, TableColumn, TableRow } from '@nuxt/ui'

import { UButton, UCheckbox, UIcon, ULink } from '#components'

const toast = useToast()
const localePath = useLocalePath()
const { users, repositories, groups } = useDataStore()
const data = ref<User[]>(users)

const columnNameMap = {
  displayName: $t('user.name-column'),
  email: $t('user.email-column'),
  eppn: $t('user.eppn-column'),
  lastModified: $t('user.last-modified-column'),
} as const

type UserTableColumn = TableColumn<User>
const columns = computed<UserTableColumn[]>(() => [
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
          to: localePath(`/users/${row.original.id}`),
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
    accessorKey: 'email',
    header: ({ column }) => sortableHeader(column, columnNameMap.email),
  },
  {
    accessorKey: 'eppn',
    header: ({ column }) => sortableHeader(column, columnNameMap.eppn),
  },
  {
    accessorKey: 'lastModified',
    header: ({ column }) => sortableHeader(column, columnNameMap.lastModified),
  },
])

const table = useTemplateRef('table')

const columnVisibility = ref({ id: false })

type Column = Parameters<
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  Extract<UserTableColumn['header'], (...arguments_: any) => any>
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
  return data.value.filter(
    item =>
      item.displayName.toLowerCase().includes(f)
      || item.email?.toLowerCase().includes(f)
      || item.eppn.toLowerCase().includes(f),
  )
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
  repoFilter: false,
  roleFilter: false,
  groupFilter: false,
  lastModifiedFilter: false,
})
const filterItems = computed<DropdownMenuItem[]>(() => [
  {
    label: $t('user.repository-filter'),
    type: 'checkbox' as const,
    checked: filterStatus.repoFilter,
    onUpdateChecked(checked: boolean) {
      filterStatus.repoFilter = checked
    },
  },
  {
    label: $t('user.role-filter'),
    type: 'checkbox' as const,
    checked: filterStatus.roleFilter,
    onUpdateChecked(checked: boolean) {
      filterStatus.roleFilter = checked
    },
  },
  {
    label: $t('user.group-filter'),
    type: 'checkbox' as const,
    checked: filterStatus.groupFilter,
    onUpdateChecked(checked: boolean) {
      filterStatus.groupFilter = checked
    },
  },
  {
    label: $t('user.last-modified-filter'),
    type: 'checkbox' as const,
    checked: filterStatus.lastModifiedFilter,
    onUpdateChecked(checked: boolean) {
      filterStatus.lastModifiedFilter = checked
    },
  },
])
const repositoryNames = ref(repositories.map(repo => repo.displayName))
const userRoles = ref([
  $t('user.role.admin'), $t('user.role.repo_admin'), $t('user.role.community_admin'),
  $t('user.role.contributor'), $t('user.role.general'),
])
const userGroupNames = ref(groups.map(group => group.displayName))

const df = new DateFormatter('ja-JP', {
  dateStyle: 'medium',
})
const dateRange = shallowRef<{ start: CalendarDate | undefined, end: CalendarDate | undefined }>({
  start: undefined,
  end: undefined,
})

const displayValue = computed(() => {
  if (!dateRange.value.start) return ''

  const startDate = df.format(dateRange.value.start.toDate(getLocalTimeZone()))
  const endDate = dateRange.value.end
    ? df.format(dateRange.value.end.toDate(getLocalTimeZone()))
    : ''

  return endDate ? `${startDate} - ${endDate}` : startDate
})

const rowSelection = ref<Record<string, boolean>>({})
const selectedUsers = computed(() => {
  const selectedIds = new Set(Object.entries(rowSelection.value)
    .filter(([, isSelected]) => isSelected)
    .map(([id]) => id))

  return data.value.filter((user, index) => selectedIds.has(index.toString()))
})

function onSelect(first: Event | TableRow<User>, second: Event | TableRow<User>) {
  const row = 'original' in first ? first : second as TableRow<User>
  row.toggleSelected(!row.getIsSelected())
}

function deleteUsers(close: () => void) {
  const count = selectedUsers.value.length
  if (count === 0) return

  const selectedIds = new Set(selectedUsers.value.map(user => user.id))
  data.value = data.value.filter(user => !selectedIds.has(user.id))
  rowSelection.value = {}

  close()
  toast.add({
    title: $t('toast.delete-success-title'),
    description: $t('user.toast-delete-success'),
    color: 'success',
    icon: 'i-lucide-check-circle',
  })
}
</script>

<template>
  <div class="flex justify-center p-6">
    <UCard class="w-full max-w-6xl">
      <h2 class="text-2xl font-semibold">
        {{ $t('user.list-title') }}
      </h2>

      <div v-if="isNotZero">
        <div class="flex justify-between items-center mt-4">
          <UButton
            v-if="isCreatable"
            color="primary" :label="$t('user.create-button')"
            variant="solid" icon="i-lucide-plus" :to="localePath('/users/create')" class="mb-4"
          />

          <UModal
            v-if="selectedUsers.length > 0"
            :title="$t('user.delete-confirmation-title', { count: selectedUsers.length })"
            :description="$t('user.delete-confirmation-description')"
            :ui="{ footer: 'justify-end' }" :close="false"
          >
            <UButton
              color="error" variant="outline" class="mb-4 ml-auto"
              :label="$t('user.delete-selected-users-button', { count: selectedUsers.length })"
            />
            <template #body>
              <div class="flex flex-col justify-between items-center mt-4">
                <div class="gap-4 text-center">
                  <div v-for="user in selectedUsers" :key="user.id" class="mb-2">
                    <p>
                      {{ user.displayName }} ({{ user.email }})
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
                <UButton
                  color="error"
                  :label="$t('modal.delete-button')" @click="deleteUsers(close)"
                />
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
                v-if="filterStatus.repoFilter"
                :placeholder="$t('user.repository-filter')"
                icon="i-lucide-folder" :items="repositoryNames" class="mt-2" multiple
              />
              <USelectMenu
                v-if="filterStatus.roleFilter"
                :placeholder="$t('user.role-filter')"
                icon="i-lucide-user" :items="userRoles" :search-input="false" class="mt-2"
                multiple
              />
              <USelectMenu
                v-if="filterStatus.groupFilter"
                :placeholder="$t('user.group-filter')"
                icon="i-lucide-users" :items="userGroupNames" class="mt-2" multiple
              />
              <UPopover v-if="filterStatus.lastModifiedFilter">
                <UInput
                  icon="i-lucide-calendar"
                  :placeholder="$t('user.last-modified-filter')"
                  :model-value="displayValue" class="mt-2" :ui="{ base: 'text-left' }" readonly
                />

                <template #content>
                  <UCalendar v-model="dateRange" :number-of-months="2" class="p-2" range />
                </template>
              </UPopover>
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
          :title="$t('user.no-users-title')"
          :actions="[{
            icon: 'i-lucide-plus',
            label: $t('user.create-button'),
            to: 'users/create',
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
