import React from 'react';
import { getUser } from '../utils/Helper';

const Home=()=>{
    return <h1>home, Hi {getUser().username}</h1>
}
export default Home;