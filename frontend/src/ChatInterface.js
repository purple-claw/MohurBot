import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import ChatHistory from './ChatHistory';

const ChatInterface = () => {
  const [q, setQ] = useState('');
  const [chatHist, setChatHist] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [stats, setStats] = useState(null);
  const [showStats, setShowStats] = useState(false);
  const [showHistory, setShowHistory] = useState(false);
  const msgsEndRef = useRef(null);

  useEffect(() => {
    loadHist();
    checkBackendHealth();
  }, []);

  //Backend health check endpoint
  const checkBackendHealth = async () => {
    try {
      console.log('Checking backend health...');
      const response = await axios.get('/api/health');
      if (response.data.status === 'healthy') {
        console.log('Backend connected successfully:', response.data);
        
        // Test CORS as well
        const corsTest = await axios.get('/api/test-cors');
        console.log('CORS test successful:', corsTest.data);
      }
    } catch (err) {
      console.error('Backend connection failed:', err);
      setError('Backend connection failed. Please ensure the server is running.');
    }
  };

  useEffect(() => {
    scrollToBottom();
  }, [chatHist]);

  const scrollToBottom = () => {
    msgsEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  const loadHist = async () => {
    try {
      const response = await axios.get('/api/history');
      setChatHist(response.data.history || []);
    } catch (err) {
      console.error('Error loading history:', err);
    }
  };

  const loadStats = async () => {
    try {
      const response = await axios.get('/api/stats');
      setStats(response.data);
    } catch (err) {
      console.error('Error loading stats:', err);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!q.trim()) return;

    setLoading(true);
    setError('');

    try {
      console.log('Sending question to backend:', q.trim());
      
      const response = await axios.post('/api/ask', {
        question: q.trim()
      }, {
        headers: {
          'Content-Type': 'application/json',
        },
        timeout: 30000, // 30 second timeout
      });

      console.log('Received response:', response.data);

      if (response.data.status === 'success') {
        const newEntry = {
          question: response.data.question,
          answer: response.data.answer,
          timestamp: new Date().toISOString(),
          source: response.data.source || 'unknown'
        };

        setChatHist(prev => [...prev, newEntry]);
        setQ('');
        
        // Reload stats after new message
        loadStats();
      } else {
        setError(response.data.error || 'Unknown error occurred');
      }
    } catch (err) {
      console.error('Error sending request:', err);
      
      if (err.code === 'ECONNREFUSED') {
        setError('Cannot connect to server. Please ensure the backend is running on port 5000.');
      } else if (err.response?.status === 405) {
        setError('Server configuration error. CORS may not be properly configured.');
      } else if (err.response?.data?.detail) {
        setError(`Server error: ${err.response.data.detail}`);
      } else {
        setError('Failed to get response from server. Please try again.');
      }
    } finally {
      setLoading(false);
    }
  };

  const formatTime = (timestamp) => {
    return new Date(timestamp).toLocaleTimeString();
  };

  const getSourceBadge = (source) => {
    const badges = {
      'llm_with_kb': { text: 'AI+KB', color: '#FF8000', title: 'AI Enhanced with Knowledge Base' },
      'llm_only': { text: 'AI', color: '#FF6600', title: 'AI Generated Response' },
      'kb_fallback': { text: 'KB', color: '#FFB366', title: 'Knowledge Base Only' },
      'error_fallback': { text: 'ERR', color: '#f44336', title: 'Error Fallback' },
      'unknown': { text: 'STD', color: '#999999', title: 'Standard Response' }
    };
    
    const badge = badges[source] || badges.unknown;
    
    return (
      <span 
        className="source-badge" 
        style={{ backgroundColor: badge.color }}
        title={badge.title}
      >
        {badge.text}
      </span>
    );
  };

  const handleHistorySelect = (question) => {
    setQ(question);
    setShowHistory(false);
  };

  const handleHistoryCleared = () => {
    // Refresh the main chat history when it's cleared from the modal
    setChatHist([]);
    loadStats(); // Refresh stats as well
  };

  return (
    <div className="chat-container">
      <div className="chat-header">
        <h1>Meet the MohurBot</h1>
        <p>Personalised ChatBot with AI Powered Intelligence</p>
        <div className="header-actions">
          <button 
            className="stats-button"
            onClick={() => {
              setShowStats(!showStats);
              if (!showStats) loadStats();
            }}
          >
            Stats
          </button>
          <button 
            className="history-button"
            onClick={() => setShowHistory(true)}
          >
            History
          </button>
        </div>
        {showStats && stats && (
          <div className="stats-panel">
            <div className="stat-item">
              <span>Total Conversations:</span>
              <span>{stats.total_conversations}</span>
            </div>
            <div className="stat-item">
              <span>AI Enhanced:</span>
              <span>{stats.llm_enhanced_responses}</span>
            </div>
            <div className="stat-item">
              <span>Knowledge Base:</span>
              <span>{stats.knowledge_base_responses}</span>
            </div>
          </div>
        )}
      </div>

      <div className="chat-messages">
        {chatHist.map((entry, idx) => (
          <div key={idx} className="message-pair">
            <div className="user-message">
              <strong>You:</strong> {entry.question}
              <span className="timestamp">{formatTime(entry.timestamp)}</span>
            </div>
            <div className="bot-message">
              <div className="bot-message-header">
                <strong>Mohur:</strong>
                {getSourceBadge(entry.source)}
              </div>
              <div className="bot-message-content">{entry.answer}</div>
              <span className="timestamp">{formatTime(entry.timestamp)}</span>
            </div>
          </div>
        ))}
        {loading && (
          <div className="loading-message">
            <div className="typing-indicator">
              <span></span>
              <span></span>
              <span></span>
            </div>
            <p className="loading-text">Mohur is thinking with AI assistance...</p>
          </div>
        )}
        <div ref={msgsEndRef} />
      </div>

      {error && (
        <div className="error-message">
          {error}
        </div>
      )}

      <form onSubmit={handleSubmit} className="input-form">
        <input
          type="text"
          value={q}
          onChange={(e) => setQ(e.target.value)}
          placeholder="Ask about productivity, remote work, leadership, or professional development..."
          disabled={loading}
          maxLength={500}
        />
        <button type="submit" disabled={loading || !q.trim()}>
          {loading ? 'AI Working...' : 'Send'}
        </button>
      </form>

      <ChatHistory 
        isVisible={showHistory}
        onClose={() => setShowHistory(false)}
        onSelectMessage={handleHistorySelect}
        onHistoryCleared={handleHistoryCleared}
      />
    </div>
  );
};

export default ChatInterface;