<script setup lang="ts">
import type { Collections } from '@nuxt/content'

const route = useRoute()
const category = route.path.split('/').find(segment => segment.length > 0) as keyof Collections

const { data: page } = await useAsyncData(`page-${route.path}`, () => {
  return queryCollection(category).path(route.path).first()
})

if (!page.value) {
  throw createError({ statusCode: 404, statusMessage: 'Page not found', fatal: true })
}

const { data: surround } = await useAsyncData(`${route.path}-surround`, () => {
  return queryCollectionItemSurroundings(category, route.path, {
    fields: ['description'],
  })
})
</script>

<template>
  <UPage v-if="page">
    <UPageHeader :title="page.title" :description="page.description" />

    <UPageBody>
      <ContentRenderer v-if="page.body" :value="page" />

      <USeparator v-if="surround?.length" />
      <UContentSurround :surround="surround" />
    </UPageBody>

    <template
      v-if="page?.body?.toc?.links?.length"
      #right
    >
      <UContentToc :links="page.body.toc.links" />
    </template>
  </UPage>
</template>
