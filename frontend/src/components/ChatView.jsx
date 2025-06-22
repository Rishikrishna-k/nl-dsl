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
      <div className="message-avatar">
        {message.role === 'user' ? '👤' : '🤖'}
      </div>
      <div className="message-content">
        <div className="message-text">{message.content}</div>
        <div className="message-time">
          {new Date(message.created_at).toLocaleTimeString()}
        </div>
      </div>
    </div>
  );

  if (!chat) {
    return (
      <div className="chat-view">
        <div className="chat-header">
          <h2>New Chat</h2>
        </div>
        <div className="chat-body">
          <div className="new-chat-welcome">
            <div className='new-chat-in-test'>
              <h3>Start a new conversation</h3>
              <p>Ask me anything and I'll help you out!</p>
            </div>
            <div className="action-buttons">
              <button>Add files</button>
              <button>Add instructions</button>
            </div>
          </div>
        </div>
        <div className="chat-input">
          <input
            type="text"
            placeholder="Ask anything"
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            onKeyPress={handleKeyPress}
            disabled
          />
          <button disabled>{'➤'}</button>
        </div>
      </div>
    );
  }

  return (
    <div className="chat-view">
      <div className="chat-header">
        <h2>{chat.name || 'Chat'}</h2>
        {error && <div className="error-message">Error: {error}</div>}
      </div>
      <div className="chat-body">
        {loading === 'loading' ? (
          <div className="loading-messages">Loading messages...</div>
        ) : messages.length === 0 ? (
          <div className="new-chat-welcome">
            <div className='new-chat-in-test'>
              <h3>Start a new conversation</h3>
              <p>Ask me anything and I'll help you out!</p>
            </div>
            <div className="action-buttons">
              <button>Add files</button>
              <button>Add instructions</button>
            </div>
          </div>
        ) : (
          <div className="messages-container">
            {messages.map(renderMessage)}
            <div ref={messagesEndRef} />
          </div>
        )}
      </div>
      <div className="chat-input">
        <input
          type="text"
          placeholder="Ask anything"
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          onKeyPress={handleKeyPress}
          disabled={isSending || loading === 'loading'}
        />
        <button onClick={handleSendMessage} disabled={isSending || loading === 'loading' || !inputValue.trim()}>
          {isSending ? '⏳' : '➤'}
        </button>
      </div>
    </div>
  );
};

export default ChatView; 