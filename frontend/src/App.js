import logo from './logo.svg';
import './App.css';
import React, { useState, useEffect } from "react";

function App() {

  const [currentTime, setCurrentTime] = useState(0);
  useEffect(() => {
    fetch('/api/time').then(res => res.text()).then(data => {
      setCurrentTime(data.time);
    });
  }, []);

  const [data, setData] = useState(0);
  useEffect(() => {
    // Fetch data from the Flask API
    fetch('/api/data')
      .then(response => response.json())
      .then(data => {setData(data.message)})
      .catch(error => console.error('Error fetching data:', error));
  }, []);

  return (
    <div className="App">
      <header className="App-header">
        {/* <img src={logo} className="App-logo" alt="logo" /> */}

        <img src={'https://pngimg.com/d/credit_card_PNG204.png'} className="App-logo" alt="logo" />

        <p>Summary:</p>
        <p className="display-linebreak" >{data}</p>

      </header>
    </div>
  );
}

export default App;
