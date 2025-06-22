import { configureStore } from '@reduxjs/toolkit';
import branchesReducer, { fetchBranchesByChat, createBranch, setCurrentBranch } from './branchesSlice';
import axios from 'axios';

jest.mock('axios');

describe('branchesSlice', () => {
  let store;
  beforeEach(() => {
    store = configureStore({ reducer: { branches: branchesReducer } });
  });

  it('should handle initial state', () => {
    const state = store.getState().branches;
    expect(state.items).toEqual([]);
    expect(state.currentBranch).toBeNull();
    expect(state.status).toBe('idle');
    expect(state.error).toBeNull();
  });

  it('should fetch branches by chat', async () => {
    axios.get.mockResolvedValueOnce({ data: [{ branch_id: 'b1', head_message_id: 'm1' }] });
    await store.dispatch(fetchBranchesByChat('chat1'));
    const state = store.getState().branches;
    expect(state.items).toHaveLength(1);
    expect(state.items[0].branch_id).toBe('b1');
    expect(state.status).toBe('succeeded');
  });

  it('should create a branch', async () => {
    const branch = { branch_id: 'b2', head_message_id: 'm2' };
    axios.post.mockResolvedValueOnce({ data: branch });
    await store.dispatch(createBranch(branch));
    const state = store.getState().branches;
    expect(state.items.some((b) => b.branch_id === 'b2')).toBe(true);
    expect(state.currentBranch.branch_id).toBe('b2');
  });

  it('should set current branch', () => {
    store.dispatch(setCurrentBranch({ branch_id: 'b3', head_message_id: 'm3' }));
    expect(store.getState().branches.currentBranch.branch_id).toBe('b3');
  });
}); 