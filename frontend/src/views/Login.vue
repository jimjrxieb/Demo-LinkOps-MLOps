<template>
  <div class="min-h-screen flex items-center justify-center bg-teal-400">
    <div
      class="relative w-full max-w-sm p-8 rounded-xl shadow-xl bg-teal-800/70 backdrop-blur-md text-white border border-teal-100"
    >
      <!-- Icon -->
      <div class="flex justify-center mb-4">
        <svg
          class="h-12 w-12 text-teal-200"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="1.5"
            d="M3 5h18M5 7v12h14V7M8 10h8v4H8z"
          />
        </svg>
      </div>

      <!-- Title -->
      <h2 class="text-center text-lg tracking-widest font-semibold mb-6">
        USER LOGIN
      </h2>

      <!-- Form -->
      <form
        class="space-y-4"
        novalidate
        @submit.prevent="doLogin"
      >
        <input
          type="hidden"
          :value="csrfToken"
          name="csrf_token"
        >

        <!-- Username -->
        <div class="relative">
          <span
            class="absolute left-3 top-1/2 transform -translate-y-1/2 text-teal-200"
          >
            <svg
              class="h-5 w-5"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="1.5"
                d="M16 12H8m0 0l4-4m-4 4l4 4"
              />
            </svg>
          </span>
          <input
            v-model.trim="form.username"
            type="text"
            placeholder="Username"
            autocomplete="username"
            :disabled="loading || isLockedOut"
            :class="[
              'w-full bg-transparent border-b pl-10 pr-3 py-2 placeholder-teal-100 focus:outline-none focus:ring-0',
              v$.username.$error
                ? 'border-red-300 focus:border-red-300'
                : 'border-teal-200 focus:border-white',
            ]"
            @blur="v$.username.$touch()"
          >
          <p
            v-if="v$.username.$error"
            class="mt-1 text-xs text-red-300"
          >
            <span v-if="!v$.username.required">Username is required.</span>
            <span v-else-if="!v$.username.minLength">Must be at least 3 characters.</span>
          </p>
        </div>

        <!-- Password -->
        <div class="relative">
          <span
            class="absolute left-3 top-1/2 transform -translate-y-1/2 text-teal-200"
          >
            <svg
              class="h-5 w-5"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="1.5"
                d="M12 11c.828 0 1.5.895 1.5 2s-.672 2-1.5 2-1.5-.895-1.5-2 .672-2 1.5-2z"
              />
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="1.5"
                d="M4 12c0-4.418 3.582-8 8-8s8 3.582 8 8-3.582 8-8 8-8-3.582-8-8z"
              />
            </svg>
          </span>
          <input
            v-model.trim="form.password"
            :type="showPassword ? 'text' : 'password'"
            placeholder="Password"
            autocomplete="current-password"
            :disabled="loading || isLockedOut"
            :class="[
              'w-full bg-transparent border-b pl-10 pr-3 py-2 placeholder-teal-100 focus:outline-none focus:ring-0',
              v$.password.$error
                ? 'border-red-300 focus:border-red-300'
                : 'border-teal-200 focus:border-white',
            ]"
            @blur="v$.password.$touch()"
          >
          <button
            type="button"
            :disabled="loading || isLockedOut"
            class="absolute right-3 top-1/2 transform -translate-y-1/2 text-teal-200 hover:text-white disabled:opacity-50"
            aria-label="Toggle password visibility"
            @click="showPassword = !showPassword"
          >
            <svg
              v-if="showPassword"
              class="h-5 w-5"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="1.5"
                d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"
              />
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="1.5"
                d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"
              />
            </svg>
            <svg
              v-else
              class="h-5 w-5"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="1.5"
                d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.542-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.542 7a10.025 10.025 0 01-4.132 5.411m0 0L21 21"
              />
            </svg>
          </button>
          <p
            v-if="v$.password.$error"
            class="mt-1 text-xs text-red-300"
          >
            <span v-if="!v$.password.required">Password is required.</span>
            <span v-else-if="!v$.password.minLength">Must be at least 6 characters.</span>
          </p>
        </div>

        <!-- Rate Limit & Error Messages -->
        <div class="space-y-2">
          <p
            v-if="isLockedOut"
            class="text-sm text-red-300 text-center"
          >
            Too many attempts. Try again in {{ lockoutRemaining }}m.
          </p>
          <p
            v-else-if="attemptsLeft < maxAttempts"
            class="text-sm text-teal-100 text-center"
          >
            {{ attemptsLeft }}
            {{ attemptsLeft === 1 ? 'attempt' : 'attempts' }} remaining
          </p>
          <p
            v-if="errorMsg"
            class="text-sm text-red-300 text-center"
          >
            {{ errorMsg }}
          </p>
        </div>

        <!-- Login Button -->
        <button
          type="submit"
          :disabled="v$.$invalid || loading || isLockedOut"
          class="w-full mt-2 py-2 bg-black hover:bg-gray-900 rounded-md text-white font-semibold transition disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center"
        >
          <svg
            v-if="loading"
            class="animate-spin -ml-1 mr-2 h-5 w-5 text-white"
            fill="none"
            viewBox="0 0 24 24"
          >
            <circle
              class="opacity-25"
              cx="12"
              cy="12"
              r="10"
              stroke="currentColor"
              stroke-width="4"
            />
            <path
              class="opacity-75"
              fill="currentColor"
              d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
            />
          </svg>
          {{ loading ? 'SIGNING IN...' : 'LOGIN' }}
        </button>

        <!-- Demo Note -->
        <p class="text-xs mt-4 text-center text-teal-200">
          Demo access: <strong>linkops-demo</strong> / <strong>demo123</strong>
        </p>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onUnmounted } from 'vue';
