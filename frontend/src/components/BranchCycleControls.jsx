import React from 'react';

const BranchCycleControls = ({ onPrev, onNext }) => (
  <span className="branch-cycle-controls" style={{ display: 'inline-flex', alignItems: 'center', gap: '0.25rem' }}>
    <button type="button" onClick={onPrev} aria-label="Previous version" style={{ cursor: 'pointer' }}>
      ←
    </button>
    <button type="button" onClick={onNext} aria-label="Next version" style={{ cursor: 'pointer' }}>
      →
    </button>
  </span>
);

export default BranchCycleControls; 