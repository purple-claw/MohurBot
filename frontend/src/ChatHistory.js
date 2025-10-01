import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './ChatHistory.css';

const ChatHistory = ({ isVisible, onClose, onSelectMessage, onHistoryCleared }) => {
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(false);
  const [stats, setStats] = useState(null);
  const [showSuccessMessage, setShowSuccessMessage] = useState(false);

  useEffect(() => {
    if (isVisible) {
      loadHistory();
      loadStats();
    }
  }, [isVisible]);

  const loadHistory = async () => {
    setLoading(true);
    try {
      const response = await axios.get('/api/history');
      setHistory(response.data.history || []);
    } catch (err) {
      console.error('Error loading history:', err);
    } finally {
      setLoading(false);
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

  const clearHistory = async () => {
    if (window.confirm('Are you sure you want to clear all chat history? This action cannot be undone.')) {
      try {
        setLoading(true);
        const response = await axios.delete('/api/history');
        
        if (response.data.status === 'success') {
          setHistory([]);
          setStats(null);
          console.log('Chat history cleared successfully..');
          
          // Call the parent callback to refresh main chat
          if (onHistoryCleared) {
            onHistoryCleared();
          }
          
          // Show success message
          setShowSuccessMessage(true);
          setTimeout(() => setShowSuccessMessage(false), 3000);
          
          // Reload stats to update the counts
          loadStats();
        }
      } catch (err) {
        console.error('Error clearing history:', err);
        alert('Failed to clear chat history. Please try again.');
      } finally {
        setLoading(false);
      }
    }
  };

  const formatTime = (timestamp) => {
    const date = new Date(timestamp);
    return date.toLocaleString();
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
        className="source-badge-small" 
        style={{ backgroundColor: badge.color }}
        title={badge.title}
      >
        {badge.text}
      </span>
    );
  };

  if (!isVisible) return null;

  return (
    <div className="chat-history-overlay">
      <div className="chat-history-modal">
        <div className="chat-history-header">
          <h2>Chat History</h2>
          <button className="close-button" onClick={onClose}>✕</button>
        </div>

        {stats && (
          <div className="history-stats">
            <div className="stat-box">
              <span className="stat-label">Total Conversations</span>
              <span className="stat-value">{stats.total_conversations}</span>
            </div>
            <div className="stat-box">
              <span className="stat-label">AI Enhanced</span>
              <span className="stat-value">{stats.llm_enhanced_responses}</span>
            </div>
            <div className="stat-box">
              <span className="stat-label">Knowledge Base</span>
              <span className="stat-value">{stats.knowledge_base_responses}</span>
            </div>
          </div>
        )}

        <div className="history-actions">
          <button className="refresh-button" onClick={loadHistory} disabled={loading}>
            Refresh
          </button>
          <button className="clear-button" onClick={clearHistory} disabled={loading}>
            {loading ? 'Clearing...' : 'Clear All'}
          </button>
        </div>

        {showSuccessMessage && (
          <div className="success-message">
            Chat history cleared successfully!
          </div>
        )}

        <div className="chat-history-content">
          {loading ? (
            <div className="loading-state">Loading history...</div>
          ) : history.length === 0 ? (
            <div className="empty-state">
              <p>No chat history yet</p>
              <p>Start a conversation to see your history here!</p>
            </div>
          ) : (
            <div className="history-list">
              {history.map((entry, idx) => (
                <div key={idx} className="history-item">
                  <div className="history-item-header">
                    <span className="history-timestamp">
                      {formatTime(entry.timestamp)}
                    </span>
                    {getSourceBadge(entry.source)}
                  </div>
                  
                  <div className="history-question">
                    <strong>Q:</strong> {entry.question}
                  </div>
                  
                  <div className="history-answer">
                    <strong>A:</strong> {entry.answer.length > 150 
                      ? `${entry.answer.substring(0, 150)}...` 
                      : entry.answer}
                  </div>
                  
                  <div className="history-actions-row">
                    <button 
                      className="use-question-btn"
                      onClick={() => onSelectMessage && onSelectMessage(entry.question)}
                    >
                      Use Question
                    </button>
                    <button 
                      className="view-full-btn"
                      onClick={() => onSelectMessage && onSelectMessage(entry.question)}
                    >
                      View Full
                    </button>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default ChatHistory;