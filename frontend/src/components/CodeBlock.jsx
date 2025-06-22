import React, { useState, useEffect } from 'react';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { vscDarkPlus } from 'react-syntax-highlighter/dist/esm/styles/prism';
import './CodeBlock.css';

const CodeBlock = ({ language, code }) => {
  const [isCopied, setIsCopied] = useState(false);
  const [isExpanded, setIsExpanded] = useState(false);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [maxHeight, setMaxHeight] = useState(400);

  // Calculate appropriate height based on content
  useEffect(() => {
    const lines = code.split('\n').length;
    const baseHeight = 200; // Minimum height
    const lineHeight = 20; // Approximate line height
    const calculatedHeight = Math.min(Math.max(baseHeight, lines * lineHeight), 600); // Max 600px
    setMaxHeight(calculatedHeight);
  }, [code]);

  const handleCopy = () => {
    navigator.clipboard.writeText(code).then(() => {
      setIsCopied(true);
      setTimeout(() => setIsCopied(false), 2500);
    });
  };

  const handleExpand = () => {
    setIsExpanded(!isExpanded);
  };

  const handleModalOpen = () => {
    setIsModalOpen(true);
  };

  const handleModalClose = () => {
    setIsModalOpen(false);
  };

  return (
    <>
      <div className={`code-block-container ${isExpanded ? 'expanded' : ''}`}>
        <div className="code-block-header">
          <div className="code-title">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M16 18L22 12L16 6" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/><path d="M8 6L2 12L8 18" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/></svg>
              <span>{language || 'code'}</span>
          </div>
          <div className="code-actions">
              <button onClick={handleCopy} className="header-action-btn" title={isCopied ? "Copied!" : "Copy code"}>
                  {isCopied ? 'Copied' : 'Copy'}
              </button>
              <button onClick={handleModalOpen} className="header-action-btn" title="Open in modal">
                  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M15 3H21V9M9 21H3V15M21 3L13 11M3 21L11 13" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/></svg>
              </button>
          </div>
        </div>
        <div className="syntax-highlighter-wrapper" style={{ maxHeight: isExpanded ? '80vh' : `${maxHeight}px` }}>
          <SyntaxHighlighter
            language={language || 'text'}
            style={vscDarkPlus}
            className="syntax-highlighter"
            showLineNumbers={true}
            wrapLines={true}
          >
            {code}
          </SyntaxHighlighter>
        </div>
      </div>

      {/* Modal */}
      {isModalOpen && (
        <div className="code-modal-overlay" onClick={handleModalClose}>
          <div className="code-modal" onClick={(e) => e.stopPropagation()}>
            <div className="code-modal-header">
              <div className="code-modal-title">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M16 18L22 12L16 6" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/><path d="M8 6L2 12L8 18" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/></svg>
                <span>{language || 'code'}</span>
              </div>
              <div className="code-modal-actions">
                <button onClick={handleCopy} className="modal-action-btn" title={isCopied ? "Copied!" : "Copy code"}>
                  {isCopied ? 'Copied' : 'Copy'}
                </button>
                <button onClick={handleModalClose} className="modal-action-btn" title="Close">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M18 6L6 18M6 6L18 18" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/></svg>
                </button>
              </div>
            </div>
            <div className="code-modal-content">
              <SyntaxHighlighter
                language={language || 'text'}
                style={vscDarkPlus}
                className="syntax-highlighter modal-syntax-highlighter"
                showLineNumbers={true}
                wrapLines={true}
              >
                {code}
              </SyntaxHighlighter>
            </div>
          </div>
        </div>
      )}
    </>
  );
};

export default CodeBlock; 