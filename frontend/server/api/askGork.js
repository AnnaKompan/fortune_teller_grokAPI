import axios from "axios";

const config = useRuntimeConfig()

export default defineEventHandler(async (event) => {
  const { keywords } = await readBody(event);
  let returnMsg = "";
  // return {message: "test"}

  console.log("Keywords:", keywords);

  if (keywords.length !== 3) {
    returnMsg = "Please enter exactly 3 keywords.";
    throw createError({
      statusCode: 400,
      statusMessage: 'Bad Request',
      message: returnMsg,
    })
  }
  
  try {
    console.log("Sending request to backend...");
    const response = await axios.post(`${config.public.apiBaseUrl}/fortune`, {
      keywords: keywords,
    }, 
    {
      headers: {
        'Content-Type': 'application/json',
      },
    });

    const data = response.data;
    console.log("Response from backend:", data);

    switch (data.status) {
      case "success":
        returnMsg = data.fortune;
        break;
      case "limit_exceeded":
        returnMsg = "⚠️ You have asked for all your opportunities today.";
        throw createError({
          statusCode: 400,
          statusMessage: 'Bad Request',
          message: returnMsg,
        })
      case "grok_error":
        returnMsg = "⚠️ Today's fortune cannot be checked.";
        throw createError({
          statusCode: 400,
          statusMessage: 'Bad Request',
          message: returnMsg,
        })
      default:
        returnMsg = "⚠️ Unexpected server response.";
        throw createError({
          statusCode: 400,
          statusMessage: 'Bad Request',
          message: returnMsg,
        })
    }
  } catch (error) {
    if (axios.isAxiosError(error) && error.response) {
      const statusCode = error.response.status;
      const backendMessage = error.response.data?.message || "Unknown backend error";

      console.error("askGork Axios error:", error);

      throw createError({
        statusCode: statusCode,
        statusMessage: 'Backend Error',
        message: backendMessage,
      });
    } else {
      console.error("askGork error:", error || error);
      throw createError({
        statusCode: 500,
        statusMessage: 'Internal Server Error',
        message: error.message,
      });
    }
  }
  return {message: returnMsg}
})
