import React from 'react';
import { useDispatch } from 'react-redux';
import { logout } from '../slices/authSlice';
import { useNavigate } from 'react-router-dom';

const Dashboard = () => {
  const dispatch = useDispatch();
  const navigate = useNavigate();

  const handleLogout = () => {
    dispatch(logout());
    navigate('/login');
  };

  return (
    <div style={{ padding: '2rem', textAlign: 'center' }}>
      <h1>Welcome to the Dashboard!</h1>
      <p>This is a placeholder page. Content will be added soon.</p>
      <button onClick={handleLogout} style={{ marginTop: '2rem', padding: '0.5rem 1.5rem', fontSize: '1rem' }}>
        Logout
      </button>
    </div>
  );
};

export default Dashboard; 