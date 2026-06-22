import { renderHook, act } from '@testing-library/react';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { usePlaces } from './usePlaces';
import { makeCreateFactoryUseCase, makeCreateStoreUseCase } from '../infrastructure/di/factories';
import { CreateFactoryUseCase } from '../application/use_cases/CreateFactoryUseCase';
import { CreateStoreUseCase } from '../application/use_cases/CreateStoreUseCase';
import { AppError } from '../domain/errors/AppError';

vi.mock('../infrastructure/di/factories', () => ({
  makeCreateFactoryUseCase: vi.fn(),
  makeCreateStoreUseCase: vi.fn(),
}));

describe('usePlaces hook', () => {
  let mockFactoryExecute: ReturnType<typeof vi.fn>;
  let mockStoreExecute: ReturnType<typeof vi.fn>;

  beforeEach(() => {
    vi.clearAllMocks();
    mockFactoryExecute = vi.fn();
    mockStoreExecute = vi.fn();
    vi.mocked(makeCreateFactoryUseCase).mockReturnValue({ execute: mockFactoryExecute } as unknown as CreateFactoryUseCase);
    vi.mocked(makeCreateStoreUseCase).mockReturnValue({ execute: mockStoreExecute } as unknown as CreateStoreUseCase);
  });

  describe('createFactory', () => {
    const fakeLocation = { lat: -23.5, lng: -46.6 };

    it('deve criar fábrica com sucesso', async () => {
      const fakeFactory = { id: 'fac1', name: 'Fabrica Teste', location: fakeLocation };
      mockFactoryExecute.mockResolvedValue(fakeFactory);

      const { result } = renderHook(() => usePlaces());

      let created: unknown;
      await act(async () => {
        created = await result.current.createFactory('Fabrica Teste', fakeLocation);
      });

      expect(mockFactoryExecute).toHaveBeenCalledWith({ name: 'Fabrica Teste', location: fakeLocation });
      expect(created).toEqual(fakeFactory);
      expect(result.current.isLoading).toBe(false);
      expect(result.current.error).toBe('');
    });

    it('deve definir erro e relançar ao receber AppError', async () => {
      mockFactoryExecute.mockRejectedValue(new AppError('Falha na fábrica'));

      const { result } = renderHook(() => usePlaces());

      await act(async () => {
        await expect(result.current.createFactory('Fabrica Teste', fakeLocation)).rejects.toThrow('Falha na fábrica');
      });

      expect(result.current.error).toBe('Falha na fábrica');
      expect(result.current.isLoading).toBe(false);
    });

    it('deve definir erro genérico e relançar ao receber erro comum', async () => {
      mockFactoryExecute.mockRejectedValue(new Error('erro'));

      const { result } = renderHook(() => usePlaces());

      await act(async () => {
        await expect(result.current.createFactory('Fabrica Teste', fakeLocation)).rejects.toThrow('erro');
      });

      expect(result.current.error).toBe('Erro ao criar fábrica.');
      expect(result.current.isLoading).toBe(false);
    });
  });

  describe('createStore', () => {
    const fakeLocation = { lat: -23.5, lng: -46.6 };

    it('deve criar loja com sucesso', async () => {
      const fakeStore = { id: 'sto1', name: 'Loja Teste', location: fakeLocation, ownerId: 'owner1' };
      mockStoreExecute.mockResolvedValue(fakeStore);

      const { result } = renderHook(() => usePlaces());

      let created: unknown;
      await act(async () => {
        created = await result.current.createStore('Loja Teste', fakeLocation, 'owner1');
      });

      expect(mockStoreExecute).toHaveBeenCalledWith({ name: 'Loja Teste', location: fakeLocation, ownerId: 'owner1' });
      expect(created).toEqual(fakeStore);
      expect(result.current.isLoading).toBe(false);
      expect(result.current.error).toBe('');
    });

    it('deve definir erro e relançar ao receber AppError', async () => {
      mockStoreExecute.mockRejectedValue(new AppError('Falha na loja'));

      const { result } = renderHook(() => usePlaces());

      await act(async () => {
        await expect(result.current.createStore('Loja Teste', fakeLocation, 'owner1')).rejects.toThrow('Falha na loja');
      });

      expect(result.current.error).toBe('Falha na loja');
      expect(result.current.isLoading).toBe(false);
    });

    it('deve definir erro genérico e relançar ao receber erro comum', async () => {
      mockStoreExecute.mockRejectedValue(new Error('erro'));

      const { result } = renderHook(() => usePlaces());

      await act(async () => {
        await expect(result.current.createStore('Loja Teste', fakeLocation, 'owner1')).rejects.toThrow('erro');
      });

      expect(result.current.error).toBe('Erro ao criar loja.');
      expect(result.current.isLoading).toBe(false);
    });
  });
});
