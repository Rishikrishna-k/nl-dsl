import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import api from '../api';
import { addMessage } from './messagesSlice';

export const fetchBranchesByChat = createAsyncThunk('branches/fetchByChat', async (chatId, thunkAPI) => {
  try {
    const response = await api.get(`/chat-graph/${chatId}/branches/`);
    return response.data.branches; 
  } catch (error) {
    return thunkAPI.rejectWithValue(error.response?.data || error.message);
  }
});

export const createBranch = createAsyncThunk('branches/createBranch', async (branchData, thunkAPI) => {
  try {
    console.log('[createBranch] Request:', branchData);
    const response = await api.post('/branches/', branchData);
    console.log('[createBranch] Response:', response.data);
    return response.data;
  } catch (error) {
    console.error('[createBranch] Error:', error);
    return thunkAPI.rejectWithValue(error.response?.data || error.message);
  }
});

const branchesSlice = createSlice({
  name: 'branches',
  initialState: {
    items: [],
    currentBranch: null,
    status: 'idle',
    error: null,
  },
  reducers: {
    setCurrentBranch(state, action) {
      state.currentBranch = action.payload;
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(fetchBranchesByChat.pending, (state) => {
        state.status = 'loading';
        state.error = null;
      })
      .addCase(fetchBranchesByChat.fulfilled, (state, action) => {
        state.status = 'succeeded';
        state.items = action.payload;
      })
      .addCase(fetchBranchesByChat.rejected, (state, action) => {
        state.status = 'failed';
        state.error = action.payload || action.error.message;
      })
      .addCase(createBranch.fulfilled, (state, action) => {
        state.items.push(action.payload);
        state.currentBranch = action.payload;
      })
      .addCase(createBranch.rejected, (state, action) => {
        state.error = action.payload || action.error.message;
      })
      .addCase(addMessage.fulfilled, (state, action) => {
        if (state.currentBranch) {
          state.currentBranch.head_message_id = action.payload.id;
        }
      });
  },
});

export const { setCurrentBranch } = branchesSlice.actions;
export default branchesSlice.reducer; 