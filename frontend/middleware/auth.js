export default defineNuxtRouteMiddleware((to, from) => {
  console.debug("middleware auth.js");
  const cookies = useCookie();
  const isAuth = cookies.get('is_auth');

  const nuxtApp = useNuxtApp();
  
  nuxtApp.provide('isAuthenticated', true);
  // if (isAuth) {
  //   nuxtApp.provide('isAuthenticated', true); // 用戶已登入
  // } else {
  //   nuxtApp.provide('isAuthenticated', false); // 用戶未登入
  // }
});
