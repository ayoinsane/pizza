<template>
  <div class="min-h-screen bg-[#FDFBF7] text-[#1C1917] font-sans selection:bg-[#E85D04] selection:text-white">
    
    <header class="sticky top-0 z-40 bg-[#FDFBF7]/90 backdrop-blur-md border-b border-[#E7E5E4]">
      <div class="max-w-6xl mx-auto px-4 h-20 flex items-center justify-between">
        <div class="flex items-center gap-3 cursor-pointer" @click="activeTab = 'catalog'">
          <div class="w-10 h-10 rounded-2xl bg-[#E85D04] flex items-center justify-center text-white font-bold text-xl shadow-lg shadow-[#E85D04]/20">
            🍕
          </div>
          <span class="text-xl font-bold tracking-tight">Теплая Пицца</span>
        </div>

        <div class="flex items-center gap-4">
          <button 
            @click="activeTab = 'catalog'"
            class="px-4 py-2 rounded-full font-medium transition-all"
            :class="activeTab === 'catalog' ? 'bg-[#1C1917] text-white' : 'hover:bg-[#F5F2EC] text-[#57534E]'"
          >
            Меню
          </button>
          <button 
            @click="loadOrders(); activeTab = 'orders'"
            class="px-4 py-2 rounded-full font-medium transition-all"
            :class="activeTab === 'orders' ? 'bg-[#1C1917] text-white' : 'hover:bg-[#F5F2EC] text-[#57534E]'"
          >
            Мои заказы
          </button>

          <button 
            @click="isCartOpen = true"
            class="flex items-center gap-2 bg-[#E85D04] hover:bg-[#D45403] text-white px-5 py-2.5 rounded-full font-medium shadow-md shadow-[#E85D04]/20 transition-all active:scale-95"
          >
            <span>Корзина</span>
            <span v-if="cartTotalCount > 0" class="bg-white text-[#E85D04] text-xs font-bold px-2 py-0.5 rounded-full">
              {{ cartTotalCount }}
            </span>
          </button>
        </div>
      </div>
    </header>

    <main class="max-w-6xl mx-auto px-4 py-8">
      
      <div v-if="activeTab === 'catalog'">
        
        <div class="flex items-center gap-2 overflow-x-auto pb-4 mb-8 no-scrollbar">
          <button 
            @click="selectedCategory = null"
            class="px-5 py-2.5 rounded-full text-sm font-medium transition-all whitespace-nowrap"
            :class="selectedCategory === null ? 'bg-[#E85D04] text-white shadow-md shadow-[#E85D04]/20' : 'bg-white border border-[#E7E5E4] text-[#78716C] hover:border-[#1C1917]'"
          >
            Все позиции
          </button>
          <button 
            v-for="cat in categories" 
            :key="cat.id"
            @click="selectedCategory = cat.id"
            class="px-5 py-2.5 rounded-full text-sm font-medium transition-all whitespace-nowrap"
            :class="selectedCategory === cat.id ? 'bg-[#E85D04] text-white shadow-md shadow-[#E85D04]/20' : 'bg-white border border-[#E7E5E4] text-[#78716C] hover:border-[#1C1917]'"
          >
            {{ cat.name }}
          </button>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <div 
            v-for="product in filteredProducts" 
            :key="product.id"
            class="bg-white rounded-3xl p-5 border border-[#E7E5E4]/80 shadow-sm hover:shadow-xl transition-all duration-300 flex flex-col justify-between group"
          >
            <div>
              <div class="relative h-48 rounded-2xl bg-[#F5F2EC] overflow-hidden mb-4">
                <img 
                  v-if="product.image" 
                  :src="product.image" 
                  :alt="product.name" 
                  class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
                >
                <div v-else class="w-full h-full flex items-center justify-center text-4xl">
                  🍕
                </div>
                <span class="absolute top-3 left-3 bg-white/90 backdrop-blur-md text-xs font-semibold px-3 py-1 rounded-full text-[#57534E]">
                  {{ product.category_name }}
                </span>
              </div>

              <h3 class="text-lg font-bold mb-1 group-hover:text-[#E85D04] transition-colors">{{ product.name }}</h3>
              <p class="text-sm text-[#78716C] line-clamp-2 mb-4">{{ product.description }}</p>
            </div>

            <div class="flex items-center justify-between pt-4 border-t border-[#F5F2EC]">
              <div>
                <span class="text-xs text-[#A8A29E] block">Цена</span>
                <span class="text-xl font-extrabold text-[#1C1917]">{{ product.price }} ₽</span>
              </div>
              <button 
                @click="addToCart(product.id)"
                class="bg-[#F5F2EC] hover:bg-[#E85D04] hover:text-white text-[#1C1917] p-3 rounded-2xl font-medium transition-all active:scale-95 flex items-center justify-center"
              >
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/></svg>
              </button>
            </div>
          </div>
        </div>

      </div>

      <div v-if="activeTab === 'orders'" class="max-w-2xl mx-auto">
        <h2 class="text-2xl font-bold mb-6">История заказов</h2>
        
        <div v-if="orders.length === 0" class="text-center py-16 bg-white rounded-3xl border border-[#E7E5E4]">
          <p class="text-[#78716C] mb-4">У вас пока нет заказов</p>
          <button @click="activeTab = 'catalog'" class="bg-[#E85D04] text-white px-6 py-3 rounded-full font-medium">Перейти к меню</button>
        </div>

        <div class="space-y-4">
          <div v-for="order in orders" :key="order.id" class="bg-white rounded-3xl p-6 border border-[#E7E5E4] shadow-sm">
            <div class="flex items-center justify-between mb-4 pb-4 border-b border-[#F5F2EC]">
              <div>
                <span class="text-sm font-bold text-[#1C1917]">Заказ №{{ order.id }}</span>
                <span class="text-xs text-[#A8A29E] block">{{ new Date(order.created_at).toLocaleString() }}</span>
              </div>
              <span class="px-3 py-1 rounded-full text-xs font-semibold" :class="getStatusBadge(order.status).class">
                {{ getStatusBadge(order.status).text }}
              </span>
            </div>

            <div class="space-y-2 mb-4">
              <div v-for="item in order.items" :key="item.id" class="flex justify-between text-sm">
                <span class="text-[#78716C]">{{ item.product_name }} × {{ item.quantity }}</span>
                <span class="font-medium">{{ item.price * item.quantity }} ₽</span>
              </div>
            </div>

            <div class="flex items-center justify-between pt-4 border-t border-[#F5F2EC] text-sm">
              <span class="text-[#78716C]">Адрес: <strong class="text-[#1C1917]">{{ order.address }}</strong></span>
              <span class="text-base font-extrabold text-[#E85D04]">Итого: {{ order.total_price }} ₽</span>
            </div>
          </div>
        </div>
      </div>

    </main>

    <div v-if="isCartOpen" class="fixed inset-0 z-50 flex justify-end">
      <div class="absolute inset-0 bg-black/40 backdrop-blur-sm transition-opacity" @click="isCartOpen = false"></div>

      <div class="relative w-full max-w-md bg-white h-full shadow-2xl flex flex-col justify-between p-6 z-10">
        <div>
          <div class="flex items-center justify-between pb-4 border-b border-[#E7E5E4] mb-6">
            <h2 class="text-xl font-bold">Ваша корзина</h2>
            <button @click="isCartOpen = false" class="p-2 text-[#78716C] hover:text-[#1C1917]">
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/></svg>
            </button>
          </div>

          <div v-if="cart && cart.items && cart.items.length > 0" class="space-y-4 max-h-[45vh] overflow-y-auto pr-2">
            <div v-for="item in cart.items" :key="item.id" class="flex items-center justify-between bg-[#FDFBF7] p-4 rounded-2xl border border-[#E7E5E4]">
              <div>
                <h4 class="font-bold text-sm">{{ item.product_name }}</h4>
                <span class="text-xs text-[#78716C]">{{ item.quantity }} шт. × {{ item.product_price }} ₽</span>
              </div>
              <div class="flex items-center gap-3">
                <span class="font-extrabold text-sm">{{ item.product_price * item.quantity }} ₽</span>
                <button @click="removeFromCart(item.id)" class="text-[#A8A29E] hover:text-red-500 transition-colors">
                  <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/></svg>
                </button>
              </div>
            </div>
          </div>
          <div v-else class="text-center py-12 text-[#78716C]">
            Корзина пока пуста 🍕
          </div>
        </div>

        <div v-if="cart && cart.items && cart.items.length > 0" class="pt-6 border-t border-[#E7E5E4]">
          <div class="space-y-3 mb-4">
            <input 
              v-model="orderAddress" 
              type="text" 
              placeholder="Адрес доставки (ул. Пушкина, д. 10)" 
              class="w-full px-4 py-3 rounded-2xl border border-[#E7E5E4] focus:outline-none focus:border-[#E85D04] text-sm bg-[#FDFBF7]"
            >
            <input 
              v-model="orderComment" 
              type="text" 
              placeholder="Комментарий к заказу" 
              class="w-full px-4 py-3 rounded-2xl border border-[#E7E5E4] focus:outline-none focus:border-[#E85D04] text-sm bg-[#FDFBF7]"
            >
          </div>

          <div class="flex items-center justify-between mb-4">
            <span class="text-[#78716C]">Итого к оплате:</span>
            <span class="text-2xl font-extrabold text-[#1C1917]">{{ cartTotalPrice }} ₽</span>
          </div>

          <button 
            @click="checkout"
            class="w-full bg-[#E85D04] hover:bg-[#D45403] text-white py-4 rounded-2xl font-bold shadow-lg shadow-[#E85D04]/20 transition-all active:scale-98"
          >
            Оформить заказ
          </button>
        </div>

      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import api from './services/api'

