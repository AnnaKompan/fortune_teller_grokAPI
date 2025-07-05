import axios from "axios";

export default defineEventHandler(async (event) => {
  const config = useRuntimeConfig()
  try {    
    // return {isAuthenticated: true, token: "fake token"}
    const response = await axios.get(`${config.public.apiBaseUrl}/me`);
    console.log("Response:", response.data);
    return response.data;

  } catch (error) {
    if (axios.isAxiosError(error) && error.response) {
      const statusCode = error.response.status;
      const backendMessage = error.response.data?.message || "Unknown backend error";

      console.error("Checklogin Axios error:", backendMessage);

      throw createError({
        statusCode,
        statusMessage: 'Backend Error',
        message: backendMessage,
      });
    } else {
      console.error("Checklogin error:", error || error);
      throw createError({
        statusCode: 500,
        statusMessage: 'Internal Server Error',
        message: "Unexpected error occurred.",
      });
    }
  }
})
