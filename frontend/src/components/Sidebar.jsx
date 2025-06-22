import React from 'react';
import './Sidebar.css';
import { useSelector, useDispatch } from 'react-redux';
import { useNavigate } from 'react-router-dom';
import { logout } from '../slices/authSlice';

const Sidebar = ({ 
  isOpen, 
  toggleSidebar, 
  chats = [], 
  currentChatId, 
  onChatSelect, 
  onNewChat 
}) => {
  const projects = [
    { name: 'finetuning' },
    { name: 'dsl generator' },
    { name: 'rag project google notebo...' },
    { name: 'mcp' },
    { name: 'backnd' },
  ];

  const dispatch = useDispatch();
  const navigate = useNavigate();
  const auth = useSelector((state) => state.auth);

  const handleLogout = () => {
    dispatch(logout());
    navigate('/login');
  };

  const handleNewChat = () => {
    if (onNewChat) {
      onNewChat();
    }
  };

  const handleChatSelect = (chatId) => {
    if (onChatSelect) {
      onChatSelect(chatId);
    }
  };

  const getChatPreview = (chat) => {
    if (chat.messages && chat.messages.length > 0) {
      const lastMessage = chat.messages[chat.messages.length - 1];
      return lastMessage.content.length > 50 
        ? lastMessage.content.substring(0, 50) + '...' 
        : lastMessage.content;
    }
    return 'No messages yet';
  };

  return (
    <div className={`sidebar ${isOpen ? 'open' : 'closed'}`}>
      <button className="close-btn" onClick={toggleSidebar}>
        &times;
      </button>
      <div className="sidebar-header">
        <button className="new-chat-btn" onClick={handleNewChat}>
          <span>+</span>
          <span>New chat</span>
        </button>
        <div className="search-library-buttons">
          <button>
            <span>🔍</span>
            <span>Search chats</span>
          </button>
          <button>
            <span>📚</span>
            <span>Library</span>
          </button>
        </div>
      </div>
      <div className="sidebar-content">
        <div className="projects-section">
          <div className="section-header">
            <button className="new-project-btn">New project</button>
          </div>
          <ul className="projects-list">
            {projects.map((project, index) => (
              <li key={index}>
                <span>📁</span> {project.name}
              </li>
            ))}
          </ul>
        </div>
        <div className="chats-section">
           <div className="section-header">
            <span>Chats</span>
          </div>
          <ul className="chats-list">
            {chats.map((chat) => (
              <li 
                key={chat.id} 
                className={currentChatId === chat.id ? 'active' : ''}
                onClick={() => handleChatSelect(chat.id)}
              >
                <div className="chat-item">
                  <div className="chat-name">{chat.name}</div>
                  <div className="chat-preview">{getChatPreview(chat)}</div>
                </div>
              </li>
            ))}
          </ul>
        </div>
      </div>
      <div className="sidebar-footer">
        {auth.user && (
          <div className="user-profile">
            <span className="user-email">{auth.user.email}</span>
            <button onClick={handleLogout} className="logout-btn">
              Logout
            </button>
          </div>
        )}
      </div>
    </div>
  );
};

export default Sidebar; 