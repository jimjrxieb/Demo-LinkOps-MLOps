import js from '@eslint/js';
import vue from 'eslint-plugin-vue';

export default [
  {
    ignores: [
      '**/node_modules/**',
      '**/dist/**',
      '**/coverage/**',
      '**/.git/**',
      '**/public/**',
      '**/*.config.js',
      '**/vite.config.js',
      '**/tailwind.config.js',
      '**/postcss.config.js',
      '**/test-*.js',
      '**/index.js'
    ],
  },
  js.configs.recommended,
  {
    files: ['**/*.vue'],
    ...vue.configs['vue3-essential'],
    languageOptions: {
      ecmaVersion: 'latest',
      sourceType: 'module',
      globals: {
        console: 'readonly',
        window: 'readonly',
        document: 'readonly',
        process: 'readonly'
      }
    },
    rules: {
      'no-console': 'off',
      'no-debugger': process.env.NODE_ENV === 'production' ? 'warn' : 'off',
      'vue/multi-word-component-names': 'off',
      'vue/no-unused-vars': 'warn',
      'vue/valid-template-root': 'error',
      'vue/no-parsing-error': 'error'
    },
  },
  {
    files: ['**/*.js', '**/*.mjs', '**/*.cjs'],
    languageOptions: {
      ecmaVersion: 'latest',
      sourceType: 'module',
      globals: {
        console: 'readonly',
        window: 'readonly',
        document: 'readonly',
        process: 'readonly'
      }
    },
    rules: {
      'no-console': 'off',
      'no-debugger': process.env.NODE_ENV === 'production' ? 'warn' : 'off',
      'no-unused-vars': 'warn'
    },
  },
]; 