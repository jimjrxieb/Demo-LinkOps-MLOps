<template>
  <div class="login-container">
    <div class="login-card">
      <h2>DEMO-LinkOps Login</h2>
      <div class="form-group">
        <input 
          v-model="user" 
          placeholder="Username" 
          class="form-input"
          @keyup.enter="doLogin"
        />
      </div>
      <div class="form-group">
        <input 
          v-model="pass" 
          placeholder="Password" 
          type="password" 
          class="form-input"
          @keyup.enter="doLogin"
        />
      </div>
      <button @click="doLogin" class="login-button" :disabled="loading">
        {{ loading ? 'Logging in...' : 'Login' }}
      </button>
      <p v-if="error" class="error-message">{{ error }}</p>
      <div class="demo-info">
        <p><strong>Demo Accounts:</strong></p>
        <p>Slim Demo: demo-slim / demo</p>
        <p>Full Demo: demo-full / arise!</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useMainStore } from '@/store/useMainStore'
import axios from 'axios'

const router = useRouter()
const store = useMainStore()

const user = ref('')
const pass = ref('')
const error = ref('')
const loading = ref(false)

const doLogin = async () => {
  if (!user.value || !pass.value) {
    error.value = 'Please enter both username and password'
    return
  }

  loading.value = true
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
    error.value = e.response?.data?.detail || 'Login failed'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: #f5f5f5;
}

.login-card {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 400px;
}

h2 {
  text-align: center;
  color: #333;
  margin-bottom: 2rem;
}

.form-group {
  margin-bottom: 1rem;
}

.form-input {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
}

.login-button {
  width: 100%;
  padding: 0.75rem;
  background: #4a90e2;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 1rem;
  cursor: pointer;
  transition: background 0.2s;
}

.login-button:hover {
  background: #357abd;
}

.login-button:disabled {
  background: #ccc;
  cursor: not-allowed;
}

.error-message {
  color: #dc3545;
  text-align: center;
  margin-top: 1rem;
}

.demo-info {
  margin-top: 2rem;
  padding-top: 1rem;
  border-top: 1px solid #eee;
  font-size: 0.9rem;
  color: #666;
}

.demo-info p {
  margin: 0.5rem 0;
}
</style> 