import { renderHook, act } from '@testing-library/react';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { useAuth } from './useAuth';
import { makeLoginUseCase } from '../infrastructure/di/factories';
import { LoginUseCase } from '../application/use_cases/LoginUseCase';
import { InvalidCredentialsError } from '../domain/errors/InvalidCredentialsError';
import { User } from '../domain/entities/User';

// Mock Next router
const pushMock = vi.fn();
vi.mock('next/navigation', () => ({
  useRouter: () => ({
    push: pushMock,
  }),
}));

// Mock DI factories
vi.mock('../infrastructure/di/factories', () => ({
  makeLoginUseCase: vi.fn(),
}));

describe('useAuth hook', () => {
  let mockExecute: ReturnType<typeof vi.fn>;

  beforeEach(() => {
    vi.clearAllMocks();
    mockExecute = vi.fn();
    vi.mocked(makeLoginUseCase).mockReturnValue({
      execute: mockExecute,
    } as unknown as LoginUseCase);
  });

  it('deve realizar login, não setar erro e redirecionar', async () => {
    const fakeUser = new User({ email: 'test@test.com', role: 'lojista' }, '1');
    mockExecute.mockResolvedValue(fakeUser);

    const { result } = renderHook(() => useAuth());

    await act(async () => {
      await result.current.login('test@test.com', 'password');
    });

    expect(mockExecute).toHaveBeenCalledWith({ email: 'test@test.com', password: 'password' });
    expect(result.current.error).toBe('');
    expect(result.current.isLoading).toBe(false);
    expect(pushMock).toHaveBeenCalledWith('/dashboard'); // lojista goes to /dashboard
  });

  it('deve definir mensagem de erro amigável ao receber InvalidCredentialsError', async () => {
    mockExecute.mockRejectedValue(new InvalidCredentialsError());

    const { result } = renderHook(() => useAuth());

    await act(async () => {
      await result.current.login('wrong@test.com', 'wrong');
    });

    expect(result.current.error).toBe('E-mail ou senha incorretos.');
    expect(result.current.isLoading).toBe(false);
    expect(pushMock).not.toHaveBeenCalled();
  });
});
