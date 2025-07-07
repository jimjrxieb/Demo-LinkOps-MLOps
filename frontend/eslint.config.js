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
    },
    rules: {
      'no-console': process.env.NODE_ENV === 'production' ? 'warn' : 'off',
      'no-debugger': process.env.NODE_ENV === 'production' ? 'warn' : 'off',
      'vue/multi-word-component-names': 'off',
    },
  },
  {
    files: ['**/*.js', '**/*.mjs', '**/*.cjs'],
    languageOptions: {
      ecmaVersion: 'latest',
      sourceType: 'module',
    },
    rules: {
      'no-console': process.env.NODE_ENV === 'production' ? 'warn' : 'off',
      'no-debugger': process.env.NODE_ENV === 'production' ? 'warn' : 'off',
    },
  },
]; 