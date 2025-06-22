import { configureStore } from '@reduxjs/toolkit';
import chatsReducer from './slices/chatsSlice';
import branchesReducer from './slices/branchesSlice';
import messagesReducer from './slices/messagesSlice';
import authReducer from './slices/authSlice';

const store = configureStore({
  reducer: {
    auth: authReducer,
    chats: chatsReducer,
    branches: branchesReducer,
    messages: messagesReducer,
  },
});

export default store; 