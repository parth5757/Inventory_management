import React from 'react';
import { getUser } from '../utils/Helper';

const Home=()=>{
    return (
        <>
            <h1>home, Hi {getUser().username}</h1>
            <h2>Id = {getUser().user_id}</h2>
        </>
    );
}
export default Home;