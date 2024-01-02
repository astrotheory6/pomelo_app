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
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Edit <code>src/App.js</code> and save to reload.
        </p>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>

        <p>Data from Python script: {data}</p>

      </header>
    </div>
  );
}

export default App;
