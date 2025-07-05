<template>
  <div>
    <div>
      <NuxtPage />
      <button class="logout-btn" @click="logout">Logout</button>
    </div>

    <div v-if="!isLoggedIn" class="overlay">
      <LoginComponent @trigger-check="checkAuthStatus"/>
    </div>
  </div>
</template>

<script setup>
  import LoginComponent from './components/login.vue'
  import { ref, onMounted } from 'vue'

  let isLoggedIn = ref(false)
  const { data, error } = await useFetch('/api/checklogin')

  const checkAuthStatus = async (response) => {
    isLoggedIn.value = response?.isAuthenticated === true
  }

  const logout = async () => {
    const { data } = useFetch('/api/logout');
    console.log('User logged out');
    isLoggedIn.value = false
  };

  onMounted(() => {
    checkAuthStatus()
  })

</script>

<style scoped>
  .overlay {
    position: fixed;        /* 固定在畫面上 */
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.5); /* 半透明的黑色背景 */
    display: flex;          /* 使用 flex 排列，方便居中 */
    justify-content: center; /* 水平居中 */
    align-items: center;    /* 垂直居中 */
    z-index: 9999;
    backdrop-filter: blur(10px);
  }

  .logout-btn {
    position: absolute;
    top: 10px;
    right: 10px;
    background-color: #6a1b9a;
    color: white;
    border: none;
    padding: 8px 12px;
    border-radius: 8px;
    font-size: 0.9em;
    cursor: pointer;
    transition: background-color 0.3s;
  }
  .logout-btn:hover {
    background-color: #4a148c; 
  }
</style>