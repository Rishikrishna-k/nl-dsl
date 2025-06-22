import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import api from '../api';

export const login = createAsyncThunk('auth/login', async (credentials, thunkAPI) => {
  try {
    const response = await api.post('/auth/login/', credentials);
    const { access, refresh, user } = response.data;
    localStorage.setItem('accessToken', access);
    localStorage.setItem('refreshToken', refresh);
    localStorage.setItem('user', JSON.stringify(user));
    return { user, access, refresh };
  } catch (error) {
    return thunkAPI.rejectWithValue(error.response?.data || error.message);
  }
});

export const restoreSession = createAsyncThunk('auth/restoreSession', async (_, thunkAPI) => {
  const token = localStorage.getItem('accessToken');
  const user = JSON.parse(localStorage.getItem('user') || 'null');
  if (token && user) {
    return { user, access: token, refresh: localStorage.getItem('refreshToken') };
  }
  return thunkAPI.rejectWithValue('No session');
});

const authSlice = createSlice({
  name: 'auth',
  initialState: { user: null, access: null, refresh: null, status: 'idle', error: null, restoring: true },
  reducers: {
    logout(state) {
      state.user = null;
      state.access = null;
      state.refresh = null;
      localStorage.clear();
      state.restoring = false;
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(login.fulfilled, (state, action) => {
        state.user = action.payload.user;
        state.access = action.payload.access;
        state.refresh = action.payload.refresh;
        state.status = 'succeeded';
        state.restoring = false;
      })
      .addCase(login.rejected, (state, action) => {
        state.error = action.payload || action.error.message;
        state.status = 'failed';
        state.restoring = false;
      })
      .addCase(restoreSession.pending, (state) => {
        state.restoring = true;
      })
      .addCase(restoreSession.fulfilled, (state, action) => {
        state.user = action.payload.user;
        state.access = action.payload.access;
        state.refresh = action.payload.refresh;
        state.status = 'succeeded';
        state.restoring = false;
      })
      .addCase(restoreSession.rejected, (state) => {
        state.restoring = false;
      });
  },
});

export const { logout } = authSlice.actions;
export default authSlice.reducer; 