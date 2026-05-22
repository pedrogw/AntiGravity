import { render, screen, waitFor } from '@testing-library/react';
import { AuthGuard } from '../../src/components/AuthGuard';
import { isTokenExpired } from '../../src/utils/jwt';

vi.mock('../../src/utils/jwt', () => ({
  isTokenExpired: vi.fn(),
}));

// Mock next/navigation
const pushMock = vi.fn();
vi.mock('next/navigation', () => ({
  useRouter: () => ({
    push: pushMock,
  }),
}));

describe('Auth Guard Integration', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('deve redirecionar para a raiz (/) se não houver token no localStorage', async () => {
    Storage.prototype.getItem = vi.fn().mockReturnValue(null);

    render(
      <AuthGuard>
        <div data-testid="protected-content">Dashboard Secreto</div>
      </AuthGuard>
    );

    // Ensure it doesn't render children
    expect(screen.queryByTestId('protected-content')).not.toBeInTheDocument();

    // Ensure it called router.push('/')
    await waitFor(() => {
      expect(pushMock).toHaveBeenCalledWith('/');
    });
  });

  it('deve renderizar o conteúdo se houver token no localStorage e não estiver expirado', async () => {
    Storage.prototype.getItem = vi.fn().mockReturnValue('valid_token');
    (isTokenExpired as vi.Mock).mockReturnValue(false);

    render(
      <AuthGuard>
        <div data-testid="protected-content">Dashboard Secreto</div>
      </AuthGuard>
    );

    await waitFor(() => {
      expect(screen.getByTestId('protected-content')).toBeInTheDocument();
      expect(pushMock).not.toHaveBeenCalled();
    });
  });
});