const activeTab = ref('catalog')
const categories = ref([])
const products = ref([])
const cart = ref(null)
const orders = ref([])
const selectedCategory = ref(null)
const isCartOpen = ref(false)

const orderAddress = ref('')
const orderComment = ref('')

const loadData = async () => {
  try {
    const [catRes, prodRes, cartRes] = await Promise.all([
      api.getCategories(),
      api.getProducts(),
      api.getCart().catch(() => ({ data: null }))
    ])
    categories.value = catRes.data
    products.value = prodRes.data
    cart.value = cartRes.data && cartRes.data.length > 0 ? cartRes.data[0] : { items: [] }
  } catch (e) {
    console.error('Ошибка загрузки данных:', e)
  }
}

const loadOrders = async () => {
  try {
    const res = await api.getOrders()
    orders.value = res.data
  } catch (e) {
    console.error('Ошибка загрузки заказов:', e)
  }
}

const filteredProducts = computed(() => {
  if (selectedCategory.value === null) return products.value
  return products.value.filter(p => p.category === selectedCategory.value)
})

const cartTotalCount = computed(() => {
  if (!cart.value || !cart.value.items) return 0
  return cart.value.items.reduce((sum, item) => sum + item.quantity, 0)
})

const cartTotalPrice = computed(() => {
  if (!cart.value || !cart.value.items) return 0
  return cart.value.items.reduce((sum, item) => sum + (item.product_price * item.quantity), 0)
})

