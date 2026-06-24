import { renderHook, act } from '@testing-library/react';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { useUsers } from './useUsers';
import { makeListDriversUseCase } from '../infrastructure/di/factories';
import { ListDriversUseCase } from '../application/use_cases/ListDriversUseCase';
import { User } from '../domain/entities/User';
import { AppError } from '../domain/errors/AppError';

vi.mock('../infrastructure/di/factories', () => ({
  makeListDriversUseCase: vi.fn(),
}));

describe('useUsers hook', () => {
  let mockListExecute: ReturnType<typeof vi.fn>;

  const fakeDriver = new User({ email: 'driver@test.com', role: 'motorista' }, 'user1');

  beforeEach(() => {
    vi.clearAllMocks();
    mockListExecute = vi.fn();
    vi.mocked(makeListDriversUseCase).mockReturnValue({ execute: mockListExecute } as unknown as ListDriversUseCase);
  });

  describe('fetchDrivers', () => {
    it('deve buscar motoristas com sucesso e popular o estado', async () => {
      mockListExecute.mockResolvedValue([fakeDriver]);

      const { result } = renderHook(() => useUsers());

      await act(async () => {
        await result.current.fetchDrivers();
      });

      expect(mockListExecute).toHaveBeenCalledOnce();
      expect(result.current.drivers).toHaveLength(1);
      expect(result.current.drivers[0].id).toBe('user1');
      expect(result.current.isLoading).toBe(false);
      expect(result.current.error).toBe('');
    });

    it('deve definir mensagem de erro ao receber AppError', async () => {
      mockListExecute.mockRejectedValue(new AppError('Erro de teste'));

      const { result } = renderHook(() => useUsers());

      await act(async () => {
        await result.current.fetchDrivers();
      });

      expect(result.current.error).toBe('Erro de teste');
      expect(result.current.isLoading).toBe(false);
      expect(result.current.drivers).toHaveLength(0);
    });

    it('deve definir mensagem generica ao receber erro comum', async () => {
      mockListExecute.mockRejectedValue(new Error('qualquer erro'));

      const { result } = renderHook(() => useUsers());

      await act(async () => {
        await result.current.fetchDrivers();
      });

      expect(result.current.error).toBe('Erro ao buscar motoristas.');
      expect(result.current.isLoading).toBe(false);
    });
  });
});
