import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import Page from '../../src/app/page';

// Mock next/navigation
const pushMock = jest.fn();
jest.mock('next/navigation', () => ({
  useRouter: () => ({
    push: pushMock,
  }),
}));

describe('Login Flow Integration (Lojista)', () => {
  beforeEach(() => {
    jest.clearAllMocks();
    Storage.prototype.setItem = jest.fn();
  });

  it('deve logar como lojista, salvar token e redirecionar para /dashboard', async () => {
    render(<Page />);

    // Fill form
    fireEvent.change(screen.getByLabelText(/e-mail/i), { target: { value: 'lojista@test.com' } });
    fireEvent.change(screen.getByLabelText(/senha/i), { target: { value: '1234' } });

    // Submit
    fireEvent.click(screen.getByRole('button', { name: /entrar/i }));

    // Wait for async actions
    await waitFor(() => {
      // Expect token saved
      expect(Storage.prototype.setItem).toHaveBeenCalledWith('token', 'fake_lojista_token');
      // Expect redirect to dashboard
      expect(pushMock).toHaveBeenCalledWith('/dashboard');
    });
  });

  it('deve mostrar mensagem de erro em credenciais inválidas', async () => {
    render(<Page />);

    fireEvent.change(screen.getByLabelText(/e-mail/i), { target: { value: 'wrong@test.com' } });
    fireEvent.change(screen.getByLabelText(/senha/i), { target: { value: 'wrong' } });

    fireEvent.click(screen.getByRole('button', { name: /entrar/i }));

    await waitFor(() => {
      expect(screen.getByRole('alert')).toHaveTextContent(/credenciais inválidas/i);
      expect(pushMock).not.toHaveBeenCalled();
    });
  });
});