const addToCart = async (productId) => {
  try {
    await api.addToCart(productId, 1)
    const cartRes = await api.getCart()
    cart.value = cartRes.data && cartRes.data.length > 0 ? cartRes.data[0] : { items: [] }
    isCartOpen.value = true
  } catch (e) {
    alert('Ошибка! Убедитесь, что вы авторизованы в админке Django (http://127.0.0.1:8000/admin/)')
  }
}

const removeFromCart = async (itemId) => {
  try {
    await api.removeFromCart(itemId)
    const cartRes = await api.getCart()
    cart.value = cartRes.data && cartRes.data.length > 0 ? cartRes.data[0] : { items: [] }
  } catch (e) {
    console.error('Ошибка удаления товара:', e)
  }
}

const checkout = async () => {
  if (!orderAddress.value.trim()) {
    alert('Пожалуйста, укажите адрес доставки!')
    return
  }
  try {
    await api.createOrder(orderAddress.value, orderComment.value)
    alert('Заказ успешно оформлен!')
    orderAddress.value = ''
    orderComment.value = ''
    isCartOpen.value = false
    cart.value = { items: [] }
    loadOrders()
    activeTab.value = 'orders'
  } catch (e) {
    alert('Ошибка при оформлении заказа: ' + (e.response?.data?.error || 'Проверьте данные'))
  }
}

const getStatusBadge = (status) => {
  switch(status) {
    case 'new': return { text: 'Новый', class: 'bg-amber-100 text-amber-700' }
    case 'cooking': return { text: 'Готовится 🍕', class: 'bg-blue-100 text-blue-700' }
    case 'delivering': return { text: 'В доставке 🚗', class: 'bg-purple-100 text-purple-700' }
    case 'done': return { text: 'Выполнен ✨', class: 'bg-emerald-100 text-emerald-700' }
    default: return { text: status, class: 'bg-gray-100 text-gray-700' }
  }
}

onMounted(() => {
  loadData()
})
</script>