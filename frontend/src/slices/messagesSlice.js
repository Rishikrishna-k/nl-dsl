import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import api from '../api';

export const fetchMessagesForChat = createAsyncThunk(
  'messages/fetchForChat', 
  async (chatId, thunkAPI) => {
    try {
      console.log(`[fetchMessagesForChat] Fetching messages for chat: ${chatId}`);
      const response = await api.get(`/chats/${chatId}/messages/`);
      console.log(`[fetchMessagesForChat] Response:`, response.data);
      return response.data;
    } catch (error) {
      console.error(`[fetchMessagesForChat] Error:`, error);
      return thunkAPI.rejectWithValue(error.response?.data || error.message);
    }
});

export const addMessage = createAsyncThunk(
  'messages/addMessage', 
  async ({ chatId, content }, thunkAPI) => {
    try {
      console.log(`[addMessage] Sending message to chat ${chatId}:`, content);
      const response = await api.post(`/chats/${chatId}/add_message/`, { content });
      console.log(`[addMessage] Response:`, response.data);
      return response.data;
    } catch (error) {
      console.error(`[addMessage] Error:`, error);
      return thunkAPI.rejectWithValue(error.response?.data || error.message);
    }
});

const messagesSlice = createSlice({
  name: 'messages',
  initialState: {
    items: [],
    status: 'idle',
    error: null,
  },
  reducers: {
    clearMessages(state) {
      state.items = [];
      state.status = 'idle';
      state.error = null;
    },
    formatAsCode(state, action) {
      const { messageId } = action.payload;
      const message = state.items.find(item => item.id === messageId);
      if (message) {
        // Use python as a default language for the new code block
        message.content = "```python\n" + message.content + "\n```";
      }
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(fetchMessagesForChat.pending, (state) => {
        state.status = 'loading';
        state.error = null;
      })
      .addCase(fetchMessagesForChat.fulfilled, (state, action) => {
        state.status = 'succeeded';
        state.items = action.payload;
        console.log(`[fetchMessagesForChat] Updated messages:`, state.items);
      })
      .addCase(fetchMessagesForChat.rejected, (state, action) => {
        state.status = 'failed';
        state.error = action.payload || action.error.message;
        console.error(`[fetchMessagesForChat] Failed:`, state.error);
      })
      .addCase(addMessage.fulfilled, (state, action) => {
        // Add both user and AI messages to the list
        if (action.payload.user_message) {
          state.items.push(action.payload.user_message);
        }
        if (action.payload.ai_message) {
          state.items.push(action.payload.ai_message);
        }
        console.log(`[addMessage] Updated messages:`, state.items);
      })
      .addCase(addMessage.rejected, (state, action) => {
        state.error = action.payload || action.error.message;
        console.error(`[addMessage] Failed:`, state.error);
      });
  },
});

export const { clearMessages, formatAsCode } = messagesSlice.actions;
export default messagesSlice.reducer; 