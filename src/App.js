import React, { useState, useEffect, useRef } from 'react';
import './App.css';
import ReactMarkdown from 'react-markdown';
import Webcam from 'react-webcam';

function App() {
  const [chatHistory, setChatHistory] = useState([]);
  const chatWindowRef = useRef(null);
  const [result, setResult] = useState(null);
  const webcamRef = useRef(null);
  console.log(webcamRef.current);

  const captureAndAnalyze = async () => {
    if (!webcamRef.current) {
      console.error("Webcam not available or not initialized.");
      return;
    }
  
    const imageSrc = webcamRef.current.getScreenshot();
    if (!imageSrc) {
      console.error("Failed to capture image.");
      return;
    }
  
    await sendImageToBackend(imageSrc);
  };
  

  const sendImageToBackend = async (imageSrc) => {
    try {
      const response = await fetch('http://127.0.0.1:5000/predict', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ image: imageSrc }),
      });
      if (response.ok) {
        const data = await response.json();
        setResult(data.result);
      } else {
        console.error('Error:', response.statusText);
      }
    } catch (error) {
      console.error('Error sending image to backend:', error);
    }
  };

  const handleKeyPress = async (event) => {
    if (event.key === 'Enter' && event.target.value.trim()) {
      const inputValue = event.target.value;
      event.target.value = '';

      const newChatHistory = [...chatHistory, { sender: 'user', message: inputValue }];
      setChatHistory(newChatHistory);

      await sendDataToBackend(inputValue, newChatHistory);
    }
  };

  const sendDataToBackend = async (inputValue, updatedChatHistory) => {
    try {
      const response = await fetch('http://127.0.0.1:5000/process', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text: inputValue }),
      });

      if (response.ok) {
        const data = await response.json();
        const newChatHistory = [...updatedChatHistory, { sender: 'bot', message: data.result }];
        setChatHistory(newChatHistory);
      } else {
        console.error('Error: ', response.statusText);
      }
    } catch (error) {
      console.error('Error sending data to backend:', error);
    }
  };

  useEffect(() => {
    if (chatWindowRef.current) {
      chatWindowRef.current.scrollTop = chatWindowRef.current.scrollHeight;
    }
  }, [chatHistory]);

  return (
    <div className="container">
      <div className="leftPane">
        <Webcam
          className="webcam"
          screenshotFormat="image/jpeg"
          width={320}
          height={240}
          ref={webcamRef}
        />
        <button onClick={captureAndAnalyze}>Analyze Skin</button>
        {result && <p>Prediction: {result}</p>}
      </div>
      <div className="chat-container">
        <div className="chat-window" ref={chatWindowRef}>
          {chatHistory.map((chat, index) => (
            <div
              key={index}
              className={chat.sender === 'user' ? 'user-message' : 'bot-message'}
            >
              {chat.sender === 'bot' ? (
                <ReactMarkdown>{chat.message}</ReactMarkdown>
              ) : (
                <p>{chat.message}</p>
              )}
            </div>
          ))}
        </div>
        <div className="input-container">
          <input
            type="text"
            onKeyDown={handleKeyPress}
            placeholder="Send a message..."
            className="input-box"
          />
        </div>
      </div>
    </div>
  );
}

export default App;
