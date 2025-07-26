<template>
  <div class="login-container p-4 max-w-sm mx-auto">
    <h2 class="text-2xl font-semibold mb-4">Login to DEMO-LinkOps</h2>
    <form @submit.prevent="doLogin" class="space-y-4">
      <div>
        <label for="username" class="block text-sm font-medium">User:</label>
        <input
          id="username"
          v-model="user"
          placeholder="Username"
          class="mt-1 block w-full border rounded p-2"
        />
      </div>
      <div>
        <label for="password" class="block text-sm font-medium">Password:</label>
        <input
          id="password"
          v-model="pass"
          type="password"
          placeholder="Password"
          class="mt-1 block w-full border rounded p-2"
        />
      </div>
      <button
        type="submit"
        class="w-full py-2 px-4 bg-blue-600 text-white rounded hover:bg-blue-700"
      >
        Login
      </button>
    </form>

    <p class="mt-4 text-sm text-gray-600">
      <strong>Demo access:</strong> use <code>linkops-demo</code> / <code>demo123</code>
    </p>
    <p v-if="error" class="mt-2 text-red-600">{{ error }}</p>
  </div>
</template>

<script>
import axios from 'axios'
import { useMainStore } from '@/store/useMainStore'
import { useRouter } from 'vue-router'
import { ref } from 'vue'

export default {
  setup() {
    const store = useMainStore()
    const router = useRouter()
    const user = ref('')
    const pass = ref('')
    const error = ref('')

    const doLogin = async () => {
      error.value = ''
      try {
        const res = await axios.post('/auth/login', {
          username: user.value,
          password: pass.value
        })
        store.setToken(res.data.access_token)
        store.setRole(res.data.role)
        router.push('/')
      } catch (e) {
        error.value = 'Login failed'
      }
    }

    return { user, pass, error, doLogin }
  }
}
</script>

<style scoped>
.login-container {
  background: white;
  border-radius: 0.5rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}
</style> 