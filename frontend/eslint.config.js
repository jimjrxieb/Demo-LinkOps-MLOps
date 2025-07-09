import js from '@eslint/js'
import pluginVue from 'eslint-plugin-vue'
import globals from 'globals'

export default [
  {
    name: 'app/files-to-lint',
    files: ['**/*.{js,mjs,jsx,vue}'],
  },

  {
    name: 'app/files-to-ignore',
    ignores: ['**/dist/**', '**/dist-ssr/**', '**/coverage/**'],
  },

  js.configs.recommended,
  ...pluginVue.configs['flat/recommended'],

  {
    name: 'app/vue-rules',
    files: ['**/*.vue'],
    languageOptions: {
      globals: {
        ...globals.browser,
      },
    },
    rules: {
      // Disable problematic rules for our use case
      'no-unused-vars': 'warn',
      'vue/multi-word-component-names': 'off',
      'vue/no-unused-vars': 'warn',
      
      // Allow template literals with embedded code
      'no-template-curly-in-string': 'off',
      
      // Allow console for development
      'no-console': 'warn',
      
      // Vue-specific rules
      'vue/attribute-hyphenation': 'error',
      'vue/v-on-event-hyphenation': 'error',
    },
  },

  {
    name: 'app/javascript-rules',
    files: ['**/*.{js,mjs,jsx}'],
    languageOptions: {
      globals: {
        ...globals.browser,
        ...globals.node,
      },
    },
    rules: {
      'no-unused-vars': 'warn',
      'no-console': 'warn',
    },
  },
];