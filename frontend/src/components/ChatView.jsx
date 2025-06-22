import React, { useState, useRef, useEffect } from 'react';
import ReactMarkdown from 'react-markdown';
import './ChatView.css';
import { useDispatch, useSelector } from 'react-redux';
import { addMessage, fetchMessagesForChat, clearMessages, formatAsCode } from '../slices/messagesSlice';
import CodeBlock from './CodeBlock';
import remarkGfm from 'remark-gfm';

const MessageActions = ({ message, onRegenerate }) => {
  const [isCopied, setIsCopied] = useState(false);
  const isCode = /```(\w+)?\n([\s\S]+)```$/.test(message.content);

  const handleCopy = () => {
    navigator.clipboard.writeText(message.content).then(() => {
      setIsCopied(true);
      setTimeout(() => setIsCopied(false), 2500);
    });
  };

  return (
    <div className="message-actions">
      {!isCode && (
        <button 
          onClick={() => onRegenerate(message.id)} 
          className="action-btn generate-btn"
          title="Generate in code editor"
        >
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M16 18L22 12L16 6" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/><path d="M8 6L2 12L8 18" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/></svg>
          <span>Code Editor</span>
        </button>
      )}
      {!isCode && (
        <button onClick={handleCopy} className="action-btn" title={isCopied ? "Copied!" : "Copy"}>
            {isCopied ? (
                <>
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M20 6L9 17L4 12" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/></svg>
                <span>Copied</span>
                </>
            ) : (
                <>
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M8 16H6C4.89543 16 4 15.1046 4 14V6C4 4.89543 4.89543 4 6 4H14C15.1046 4 16 4.89543 16 6V8M18 10H10C8.89543 10 8 10.8954 8 12V20C8 21.1046 8.89543 22 10 22H18C19.1046 22 20 21.1046 20 20V12C20 10.8954 19.1046 10 18 10Z" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/></svg>
                <span>Copy</span>
                </>
            )}
        </button>
      )}
    </div>
  );
};

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

    const content = inputValue.trim();
    setInputValue('');
    setIsSending(true);

    try {
      await dispatch(addMessage({ chatId: chat.id, content })).unwrap();
    } catch (err) {
      console.error('[ChatView] Failed to send message:', err);
      setInputValue(content);
    } finally {
      setIsSending(false);
    }
  };

  const handleFormatAsCode = (messageId) => {
    dispatch(formatAsCode({ messageId }));
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  const renderMessage = (message, index) => {
    const codeBlockRegex = /```(\w*)\n([\s\S]+?)\n```/;
    const match = message.content.match(codeBlockRegex);
    const isCode = !!match;
    const language = isCode ? match[1] || 'text' : null;
    const code = isCode ? match[2] : null;

    const wrapperClass = `message-wrapper ${message.role} ${isCode && message.role === 'assistant' ? 'assistant-code' : ''}`;

    return (
      <div key={message.id || index} className={wrapperClass}>
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
          <div className="message-content-wrapper">
            {message.role === 'assistant' && (
              <MessageActions message={message} onRegenerate={handleFormatAsCode} />
            )}
            <div className="message-content">
              {isCode ? (
                <CodeBlock language={language} code={code} />
              ) : (
                <ReactMarkdown remarkPlugins={[remarkGfm]}>
                  {message.content}
                </ReactMarkdown>
              )}
            </div>
          </div>
        </div>
      </div>
    );
  };

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
            {messages.map((message, index) => renderMessage(message, index))}
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