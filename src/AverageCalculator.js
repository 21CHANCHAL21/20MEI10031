import React, { useState } from 'react';
import axios from 'axios';

const API_BASE_URL = 'http://localhost:9876';


function AverageCalculator() {
  const [windowPrevState, setWindowPrevState] = useState([]);
  const [windowCurrState, setWindowCurrState] = useState([]);
  const [numbers, setNumbers] = useState([]);
  const [avg, setAvg] = useState(0);

  const handleNumberRequest = async (numberType) => {
    try {
      const response = await axios.get(`${API_BASE_URL}/numbers/${numberType}`);
      const responseData = response.data;
      setWindowPrevState(responseData.windowPrevState);
      setWindowCurrState(responseData.windowCurrState);
      setNumbers(responseData.numbers);
      setAvg(responseData.avg);
    } catch (error) {
      console.error('Error fetching data:', error);
    }
  };

  return (
    <div>
      <h1>Average Calculator</h1>
      <button onClick={() => handleNumberRequest('p')}>Fetch Prime Numbers</button>
      <button onClick={() => handleNumberRequest('f')}>Fetch Fibonacci Numbers</button>
      <button onClick={() => handleNumberRequest('e')}>Fetch Even Numbers</button>
      <button onClick={() => handleNumberRequest('r')}>Fetch Random Numbers</button>
      <div>
        <h2>Previous Window State: {JSON.stringify(windowPrevState)}</h2>
        <h2>Current Window State: {JSON.stringify(windowCurrState)}</h2>
        <h2>Numbers: {JSON.stringify(numbers)}</h2>
        <h2>Average: {avg}</h2>
      </div>
    </div>
  );
}

export default AverageCalculator;

