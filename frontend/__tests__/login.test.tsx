import { render, screen } from '@testing-library/react';
import Page from '../src/app/page';

// Mock next/navigation
jest.mock('next/navigation', () => ({
  useRouter: () => ({
    push: jest.fn(),
  }),
}));

describe('Login Gateway (Rota Inicial)', () => {
  it('deve renderizar o formulário de login com campos de email e senha', () => {
    render(<Page />);

    // Verifica a existência do título
    const heading = screen.getByRole('heading', { level: 1, name: /login/i });
    expect(heading).toBeInTheDocument();

    // Verifica a existência do campo de e-mail
    const emailInput = screen.getByLabelText(/e-mail/i);
    expect(emailInput).toBeInTheDocument();
    expect(emailInput).toHaveAttribute('type', 'email');

    // Verifica a existência do campo de senha
    const passwordInput = screen.getByLabelText(/senha/i);
    expect(passwordInput).toBeInTheDocument();
    expect(passwordInput).toHaveAttribute('type', 'password');

    // Verifica a existência do botão de submissão
    const submitButton = screen.getByRole('button', { name: /entrar/i });
    expect(submitButton).toBeInTheDocument();
  });
});
