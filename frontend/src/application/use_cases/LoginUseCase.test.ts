import { describe, it, expect, vi, beforeEach } from 'vitest';
import { LoginUseCase } from './LoginUseCase';
import { AuthRepositoryProtocol } from '../../domain/repositories/AuthRepositoryProtocol';
import { TokenStorageProtocol } from '../../domain/repositories/TokenStorageProtocol';
import { User } from '../../domain/entities/User';
import { InvalidCredentialsError } from '../../domain/errors/InvalidCredentialsError';

describe('LoginUseCase', () => {
  let mockAuthRepo: AuthRepositoryProtocol;
  let mockTokenStorage: TokenStorageProtocol;
  let useCase: LoginUseCase;

  beforeEach(() => {
    mockAuthRepo = {
      login: vi.fn(),
      logout: vi.fn(),
      refreshToken: vi.fn(),
    };
    mockTokenStorage = {
      saveToken: vi.fn(),
      getToken: vi.fn(),
      removeToken: vi.fn(),
      getRefreshToken: vi.fn(),
      saveRefreshToken: vi.fn(),
      clearTokens: vi.fn(),
    };
    useCase = new LoginUseCase(mockAuthRepo, mockTokenStorage);
  });

  it('deve realizar login com sucesso e salvar o token', async () => {
    const mockUser = new User({ email: 'test@test.com', role: 'lojista' }, 'user-id');
    const mockToken = 'mock-jwt-token';
    
    vi.mocked(mockAuthRepo.login).mockResolvedValue({ user: mockUser, token: mockToken, refresh_token: 'mock-refresh-token' });

    const result = await useCase.execute({ email: 'test@test.com', password: 'password123' });

    expect(mockAuthRepo.login).toHaveBeenCalledWith('test@test.com', 'password123');
    expect(mockTokenStorage.saveToken).toHaveBeenCalledWith(mockToken);
    expect(result.id).toBe('user-id');
    expect(result.email).toBe('test@test.com');
  });

  it('deve propagar o erro se o repositório falhar (ex: InvalidCredentialsError)', async () => {
    vi.mocked(mockAuthRepo.login).mockRejectedValue(new InvalidCredentialsError());

    await expect(useCase.execute({ email: 'wrong@test.com', password: 'wrong' }))
      .rejects
      .toThrow(InvalidCredentialsError);

    expect(mockTokenStorage.saveToken).not.toHaveBeenCalled();
  });
});
