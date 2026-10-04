import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { describe, expect, it, vi } from 'vitest';
import AnalysisInput from '../components/AnalysisInput.jsx';

describe('AnalysisInput', () => {
  it('blocks empty submit and does not call onSubmit', async () => {
    const user = userEvent.setup();
    const onSubmit = vi.fn();
    render(<AnalysisInput onSubmit={onSubmit} />);
    await user.click(screen.getByRole('button', { name: /analyze/i }));
    expect(onSubmit).not.toHaveBeenCalled();
    expect(screen.getByText(/enter a news article/i)).toBeInTheDocument();
  });
});
