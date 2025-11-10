// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  modules: [
    '@nuxt/eslint',
    '@nuxt/test-utils',
    '@nuxt/ui',
    '@nuxtjs/i18n',
  ],
  ssr: false,
  imports: {
    dirs: ['~/types'],
  },
  devtools: { enabled: true },
  app: {
    baseURL: '/',
  },
  css: ['~/assets/css/main.css'],
  build: {
    transpile: ['@@nuxt/ui'],
  },
  compatibilityDate: '2025-07-15',
  nitro: {
    preset: 'static',
  },
  eslint: {
    config: {
      stylistic: true,
    },
  },
  i18n: {
    locales: [
      { code: 'en', iso: 'es-US', file: 'en.json', name: 'English' },
      { code: 'ja', iso: 'ja-JP', file: 'ja.json', name: '日本語' },
    ],
    defaultLocale: 'ja',
    detectBrowserLanguage: false,
    restructureDir: 'app/i18n',
  },
})
