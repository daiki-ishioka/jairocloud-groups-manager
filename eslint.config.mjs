// @ts-check
import unicorn from 'eslint-plugin-unicorn'
import { globalIgnores } from 'eslint/config'

import withNuxt from './.nuxt/eslint.config.mjs'

export default withNuxt([
  // Your custom configs here
  unicorn.configs.recommended,
  globalIgnores(['htmlcov/', '.tox/']),
  {
    name: 'stylistic',
    rules: {
      'camelcase': ['error', { properties: 'always' }],
      'no-console': 'error',
      'vue/first-attribute-linebreak': ['error', { singleline: 'beside', multiline: 'below' }],
      'vue/max-attributes-per-line': [
        'warn', { singleline: { max: 4 }, multiline: { max: 4 } },
      ],
      '@stylistic/function-call-spacing': ['error', 'never'],
      '@stylistic/max-len': ['error', { code: 100 }],
    },
  },
  {
    name: 'sort-imports',
    rules: {
      'sort-imports': ['error', {
        ignoreCase: false,
        ignoreDeclarationSort: true,
        ignoreMemberSort: false,
      }],
      'import/order': ['error', {
        'groups': ['builtin', 'external', 'parent', 'sibling', 'index', 'object', 'type'],
        'newlines-between': 'always',
      }],
    },
  },
  {
    files: ['**/app/**/*.vue'],
    rules: {
      'unicorn/filename-case': [
        'error', { case: 'pascalCase', ignore: ['app.vue'] },
      ],
      'vue/no-multiple-template-root': 'off',
    },
  },
  {
    files: ['**/app/**/*.{ts,js}'],
    rules: {
      'unicorn/filename-case': ['error', { case: 'camelCase' }],
    },
  },
  {
    files: ['**/app/{pages,layouts}/**/*.vue'],
    rules: {
      'unicorn/filename-case': ['error', { case: 'kebabCase' }],
    },
  },
])
