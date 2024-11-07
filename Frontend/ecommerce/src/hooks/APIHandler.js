import { useState } from "react";
import axios from 'axios';

function useApi() {
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const callApi = async ({ url, method = "GET", body = {}, header = {} }) => {
    // console.log("data come to api handler: ", url, method, body, header);
    setLoading(true);
    let response = null;
    try {
      response = await axios.request({ url: url, method: method, data: body, headers: header });
      // console.log("async response:", response);
    } catch (err) {
      // Capture the error message from Django
      if (err.response && err.response.data) {
        setError(err.response.data.error); // Customize this based on the Django response structure
      } else {
        setError("An error occurred. Please try again.");
      }
    }
    setLoading(false);
    return response;
  };

  return { callApi, error, loading };
}

export default useApi;
