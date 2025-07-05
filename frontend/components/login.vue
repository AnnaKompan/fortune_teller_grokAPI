<template>
  <div class="login-wrapper">
    <div class="login-box">
      <h2>Login to test your fortune</h2>
      <button class="google-btn" @click="loginWithGoogle">
        <img class="google-logo" src="https://www.gstatic.com/firebasejs/ui/2.0.0/images/auth/google.svg" alt="Google logo" />
        <span>Login with Google</span>
      </button>
    </div>
  </div>
</template>

<script setup>
  const emit = defineEmits(['trigger-check']);
  const loginWithGoogle = async () => {
    const { data, error } = await useFetch('/api/login')
    if(data.value )console.log(data.value)
    if(error.value) console.log(error.value)
    emit('trigger-check', { isAuthenticated: true })
  }

</script>

<style scoped>
.login-wrapper {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  /* background: #f1f1f1; */
}

.login-box {
  background: #fff;
  padding: 2rem;
  border-radius: 12px;
  box-shadow: 0 0 15px rgba(0, 0, 0, 0.1);
  text-align: center;
  width: 25vw;
  /* height: 25vh; */
}

.google-btn {
  margin: 0 auto;
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 12px 25px;
  font-size: 16px;
  background: #ffffff;
  color: #aaaaaa;
  border: 1px solid #e4e3e3;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease-in-out;
  /* box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1); */
}

.google-btn:hover {
  background: #dcdcdc;
  /* box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15); */
}

.google-logo {
  width: 20px;
  height: 20px;
}

span {
  font-weight: bold;
}
</style>
