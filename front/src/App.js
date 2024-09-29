import React, { useState, useEffect, useRef } from 'react';
import './App.css'; // Import the CSS file
import ReactMarkdown from 'react-markdown';
import Webcam from 'react-webcam';

function App() {
  const [chatHistory, setChatHistory] = useState([]); // Store chat history
  const chatWindowRef = useRef(null);
  const [webcamResult, setWebcamResult] = useState(null); // State for webcam analysis result
  const [selectedFile, setSelectedFile] = useState(null); // State to store selected file
  const [fileResult, setFileResult] = useState(null); // Store file upload result
  const [isAnalyzing, setIsAnalyzing] = useState(false); // State to manage analysis button
  const webcamRef = useRef(null); // Ref for webcam

  // Handle file selection
  const handleFileChange = (event) => {
    const file = event.target.files[0];
    if (file && file.size > 5 * 1024 * 1024) { // 5MB size limit
      alert('File is too large. Please upload a file smaller than 5MB.');
      return;
    }
    if (file) {
      setSelectedFile(file);
    }
  };

  // Handle file upload and submit
  const handleFileUpload = async () => {
    if (!selectedFile) {
      alert('Please select a file first.');
      return;
    }

    const formData = new FormData();
    formData.append('file', selectedFile);

    try {
      const response = await fetch('http://127.0.0.1:5000/upload', {
        method: 'POST',
        body: formData,  // Send the form data containing the file
      });
      if (response.ok) {
        const data = await response.json();
        setFileResult(data.result); // Handle backend response (if any)
        setSelectedFile(null); // Clear file after successful upload
      } else {
        console.error('Error:', response.statusText);
      }
    } catch (error) {
      console.error('Error uploading file:', error);
    }
  };

  // Capture and analyze image from webcam
  const captureAndAnalyze = async () => {
    if (isAnalyzing) return; // Prevent multiple clicks
    setIsAnalyzing(true);

    if (!webcamRef.current) {
      console.error("Webcam not available or not initialized.");
      setIsAnalyzing(false);
      return;
    }

    const imageSrc = webcamRef.current.getScreenshot();
    if (!imageSrc) {
      console.error("Failed to capture image.");
      setIsAnalyzing(false);
      return;
    }

    await sendImageToBackend(imageSrc);
    setIsAnalyzing(false);
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
        setWebcamResult(data.result);
      } else {
        console.error('Error:', response.statusText);
      }
    } catch (error) {
      console.error('Error sending image to backend:', error);
    }
  };

  // Handle text input submission in chat
  const handleKeyPress = async (event) => {
    if (event.key === 'Enter' && event.target.value.trim()) {
      const inputValue = event.target.value;

      event.target.value = ''; // Clear the input field

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

  // Auto-scroll chat to the bottom
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
        <button onClick={captureAndAnalyze} disabled={isAnalyzing}>
          {isAnalyzing ? "Analyzing..." : "Analyze Skin"}
        </button>
        {webcamResult && <p>Webcam Analysis Result: {webcamResult}</p>}
        
        <div>
          <h2>Upload a file for analysis</h2>
          <input type="file" onChange={handleFileChange} />
          <button onClick={handleFileUpload}>Upload File</button>
          {fileResult && <p>File Analysis Result: {fileResult}</p>}
        </div>
      </div>

      <div className="chat-container">
        <div className="chat-window" ref={chatWindowRef}>
          {chatHistory.map((chat, index) => (
            <div key={index} className={chat.sender === 'user' ? 'user-message' : 'bot-message'}>
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
