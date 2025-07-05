// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  ssr: true,
  // axios: {
  //   // put axios url here
  // },
  devtools: { enabled: true },
  // 使用 JavaScript
  typescript: {
    strict: false,
    shim: false
  },
  runtimeConfig: {
    public: {
      googleClientId: process.env.GOOGLE_CLIENT_ID,
      apiBaseUrl: process.env.NUXT_PUBLIC_API_URL
    },
    googleClientSecret: process.env.GOOGLE_CLIENT_SECRET,
    googleRedirectUri: process.env.GOOGLE_REDIRECT_URI,
    gorkSessionSecret: process.env.SESSION_SECRET,
    }
  }
)
