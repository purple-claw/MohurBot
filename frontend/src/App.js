import React from 'react';
import ChatInterface from './ChatInterface';
import './App.css';

function App() {
  return (
    <div className="App">
      <main className="app-main">
        <ChatInterface />
      </main>
      <footer className="app-footer">
        <p>Mohur AI Assistant v2.0 - • Built with React & FastAPI With Love by NitinSri</p>
      </footer>
    </div>
  );
}

export default App;
