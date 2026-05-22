import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import Page from '../../src/app/page';

// Mock next/navigation
const pushMock = vi.fn();
vi.mock('next/navigation', () => ({
  useRouter: () => ({
    push: pushMock,
  }),
}));

describe('Login Flow Integration (Motorista)', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    Storage.prototype.setItem = vi.fn();
  });

  it('deve logar como motorista, salvar token e redirecionar para /drive', async () => {
    render(<Page />);

    // Fill form
    fireEvent.change(screen.getByLabelText(/e-mail/i), { target: { value: 'motorista@test.com' } });
    fireEvent.change(screen.getByLabelText(/senha/i), { target: { value: '1234' } });

    // Submit
    fireEvent.click(screen.getByRole('button', { name: /entrar/i }));

    // Wait for async actions
    await waitFor(() => {
      // Expect token saved
      expect(Storage.prototype.setItem).toHaveBeenCalledWith('token', 'fake_motorista_token');
      // Expect redirect to drive
      expect(pushMock).toHaveBeenCalledWith('/drive');
    });
  });
});
