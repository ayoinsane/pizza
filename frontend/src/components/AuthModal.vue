<template>
  <div class="fixed inset-0 z-50 flex items-center justify-center bg-black/40 backdrop-blur-sm">
    <div class="bg-white p-8 rounded-3xl shadow-2xl w-full max-w-md">
      <h2 class="text-2xl font-bold mb-6 text-center">{{ isLogin ? 'Вход' : 'Регистрация' }}</h2>
      
      <form @submit.prevent="submitForm" class="space-y-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Логин</label>
          <input v-model="username" type="text" required class="w-full px-4 py-3 rounded-2xl border border-gray-200 focus:outline-none focus:border-[#E85D04]">
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Пароль</label>
          <input v-model="password" type="password" required class="w-full px-4 py-3 rounded-2xl border border-gray-200 focus:outline-none focus:border-[#E85D04]">
        </div>
        
        <div v-if="error" class="text-red-500 text-sm text-center">{{ error }}</div>
        
        <button type="submit" class="w-full bg-[#E85D04] text-white py-3 rounded-2xl font-bold hover:bg-[#D45403] transition-all">
          {{ isLogin ? 'Войти' : 'Зарегистрироваться' }}
        </button>
      </form>

      <div class="mt-4 text-center text-sm text-gray-600">
        <span v-if="isLogin">Нет аккаунта? </span>
        <span v-else>Уже есть аккаунт? </span>
        <button @click="isLogin = !isLogin" class="text-[#E85D04] font-bold hover:underline">
          {{ isLogin ? 'Создать' : 'Войти' }}
        </button>
      </div>
      
      <button @click="$emit('close')" class="mt-4 w-full text-gray-400 hover:text-gray-600 text-sm">Закрыть</button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import api from '../services/api'

const emit = defineEmits(['close', 'success'])
const isLogin = ref(true)
const username = ref('')
const password = ref('')
const error = ref('')

const submitForm = async () => {
  error.value = ''
  try {
    if (isLogin.value) {
      await api.login(username.value, password.value)
    } else {
      await api.register(username.value, password.value)
    }
    emit('success')
  } catch (e) {
    error.value = e.response?.data?.error || 'Произошла ошибка'
  }
}
</script>