import useVuelidate from '@vuelidate/core';
import { required, minLength } from '@vuelidate/validators';
import axios from 'axios';
import { useMainStore } from '@/store/useMainStore';
import { useRouter } from 'vue-router';

// Form state
const form = ref({ username: '', password: '' });
const showPassword = ref(false);
const loading = ref(false);
const errorMsg = ref('');
const csrfToken =
  document.querySelector('meta[name="csrf-token"]')?.content || '';

// Validation
const rules = {
  username: { required, minLength: minLength(3) },
  password: { required, minLength: minLength(6) },
};
const v$ = useVuelidate(rules, form);

// Rate limiting
const maxAttempts = 5;
const resetMinutes = 60;
const attempts = ref(0);
const lockoutUntil = ref(null);
let lockoutTimer = null;

const store = useMainStore();
const router = useRouter();

// Computed
const attemptsLeft = computed(() => Math.max(0, maxAttempts - attempts.value));
const isLockedOut = computed(
  () => lockoutUntil.value && new Date() < lockoutUntil.value
);
const lockoutRemaining = computed(() =>
  lockoutUntil.value ? Math.ceil((lockoutUntil.value - Date.now()) / 60000) : 0
);

// Cleanup
onUnmounted(() => clearTimeout(lockoutTimer));

async function doLogin() {
  v$.$touch();
  if (v$.$invalid || loading.value || isLockedOut.value) return;

  loading.value = true;
  errorMsg.value = '';

  try {
    const res = await axios.post('/auth/login', {
      username: form.value.username,
      password: form.value.password,
      csrf_token: csrfToken,
    });

    // Handle successful login
    store.setToken(res.data.access_token);
    store.setRole(res.data.role);
    router.push('/');
  } catch (err) {
    attempts.value++;
    if (attempts.value >= maxAttempts) {
      lockoutUntil.value = new Date(Date.now() + resetMinutes * 60000);
      lockoutTimer = setTimeout(() => {
        attempts.value = 0;
        lockoutUntil.value = null;
      }, resetMinutes * 60000);
      errorMsg.value = 'Too many attempts—try again later.';
    } else {
      errorMsg.value =
        err.response?.status === 429
          ? 'Rate limited—please wait.'
          : 'Invalid credentials.';
    }
  } finally {
    loading.value = false;
  }
}
</script>

<style scoped>
/* loader spinner animation handled by Tailwind utility classes */
</style>
