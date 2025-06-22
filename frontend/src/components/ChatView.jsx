import React, { useState, useRef, useEffect } from 'react';
import './ChatView.css';
import { useDispatch, useSelector } from 'react-redux';
import { addMessage, fetchMessagesForChat, clearMessages } from '../slices/messagesSlice';

const ChatView = ({ chat }) => {
  const dispatch = useDispatch();
  const [inputValue, setInputValue] = useState('');
  const [isSending, setIsSending] = useState(false);
  const messagesEndRef = useRef(null);
  
  const { items: messages, status: loading, error } = useSelector(state => state.messages);

  // Auto-scroll to bottom when messages change
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  // Fetch messages when chat changes
  useEffect(() => {
    if (chat && chat.id) {
      console.log(`[ChatView] Fetching messages for chat: ${chat.id}`);
      dispatch(fetchMessagesForChat(chat.id));
    } else {
      console.log(`[ChatView] Clearing messages - no chat selected`);
      dispatch(clearMessages());
    }
  }, [chat, dispatch]);

  const handleSendMessage = async () => {
    if (!inputValue.trim() || isSending || !chat || !chat.id) return;

    const userMessageContent = inputValue.trim();
    setInputValue('');
    setIsSending(true);

    try {
      console.log(`[ChatView] Sending message: ${userMessageContent}`);
      await dispatch(addMessage({
        chatId: chat.id,
        content: userMessageContent,
      })).unwrap();
      
      console.log(`[ChatView] Message sent successfully`);
      
    } catch (err) {
      console.error('[ChatView] Failed to send message:', err);
      setInputValue(userMessageContent);
    } finally {
      setIsSending(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  const renderMessage = (message) => (
    <div key={message.id} className={`message ${message.role}`}>
      <div className="message-container">
        {message.role === 'assistant' && (
          <div className="message-avatar">
            <div className="ai-avatar">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M12 2L2 7L12 12L22 7L12 2Z" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                <path d="M2 17L12 22L22 17" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                <path d="M2 12L12 17L22 12" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
              </svg>
            </div>
          </div>
        )}
        <div className="message-content">
          <div className="message-text">{message.content}</div>
        </div>
      </div>
    </div>
  );

  if (!chat) {
    return (
      <div className="chat-view">
        <div className="welcome-screen">
          <div className="welcome-content">
            <h1>How can I help you today?</h1>
            <div className="suggestion-grid">
              <button className="suggestion-card">
                <div className="suggestion-icon">💡</div>
                <div className="suggestion-text">Explain quantum computing</div>
              </button>
              <button className="suggestion-card">
                <div className="suggestion-icon">🎨</div>
                <div className="suggestion-text">Write a creative story</div>
              </button>
              <button className="suggestion-card">
                <div className="suggestion-icon">🔧</div>
                <div className="suggestion-text">Help with coding</div>
              </button>
              <button className="suggestion-card">
                <div className="suggestion-icon">📚</div>
                <div className="suggestion-text">Analyze a book</div>
              </button>
            </div>
          </div>
        </div>
        <div className="chat-input-container">
          <div className="chat-input-wrapper">
            <input
              type="text"
              placeholder="Message ChatGPT..."
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              onKeyPress={handleKeyPress}
              disabled
            />
            <button disabled className="send-button">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M22 2L11 13" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                <path d="M22 2L15 22L11 13L2 9L22 2Z" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
              </svg>
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="chat-view">
      <div className="messages-container">
        {loading === 'loading' ? (
          <div className="loading-messages">
            <div className="loading-spinner"></div>
            <span>Loading messages...</span>
          </div>
        ) : messages.length === 0 ? (
          <div className="welcome-screen">
            <div className="welcome-content">
              <h1>How can I help you today?</h1>
              <div className="suggestion-grid">
                <button className="suggestion-card">
                  <div className="suggestion-icon">💡</div>
                  <div className="suggestion-text">Explain quantum computing</div>
                </button>
                <button className="suggestion-card">
                  <div className="suggestion-icon">🎨</div>
                  <div className="suggestion-text">Write a creative story</div>
                </button>
                <button className="suggestion-card">
                  <div className="suggestion-icon">🔧</div>
                  <div className="suggestion-text">Help with coding</div>
                </button>
                <button className="suggestion-card">
                  <div className="suggestion-icon">📚</div>
                  <div className="suggestion-text">Analyze a book</div>
                </button>
              </div>
            </div>
          </div>
        ) : (
          <div className="messages-list">
            {messages.map(renderMessage)}
            <div ref={messagesEndRef} />
          </div>
        )}
      </div>
      
      <div className="chat-input-container">
        <div className="chat-input-wrapper">
          <input
            type="text"
            placeholder="Message ChatGPT..."
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            onKeyPress={handleKeyPress}
            disabled={isSending || loading === 'loading'}
          />
          <button 
            onClick={handleSendMessage} 
            disabled={isSending || loading === 'loading' || !inputValue.trim()}
            className="send-button"
          >
            {isSending ? (
              <div className="sending-spinner"></div>
            ) : (
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M22 2L11 13" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                <path d="M22 2L15 22L11 13L2 9L22 2Z" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
              </svg>
            )}
          </button>
        </div>
      </div>
    </div>
  );
};

export default ChatView; 