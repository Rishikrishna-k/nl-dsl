import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useDispatch, useSelector } from 'react-redux';
import { login } from '../slices/authSlice';
import './Login.css'; // We'll create this for styling

// Re-using the Dialog component concept from Registration
const Dialog = ({ dialog, onDismiss, children }) => {
    if (!dialog.message) return null;
    return (
        <div className={`dialog-overlay ${dialog.type}`}>
            <div className="dialog-box">
                <p>{dialog.message}</p>
                {children}
                <button onClick={onDismiss} className="dialog-close-btn">Close</button>
            </div>
        </div>
    );
};

// --- Icon Components (for social logins) ---
const GoogleIcon = () => <svg height="20" viewBox="0 0 20 20" width="20"><path d="M19.6 10.23c0-.62-.06-1.22-.16-1.81H10.1v3.41h5.3c-.22 1.11-.88 2.06-1.85 2.71v2.32h3.01c1.76-1.62 2.76-3.95 2.76-6.63z" fill="#4285F4"></path><path d="M10.1 20c2.7 0 4.96-.89 6.62-2.42l-3.01-2.32c-.9.6-2.05.96-3.61.96-2.76 0-5.1-1.86-5.94-4.37H.9v2.4C2.72 17.02 6.14 20 10.1 20z" fill="#34A853"></path><path d="M4.16 11.78c-.18-.54-.28-1.12-.28-1.72s.1-1.18.28-1.72V5.94H.9C.32 7.08 0 8.48 0 10.06c0 1.58.32 2.98.9 4.12l3.26-2.4z" fill="#FBBC05"></path><path d="M10.1 4.16c1.47 0 2.8.51 3.84 1.52l2.67-2.67C15.05 1.18 12.8 0 10.1 0 6.14 0 2.72 2.98.9 6.66l3.26 2.4c.84-2.5 3.18-4.37 5.94-4.37z" fill="#EA4335"></path></svg>;
const MicrosoftIcon = () => <svg height="20" viewBox="0 0 20 20" width="20"><path d="M9.5 9.5H1V1h8.5v8.5zM20 9.5h-8.5V1H20v8.5zM9.5 20H1v-8.5h8.5V20zM20 20h-8.5v-8.5H20V20z" fill="#F25022"></path></svg>;
const AppleIcon = () => <svg height="20" viewBox="0 0 20 20" width="20"><path d="M16.14 10.2c.02-1.82-1.35-2.9-2.8-2.94-1.2-.02-2.3 1-3.04 1-.77 0-1.6-1-2.8-1-1.48 0-2.92 1.2-2.92 3.1 0 2.22 1.74 3.32 3.13 3.32.73 0 1.6-.53 2.52-.53s1.7.53 2.5.53c1.55 0 3.29-1.3 3.29-3.51zM14.6 4.6c.74-.9 1.2-2.1.95-3.1-.9.08-2.1.65-2.85 1.5-.7.83-1.3 2.1-.9 3.1.95-.03 2.1-.67 2.8-1.5z"></path></svg>;
const PhoneIcon = () => <svg height="20" viewBox="0 0 20 20" width="20" fill="none" stroke="currentColor" strokeWidth="1.5"><path d="M6.05 4.3C6.39 3.55 7.07 3 7.86 3h4.28c.79 0 1.47.55 1.81 1.3l.03.07c.34.75.34 1.6 0 2.35l-.03.07c-.34.75-1.02 1.3-1.81 1.3H7.86c-.79 0-1.47-.55-1.81-1.3l-.03-.07a2.3 2.3 0 010-2.35l.03-.07zM10 13v4M8 17h4"></path></svg>;

const Login = () => {
    const [step, setStep] = useState(1);
    const [formData, setFormData] = useState({
        email: '',
        password: '',
    });
    const [dialog, setDialog] = useState({ message: null, type: null });
    const dispatch = useDispatch();
    const navigate = useNavigate();
    const { status, error } = useSelector((state) => state.auth);

    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const handleNextStep = (e) => {
        e.preventDefault();
        if (!formData.email || !/\S+@\S+\.\S+/.test(formData.email)) {
            setDialog({ message: 'Please enter a valid email address.', type: 'error' });
            return;
        }
        setStep(2);
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setDialog({ message: null, type: null });

        if (!formData.password) {
            setDialog({ message: 'Please enter your password.', type: 'error' });
            return;
        }

        try {
            const result = await dispatch(login(formData)).unwrap();
            setDialog({ message: 'Login successful! Redirecting...', type: 'success' });
            setTimeout(() => navigate('/dashboard'), 1000);
        } catch (err) {
            setDialog({ message: err || 'Login failed. Please check your credentials.', type: 'error' });
        }
    };

    const dismissDialog = () => setDialog({ message: null, type: null });

    return (
        <div className="login-container">
            <Dialog dialog={dialog} onDismiss={dismissDialog}>
                {dialog.type === 'success' && (
                    <>
                        <p style={{ fontSize: '0.9rem', marginTop: '-0.5rem', marginBottom: '1rem' }}>You will be redirected shortly.</p>
                        <Link to="/dashboard" className="dialog-link">
                            Click here to go now
                        </Link>
                    </>
                )}
            </Dialog>

            <div className="login-form-wrapper">
                <h1 className="logo-title">DSLGPT</h1>
                <h2 className="form-title">Welcome back</h2>
                
                <form onSubmit={step === 1 ? handleNextStep : handleSubmit}>
                    {step === 1 ? (
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
                    ) : (
                        <>
                            <div className="input-group email-display">
                                <label>Email address</label>
                                <p>{formData.email}</p>
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
                                    autoFocus
                                />
                            </div>
                        </>
                    )}
                    
                    <button type="submit" className="submit-btn" disabled={status === 'loading'}>
                        {status === 'loading' ? 'Continuing...' : 'Continue'}
                    </button>
                    {step === 2 && (
                        <button type="button" className="back-btn" onClick={() => setStep(1)}>
                            Back
                        </button>
                    )}
                </form>

                <p className="signup-prompt">
                    Don't have an account? <Link to="/register">Sign up</Link>
                </p>

                 {step === 1 && (
                    <>
                        <div className="separator">OR</div>
                        <div className="social-logins">
                            <button className="social-btn"><GoogleIcon /> Continue with Google</button>
                            <button className="social-btn"><MicrosoftIcon /> Continue with Microsoft</button>
                            <button className="social-btn"><AppleIcon /> Continue with Apple</button>
                            <button className="social-btn"><PhoneIcon /> Continue with phone</button>
                        </div>
                    </>
                )}
            </div>
        </div>
    );
};

export default Login; 