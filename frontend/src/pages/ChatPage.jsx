import React, { useEffect, useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { fetchChats, createChat, setCurrentChat } from '../slices/chatsSlice';
import ChatView from '../components/ChatView';
import Sidebar from '../components/Sidebar';
import './Dashboard.css';

const ChatPage = () => {
  const dispatch = useDispatch();
  const { items: chats, currentChat, status: chatsStatus } = useSelector((state) => state.chats);
  const [isSidebarOpen, setSidebarOpen] = useState(true);

  useEffect(() => {
    console.log('[ChatPage] Fetching chats');
    dispatch(fetchChats());
  }, [dispatch]);

  const handleNewChat = () => {
    console.log('[ChatPage] Creating new chat');
    dispatch(createChat({ name: 'New Chat' }));
  };

  const handleChatSelect = (chat) => {
    console.log('[ChatPage] Selecting chat:', chat.id);
    dispatch(setCurrentChat(chat));
  };
  
  return (
    <div className="chat-page-container">
      <Sidebar 
        isOpen={isSidebarOpen}
        toggleSidebar={() => setSidebarOpen(!isSidebarOpen)}
        chats={chats}
        currentChatId={currentChat?.id}
        onNewChat={handleNewChat}
        onChatSelect={handleChatSelect}
      />
      <main className="chat-main">
        <ChatView chat={currentChat} />
      </main>
    </div>
  );
};

export default ChatPage; 