import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import Registration from './pages/Registration';
import Dashboard from './pages/Dashboard';
import Login from './pages/Login';
import './App.css';
import { useSelector } from 'react-redux';

function ProtectedRoute({ children }) {
  const auth = useSelector((state) => state.auth);
  if (auth.restoring) {
    return <div>Loading...</div>;
  }
  if (!auth.user || !auth.access) {
    return <Navigate to="/login" replace />;
  }
  return children;
}

function App() {
  return (
    <div className="App">
      <Routes>
        <Route path="/register" element={<Registration />} />
        <Route path="/login" element={<Login />} />
        <Route path="/dashboard" element={
          <ProtectedRoute>
            <Dashboard />
          </ProtectedRoute>
        } />
        {/* Redirect to registration page by default */}
        <Route path="*" element={<Navigate to="/register" />} />
      </Routes>
    </div>
  );
}

export default App;