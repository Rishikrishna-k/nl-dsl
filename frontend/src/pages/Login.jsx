import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import './Login.css'; // We'll create this for styling

const Login = () => {
    const [formData, setFormData] = useState({
        email: '',
        password: '',
    });
    const [error, setError] = useState(null);
    const [loading, setLoading] = useState(false);

    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        // Dummy logic for now
        setError(null);
        setLoading(true);
        console.log('Logging in with:', formData);
        // Replace with actual API call
        setTimeout(() => {
            setError('Dummy login failed. This is a placeholder.');
            setLoading(false);
        }, 1000);
    };

    return (
        <div className="login-container">
            <div className="login-form-wrapper">
                <h1 className="logo-title">ChatGPT</h1>
                <h2 className="form-title">Welcome back</h2>

                <form onSubmit={handleSubmit}>
                    <div className="input-group">
                        <label htmlFor="email">Email address</label>
                        <input
                            type="email"
                            id="email"
                            name="email"
                            value={formData.email}
                            onChange={handleChange}
                            placeholder="Email address"
                            required
                        />
                    </div>
                    <div className="input-group">
                        <label htmlFor="password">Password</label>
                        <input
                            type="password"
                            id="password"
                            name="password"
                            value={formData.password}
                            onChange={handleChange}
                            placeholder="Password"
                            required
                        />
                    </div>

                    {error && <p className="error-dialog">{error}</p>}

                    <button type="submit" className="submit-btn" disabled={loading}>
                        {loading ? 'Logging in...' : 'Continue'}
                    </button>
                </form>

                <p className="signup-prompt">
                    Don't have an account? <Link to="/register">Sign up</Link>
                </p>
            </div>
        </div>
    );
};

export default Login; 