import { configureStore } from '@reduxjs/toolkit';
import chatsReducer, { fetchChats, createChat, setCurrentChat } from './chatsSlice';
import axios from 'axios';

jest.mock('axios');

describe('chatsSlice', () => {
  let store;
  beforeEach(() => {
    store = configureStore({ reducer: { chats: chatsReducer } });
  });

  it('should handle initial state', () => {
    const state = store.getState().chats;
    expect(state.items).toEqual([]);
    expect(state.currentChat).toBeNull();
    expect(state.status).toBe('idle');
    expect(state.error).toBeNull();
  });

  it('should fetch chats', async () => {
    axios.get.mockResolvedValueOnce({ data: [{ id: '1', name: 'Test Chat' }] });
    await store.dispatch(fetchChats());
    const state = store.getState().chats;
    expect(state.items).toHaveLength(1);
    expect(state.items[0].name).toBe('Test Chat');
    expect(state.status).toBe('succeeded');
  });

  it('should create a chat', async () => {
    const chat = { id: '2', name: 'New Chat' };
    axios.post.mockResolvedValueOnce({ data: chat });
    await store.dispatch(createChat(chat));
    const state = store.getState().chats;
    expect(state.items.some((c) => c.id === '2')).toBe(true);
    expect(state.currentChat.id).toBe('2');
  });

  it('should set current chat', () => {
    store.dispatch(setCurrentChat({ id: '3', name: 'Current' }));
    expect(store.getState().chats.currentChat.id).toBe('3');
  });
}); 