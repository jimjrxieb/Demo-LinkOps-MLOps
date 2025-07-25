<template>
  <div id="app">
    <router-view></router-view>
    <SessionTimer v-if="store.isAuthenticated" />
  </div>
</template>

<script setup>
import { useMainStore } from '@/store/useMainStore'
import SessionTimer from '@/components/SessionTimer.vue'

const store = useMainStore()
</script>

<style>
#app {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}
</style>
