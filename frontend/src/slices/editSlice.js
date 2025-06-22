import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import api from '../api';

// Async thunk for editing message with branch creation
export const editMessageWithBranch = createAsyncThunk(
  'edit/editMessageWithBranch',
  async ({ chatId, originalMessageId, newContent }, { rejectWithValue }) => {
    try {
      console.log('[editSlice] Starting edit message with branch');
      console.log('[editSlice] Chat ID:', chatId);
      console.log('[editSlice] Original message ID:', originalMessageId);
      console.log('[editSlice] New content:', newContent);

      const response = await api.post('/edit/edit_with_branch/', {
        chat_id: chatId,
        original_message_id: originalMessageId,
        new_content: newContent
      });

      console.log('[editSlice] Edit response received:', response.data);
      console.log('[editSlice] Debug info:', response.data.debug_info);
      console.log('[editSlice] New branch:', response.data.new_branch);
      console.log('[editSlice] New message:', response.data.new_message);
      console.log('[editSlice] Edit record:', response.data.edit_record);
      console.log('[editSlice] Branch messages count:', response.data.branch_messages.length);
      console.log('[editSlice] All branches count:', response.data.all_branches.length);

      return response.data;
    } catch (error) {
      console.error('[editSlice] Edit failed:', error);
      console.error('[editSlice] Error response:', error.response?.data);
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);

// Async thunk for getting branch messages
export const getBranchMessages = createAsyncThunk(
  'edit/getBranchMessages',
  async ({ chatId, headId }, { rejectWithValue }) => {
    try {
      console.log('[editSlice] Getting branch messages');
      console.log('[editSlice] Chat ID:', chatId);
      console.log('[editSlice] Head ID:', headId);

      const response = await api.get(`/edit/get_branch_messages/?chat_id=${chatId}&head_id=${headId}`);

      console.log('[editSlice] Branch messages response:', response.data);
      console.log('[editSlice] Debug info:', response.data.debug_info);
      console.log('[editSlice] Messages count:', response.data.messages.length);

      return response.data;
    } catch (error) {
      console.error('[editSlice] Get branch messages failed:', error);
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);

// Async thunk for getting all branches
export const getAllBranches = createAsyncThunk(
  'edit/getAllBranches',
  async (chatId, { rejectWithValue }) => {
    try {
      console.log('[editSlice] Getting all branches for chat:', chatId);

      const response = await api.get(`/edit/get_all_branches/?chat_id=${chatId}`);

      console.log('[editSlice] All branches response:', response.data);
      console.log('[editSlice] Debug info:', response.data.debug_info);
      console.log('[editSlice] Branches count:', response.data.branches.length);

      return response.data;
    } catch (error) {
      console.error('[editSlice] Get all branches failed:', error);
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);

// Async thunk for enhanced edit workflow
export const enhancedEditWithBranch = createAsyncThunk(
  'edit/enhancedEditWithBranch',
  async ({ chatId, originalMessageId, newContent }, { rejectWithValue }) => {
    try {
      console.log('[editSlice] Starting enhanced edit workflow');
      console.log('[editSlice] Chat ID:', chatId);
      console.log('[editSlice] Original message ID:', originalMessageId);
      console.log('[editSlice] New content:', newContent);

      const response = await api.post('/edit/enhanced_edit_with_branch/', {
        chat_id: chatId,
        original_message_id: originalMessageId,
        new_content: newContent
      });

      console.log('[editSlice] Enhanced edit response received:', response.data);
      
      // Print all debug information
      console.log('='.repeat(80));
      console.log('ENHANCED EDIT WORKFLOW DEBUG INFO');
      console.log('='.repeat(80));
      
      const debugInfo = response.data.debug_info || {};
      console.log('📊 DEBUG INFO:', debugInfo);
      
      const steps = debugInfo.steps_completed || [];
      console.log('✅ STEPS COMPLETED:', steps);
      
      const newBranch = response.data.new_branch || {};
      console.log('🌿 NEW BRANCH:', newBranch);
      
      const newMessage = response.data.new_message || {};
      console.log('💬 NEW MESSAGE:', newMessage);
      
      const editRecord = response.data.edit_record || {};
      console.log('📝 EDIT RECORD:', editRecord);
      
      const branchComparison = response.data.branch_comparison || {};
      console.log('🔄 BRANCH COMPARISON:', branchComparison);
      
      const allBranches = response.data.all_branches || [];
      console.log('🌳 ALL BRANCHES:', allBranches);
      
      const updatedGraph = response.data.updated_graph || {};
      console.log('🗺️ UPDATED GRAPH:', updatedGraph);
      
      console.log('='.repeat(80));
      console.log('ENHANCED EDIT WORKFLOW COMPLETED SUCCESSFULLY!');
      console.log('='.repeat(80));

      return response.data;
    } catch (error) {
      console.error('[editSlice] Enhanced edit failed:', error);
      console.error('[editSlice] Error response:', error.response?.data);
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);

// Async thunk for loading messages for a specific branch
export const loadBranchMessages = createAsyncThunk(
  'edit/loadBranchMessages',
  async ({ chatId, headId }, { rejectWithValue }) => {
    try {
      console.log('[editSlice] Loading messages for branch');
      console.log('[editSlice] Chat ID:', chatId);
      console.log('[editSlice] Head ID:', headId);

      const response = await api.get(`/edit/get_branch_messages/?chat_id=${chatId}&head_id=${headId}`);

      console.log('[editSlice] Branch messages response:', response.data);
      console.log('[editSlice] Messages count:', response.data.messages.length);

      return response.data;
    } catch (error) {
      console.error('[editSlice] Load branch messages failed:', error);
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);

const editSlice = createSlice({
  name: 'edit',
  initialState: {
    // Edit workflow state
    isEditing: false,
    editingMessage: null,
    editValue: '',
    
    // Current branch state
    currentBranch: null,
    currentBranchMessages: [],
    
    // All branches state
    allBranches: [],
    
    // Debug information
    lastEditResult: null,
    lastDebugInfo: null,
    
    // Loading states
    editLoading: false,
    branchMessagesLoading: false,
    allBranchesLoading: false,
    
    // Error states
    editError: null,
    branchMessagesError: null,
    allBranchesError: null,
  },
  reducers: {
    // Start editing a message
    startEdit: (state, action) => {
      const { message } = action.payload;
      console.log('[editSlice] Starting edit for message:', message.id);
      state.isEditing = true;
      state.editingMessage = message;
      state.editValue = message.content;
      state.editError = null;
    },
    
    // Update edit value
    updateEditValue: (state, action) => {
      state.editValue = action.payload;
    },
    
    // Cancel editing
    cancelEdit: (state) => {
      console.log('[editSlice] Canceling edit');
      state.isEditing = false;
      state.editingMessage = null;
      state.editValue = '';
      state.editError = null;
    },
    
    // Set current branch
    setCurrentBranch: (state, action) => {
      const { branchId, headId } = action.payload;
      console.log('[editSlice] Setting current branch:', branchId, 'with head:', headId);
      state.currentBranch = { branchId, headId };
    },
    
    // Clear edit state
    clearEditState: (state) => {
      console.log('[editSlice] Clearing edit state');
      state.isEditing = false;
      state.editingMessage = null;
      state.editValue = '';
      state.currentBranch = null;
      state.currentBranchMessages = [];
      state.allBranches = [];
      state.lastEditResult = null;
      state.lastDebugInfo = null;
      state.editError = null;
      state.branchMessagesError = null;
      state.allBranchesError = null;
    },
  },
  extraReducers: (builder) => {
    builder
      // Edit message with branch
      .addCase(editMessageWithBranch.pending, (state) => {
        console.log('[editSlice] Edit message pending');
        state.editLoading = true;
        state.editError = null;
      })
      .addCase(editMessageWithBranch.fulfilled, (state, action) => {
        console.log('[editSlice] Edit message fulfilled');
        state.editLoading = false;
        state.isEditing = false;
        state.editingMessage = null;
        state.editValue = '';
        state.lastEditResult = action.payload;
        state.lastDebugInfo = action.payload.debug_info;
        
        // Update current branch to the new branch
        if (action.payload.new_branch) {
          state.currentBranch = {
            branchId: action.payload.new_branch.branch_id,
            headId: action.payload.new_branch.head_message_id
          };
        }
        
        // Update branch messages
        state.currentBranchMessages = action.payload.branch_messages;
        
        // Update all branches
        state.allBranches = action.payload.all_branches;
        
        console.log('[editSlice] Edit completed successfully');
        console.log('[editSlice] New branch set:', state.currentBranch);
        console.log('[editSlice] Branch messages updated:', state.currentBranchMessages.length);
        console.log('[editSlice] All branches updated:', state.allBranches.length);
      })
      .addCase(editMessageWithBranch.rejected, (state, action) => {
        console.log('[editSlice] Edit message rejected:', action.payload);
        state.editLoading = false;
        state.editError = action.payload;
      })
      
      // Get branch messages
      .addCase(getBranchMessages.pending, (state) => {
        console.log('[editSlice] Get branch messages pending');
        state.branchMessagesLoading = true;
        state.branchMessagesError = null;
      })
      .addCase(getBranchMessages.fulfilled, (state, action) => {
        console.log('[editSlice] Get branch messages fulfilled');
        state.branchMessagesLoading = false;
        state.currentBranchMessages = action.payload.messages;
        console.log('[editSlice] Branch messages updated:', state.currentBranchMessages.length);
      })
      .addCase(getBranchMessages.rejected, (state, action) => {
        console.log('[editSlice] Get branch messages rejected:', action.payload);
        state.branchMessagesLoading = false;
        state.branchMessagesError = action.payload;
      })
      
      // Get all branches
      .addCase(getAllBranches.pending, (state) => {
        console.log('[editSlice] Get all branches pending');
        state.allBranchesLoading = true;
        state.allBranchesError = null;
      })
      .addCase(getAllBranches.fulfilled, (state, action) => {
        console.log('[editSlice] Get all branches fulfilled');
        state.allBranchesLoading = false;
        state.allBranches = action.payload.branches;
        console.log('[editSlice] All branches updated:', state.allBranches.length);
      })
      .addCase(getAllBranches.rejected, (state, action) => {
        console.log('[editSlice] Get all branches rejected:', action.payload);
        state.allBranchesLoading = false;
        state.allBranchesError = action.payload;
      })
      
      // Enhanced edit with branch
      .addCase(enhancedEditWithBranch.pending, (state) => {
        console.log('[editSlice] Enhanced edit pending');
        state.editLoading = true;
        state.editError = null;
      })
      .addCase(enhancedEditWithBranch.fulfilled, (state, action) => {
        console.log('[editSlice] Enhanced edit fulfilled');
        state.editLoading = false;
        state.isEditing = false;
        state.editingMessage = null;
        state.editValue = '';
        state.lastEditResult = action.payload;
        state.lastDebugInfo = action.payload.debug_info;
        
        // Update current branch to the new branch
        if (action.payload.new_branch) {
          state.currentBranch = {
            branchId: action.payload.new_branch.branch_id,
            headId: action.payload.new_branch.head_message_id
          };
        }
        
        // Update branch messages from the new branch
        if (action.payload.branch_comparison && action.payload.branch_comparison.new_branch) {
          state.currentBranchMessages = action.payload.branch_comparison.new_branch.messages;
        }
        
        // Update all branches
        state.allBranches = action.payload.all_branches;
        
        console.log('[editSlice] Enhanced edit completed successfully');
        console.log('[editSlice] New branch set:', state.currentBranch);
        console.log('[editSlice] Branch messages updated:', state.currentBranchMessages.length);
        console.log('[editSlice] All branches updated:', state.allBranches.length);
      })
      .addCase(enhancedEditWithBranch.rejected, (state, action) => {
        console.log('[editSlice] Enhanced edit rejected:', action.payload);
        state.editLoading = false;
        state.editError = action.payload;
      });
  },
});

export const { 
  startEdit, 
  updateEditValue, 
  cancelEdit, 
  setCurrentBranch, 
  clearEditState 
} = editSlice.actions;

export default editSlice.reducer; 