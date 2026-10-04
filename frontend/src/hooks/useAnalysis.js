import { useContext } from 'react';
import { AnalysisContext } from '../context/AnalysisContext.jsx';

export function useAnalysis() {
  const ctx = useContext(AnalysisContext);
  if (!ctx) throw new Error('useAnalysis must be used within AnalysisProvider');
  return ctx;
}
