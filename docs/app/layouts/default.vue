<script setup lang="ts">
import type { Collections } from '@nuxt/content'

const route = useRoute()
const category = computed<keyof Collections>(() => {
  const pathHead = route.path.split('/').find(segment => segment.length > 0)
  return pathHead ? pathHead as keyof Collections : 'detailed'
})

const { data: navigation } = await useAsyncData(() => `navigation-${category.value}`,
  () => queryCollectionNavigation(category.value),
  {
    transform: (data) => {
      return data?.find(item => item.path === `/${category.value}`)?.children || data || []
    },
    watch: [category],
  },
)
const { data: files } = useLazyAsyncData(
  () => `search-${category.value}`,
  () => queryCollectionSearchSections(category.value as keyof Collections),
  {
    server: false,
    watch: [category],
  },
)
</script>

<template>
  <UApp>
    <UMain>
      <UContainer>
        <UPage>
          <template #left>
            <UPageAside>
              <template #top>
                <UContentSearchButton :collapsed="false" :kbds="['/']" />
              </template>

              <UContentNavigation
                :navigation="navigation"
                highlight
              />
            </UPageAside>
          </template>

          <slot />
        </UPage>
      </UContainer>
    </UMain>

    <LazyUContentSearch
      :files="files"
      shortcut="/"
      :navigation="navigation"
      :fuse="{ resultLimit: 42 }"
    />
  </UApp>
</template>
