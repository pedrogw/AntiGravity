import { describe, it, expect, vi, beforeEach } from 'vitest';
import { LogoutUseCase } from './LogoutUseCase';
import { AuthRepositoryProtocol } from '../../domain/repositories/AuthRepositoryProtocol';
import { TokenStorageProtocol } from '../../domain/repositories/TokenStorageProtocol';

describe('LogoutUseCase', () => {
  let mockAuthRepo: AuthRepositoryProtocol;
  let mockTokenStorage: TokenStorageProtocol;
  let useCase: LogoutUseCase;

  beforeEach(() => {
    mockAuthRepo = {
      login: vi.fn(),
      logout: vi.fn().mockResolvedValue(undefined),
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
    useCase = new LogoutUseCase(mockAuthRepo, mockTokenStorage);
  });

  it('deve realizar logout chamando repositório e removendo o token do storage', async () => {
    await useCase.execute();

    expect(mockAuthRepo.logout).toHaveBeenCalled();
    expect(mockTokenStorage.clearTokens).toHaveBeenCalled();
  });
});
