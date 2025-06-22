import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import api from '../api';

export const fetchChats = createAsyncThunk('chats/fetchChats', async (_, thunkAPI) => {
  try {
    const response = await api.get('/chats/');
    return response.data;
  } catch (error) {
    return thunkAPI.rejectWithValue(error.response?.data || error.message);
  }
});

export const createChat = createAsyncThunk('chats/createChat', async (chatData, thunkAPI) => {
  try {
    const response = await api.post('/chats/', chatData);
    return response.data;
  } catch (error) {
    return thunkAPI.rejectWithValue(error.response?.data || error.message);
  }
});

export const renameChat = createAsyncThunk('chats/renameChat', async ({ chatId, newName }, thunkAPI) => {
  try {
    const response = await api.patch(`/chats/${chatId}/rename/`, { name: newName });
    return response.data;
  } catch (error) {
    return thunkAPI.rejectWithValue(error.response?.data || error.message);
  }
});

export const deleteChat = createAsyncThunk('chats/deleteChat', async (chatId, thunkAPI) => {
  try {
    await api.delete(`/chats/${chatId}/`);
    return chatId;
  } catch (error) {
    return thunkAPI.rejectWithValue(error.response?.data || error.message);
  }
});

const chatsSlice = createSlice({
  name: 'chats',
  initialState: {
    items: [],
    currentChat: null,
    status: 'idle',
    error: null,
  },
  reducers: {
    setCurrentChat(state, action) {
      state.currentChat = action.payload;
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(fetchChats.pending, (state) => {
        state.status = 'loading';
        state.error = null;
      })
      .addCase(fetchChats.fulfilled, (state, action) => {
        state.status = 'succeeded';
        state.items = action.payload.results;
        if (state.items && state.items.length > 0 && !state.currentChat) {
          state.currentChat = state.items[0];
        }
      })
      .addCase(fetchChats.rejected, (state, action) => {
        state.status = 'failed';
        state.error = action.payload;
      })
      .addCase(createChat.fulfilled, (state, action) => {
        state.items.unshift(action.payload);
        state.currentChat = action.payload;
      })
      .addCase(createChat.rejected, (state, action) => {
        state.error = action.payload || action.error.message;
      })
      .addCase(renameChat.fulfilled, (state, action) => {
        const index = state.items.findIndex(chat => chat.id === action.payload.id);
        if (index !== -1) {
          state.items[index] = action.payload;
        }
        if (state.currentChat && state.currentChat.id === action.payload.id) {
          state.currentChat = action.payload;
        }
      })
      .addCase(renameChat.rejected, (state, action) => {
        state.error = action.payload || action.error.message;
      })
      .addCase(deleteChat.fulfilled, (state, action) => {
        state.items = state.items.filter(chat => chat.id !== action.payload);
        if (state.currentChat && state.currentChat.id === action.payload) {
          state.currentChat = state.items.length > 0 ? state.items[0] : null;
        }
      })
      .addCase(deleteChat.rejected, (state, action) => {
        state.error = action.payload || action.error.message;
      });
  },
});

export const { setCurrentChat } = chatsSlice.actions;
export default chatsSlice.reducer; 