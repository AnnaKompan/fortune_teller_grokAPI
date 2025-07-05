import axios from "axios";

const config = useRuntimeConfig()

export default defineEventHandler(async (event) => {
  try {
    const url = config.public.apiBaseUrl + "/logout";
    
    const response = await axios.get(url);
    return response.data;

  } catch (error) {
    if (axios.isAxiosError(error) && error.response) {
      const statusCode = error.response.status;
      const backendMessage = error.response.data?.message || "Unknown backend error";

      console.error("Logout Axios error:", backendMessage);

      throw createError({
        statusCode,
        statusMessage: 'Backend Error',
        message: backendMessage,
      });
    } else {
      console.error("Logout error:", error.message || error);
      throw createError({
        statusCode: 500,
        statusMessage: 'Internal Server Error',
        message: "Unexpected error occurred.",
      });
    }
  }
})
