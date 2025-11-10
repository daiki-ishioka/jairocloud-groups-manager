<template>
  <UApp :toaster="{ position: 'top-center' }">
    <AppHeader />

    <UMain>
      <UContainer>
        <div class="flex gap-8 min-h-[calc(100vh-var(--ui-header-height))]">
          <AppSideMenu />

          <UPageBody class="flex-1 flex flex-col min-w-0 pb-0">
            <slot />

            <AppFooter />
          </UPageBody>
        </div>
      </UContainer>
    </UMain>
  </UApp>
</template>
