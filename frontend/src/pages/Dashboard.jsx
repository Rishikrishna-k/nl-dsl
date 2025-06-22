import React, { useState, useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { logout } from '../slices/authSlice';
import { fetchChats, createChat, setCurrentChat } from '../slices/chatsSlice';
import { useNavigate } from 'react-router-dom';
import ChatView from '../components/ChatView';
import Sidebar from '../components/Sidebar';
import './Dashboard.css';

const Dashboard = () => {
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const { items: chats, currentChat, status: chatsStatus } = useSelector((state) => state.chats);
  const [isSidebarOpen, setSidebarOpen] = useState(true);

  useEffect(() => {
    dispatch(fetchChats());
  }, [dispatch]);

  const handleLogout = () => {
    dispatch(logout());
    navigate('/login');
  };

  const handleNewChat = () => {
    dispatch(createChat({ name: 'New Chat' }));
  };

  const handleChatSelect = (chat) => {
    dispatch(setCurrentChat(chat));
  };

  return (
    <div className="dashboard-container">
      <Sidebar 
        isOpen={isSidebarOpen}
        toggleSidebar={() => setSidebarOpen(!isSidebarOpen)}
        chats={chats}
        currentChatId={currentChat?.id}
        onNewChat={handleNewChat}
        onChatSelect={handleChatSelect}
        onLogout={handleLogout}
      />
      <main className="chat-main">
        <ChatView chat={currentChat} />
      </main>
    </div>
  );
};

export default Dashboard; 