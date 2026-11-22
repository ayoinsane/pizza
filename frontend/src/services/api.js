import axios from 'axios'

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

const API = axios.create({
  baseURL: 'http://localhost:8000/api/',
  withCredentials: true,
})

API.interceptors.request.use((config) => {
  if (config.method === 'post' || config.method === 'put' || config.method === 'delete') {
    const csrftoken = getCookie('csrftoken');
    if (csrftoken) {
      config.headers['X-CSRFToken'] = csrftoken;
    }
  }
  return config;
})

export default {
  getCategories() { return API.get('categories/') },
  getProducts() { return API.get('products/') },
  getCart() { return API.get('cart/') },
  addToCart(productId, quantity = 1) { return API.post('cart/add_item/', { product_id: productId, quantity }) },
  removeFromCart(itemId) { return API.post('cart/remove_item/', { item_id: itemId }) },
  getOrders() { return API.get('orders/') },
  createOrder(address, comment) { return API.post('orders/', { address, comment }) },
  login(username, password) { return API.post('auth/login/', { username, password }) },
  register(username, password) { return API.post('auth/register/', { username, password }) },
  logout() { return API.post('auth/logout/') },
  getUserInfo() { return API.get('auth/user/') }
}