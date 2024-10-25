import { useState } from "react";
import axios from 'axios';

function useApi(){
    const [error, setError] = useState("");
    const[loading, setLoading] = useState(false);
    const callApi=async({url, method="GET", body={}, header={}})=>{
        console.log("data come to api handler: ",url, method, body, header)
        setLoading(true);
        let response=null;
        try{
            console.log("async started")
            console.log(url, method, body, header)
            response = await axios.request({url:url, method:method, data:body, headers:header})
            console.log("async response:", response)
        }
        catch(err){
            console.log("async error")
            setError(err)
        }
        setLoading(false);
        return response;
    }
    return {callApi, error, loading}
}

export default useApi;