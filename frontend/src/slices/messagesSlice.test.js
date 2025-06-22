import { configureStore } from '@reduxjs/toolkit';
import messagesReducer, { fetchMessagesForBranch, addMessage, editMessage } from './messagesSlice';
import axios from 'axios';

jest.mock('axios');

describe('messagesSlice', () => {
  let store;
  beforeEach(() => {
    store = configureStore({ reducer: { messages: messagesReducer } });
  });

  it('should handle initial state', () => {
    const state = store.getState().messages;
    expect(state.items).toEqual([]);
    expect(state.status).toBe('idle');
    expect(state.error).toBeNull();
  });

  it('should fetch messages for branch', async () => {
    axios.get.mockResolvedValueOnce({ data: [{ id: 'm1', content: 'Hello' }] });
    await store.dispatch(fetchMessagesForBranch('b1'));
    const state = store.getState().messages;
    expect(state.items).toHaveLength(1);
    expect(state.items[0].content).toBe('Hello');
    expect(state.status).toBe('succeeded');
  });

  it('should add a message', async () => {
    const msg = { id: 'm2', content: 'New message' };
    axios.post.mockResolvedValueOnce({ data: msg });
    await store.dispatch(addMessage(msg));
    const state = store.getState().messages;
    expect(state.items.some((m) => m.id === 'm2')).toBe(true);
  });

  it('should edit a message (create new branch)', async () => {
    const msg = { id: 'm3', content: 'Edited message' };
    axios.post.mockResolvedValueOnce({ data: msg }); // message
    axios.patch.mockResolvedValueOnce({}); // update graph
    axios.post.mockResolvedValueOnce({ data: { branch_id: 'b2', head_message_id: 'm3' } }); // branch
    axios.post.mockResolvedValueOnce({}); // edit event
    await store.dispatch(editMessage({
      editData: {
        newMessage: msg,
        chatId: 'c1',
        updatedGraph: {},
        editEvent: { chat: 'c1', branch: 'b1', prev_message_id: 'm1', new_message_id: 'm3', new_head_id: 'm3' },
      },
      branchData: { chat: 'c1', head_message_id: 'm3' },
    }));
    const state = store.getState().messages;
    expect(state.items.some((m) => m.id === 'm3')).toBe(true);
  });
}); 