import { renderHook, act } from '@testing-library/react';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { usePlaces } from './usePlaces';
import {
  makeCreateFactoryUseCase,
  makeCreateStoreUseCase,
  makeListFactoriesUseCase,
  makeListStoresUseCase,
} from '../infrastructure/di/factories';
import { CreateFactoryUseCase } from '../application/use_cases/CreateFactoryUseCase';
import { CreateStoreUseCase } from '../application/use_cases/CreateStoreUseCase';
import { ListFactoriesUseCase } from '../application/use_cases/ListFactoriesUseCase';
import { ListStoresUseCase } from '../application/use_cases/ListStoresUseCase';
import { AppError } from '../domain/errors/AppError';
import { Factory, Store } from '../domain/entities/Place';
import { Coordinates } from '../domain/value_objects/Coordinates';

vi.mock('../infrastructure/di/factories', () => ({
  makeCreateFactoryUseCase: vi.fn(),
  makeCreateStoreUseCase: vi.fn(),
  makeListFactoriesUseCase: vi.fn(),
  makeListStoresUseCase: vi.fn(),
}));

describe('usePlaces hook', () => {
  let mockFactoryExecute: ReturnType<typeof vi.fn>;
  let mockStoreExecute: ReturnType<typeof vi.fn>;
  let mockListFactoriesExecute: ReturnType<typeof vi.fn>;
  let mockListStoresExecute: ReturnType<typeof vi.fn>;

  beforeEach(() => {
    vi.clearAllMocks();
    mockFactoryExecute = vi.fn();
    mockStoreExecute = vi.fn();
    mockListFactoriesExecute = vi.fn();
    mockListStoresExecute = vi.fn();
    vi.mocked(makeCreateFactoryUseCase).mockReturnValue({ execute: mockFactoryExecute } as unknown as CreateFactoryUseCase);
    vi.mocked(makeCreateStoreUseCase).mockReturnValue({ execute: mockStoreExecute } as unknown as CreateStoreUseCase);
    vi.mocked(makeListFactoriesUseCase).mockReturnValue({ execute: mockListFactoriesExecute } as unknown as ListFactoriesUseCase);
    vi.mocked(makeListStoresUseCase).mockReturnValue({ execute: mockListStoresExecute } as unknown as ListStoresUseCase);
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

  describe('listFactories', () => {
    const fakeFactory = new Factory(
      { name: 'Fabrica 1', location: new Coordinates({ lat: -23.5, lng: -46.6 }) },
      'fac1',
    );

    it('deve listar fabricas com sucesso e popular o estado', async () => {
      mockListFactoriesExecute.mockResolvedValue([fakeFactory]);

      const { result } = renderHook(() => usePlaces());

      await act(async () => {
        await result.current.listFactories();
      });

      expect(mockListFactoriesExecute).toHaveBeenCalledOnce();
      expect(result.current.factories).toHaveLength(1);
      expect(result.current.factories[0].id).toBe('fac1');
      expect(result.current.isLoading).toBe(false);
      expect(result.current.error).toBe('');
    });

    it('deve definir mensagem de erro ao receber AppError', async () => {
      mockListFactoriesExecute.mockRejectedValue(new AppError('Erro nas fabricas'));

      const { result } = renderHook(() => usePlaces());

      await act(async () => {
        await result.current.listFactories();
      });

      expect(result.current.error).toBe('Erro nas fabricas');
      expect(result.current.isLoading).toBe(false);
      expect(result.current.factories).toHaveLength(0);
    });

    it('deve definir mensagem generica ao receber erro comum', async () => {
      mockListFactoriesExecute.mockRejectedValue(new Error('erro'));

      const { result } = renderHook(() => usePlaces());

      await act(async () => {
        await result.current.listFactories();
      });

      expect(result.current.error).toBe('Erro ao buscar fábricas.');
      expect(result.current.isLoading).toBe(false);
    });
  });

  describe('listStores', () => {
    const fakeStore = new Store(
      { name: 'Loja 1', location: new Coordinates({ lat: -23.5, lng: -46.6 }), ownerId: 'owner1' },
      'sto1',
    );

    it('deve listar lojas com sucesso e popular o estado', async () => {
      mockListStoresExecute.mockResolvedValue([fakeStore]);

      const { result } = renderHook(() => usePlaces());

      await act(async () => {
        await result.current.listStores();
      });

      expect(mockListStoresExecute).toHaveBeenCalledOnce();
      expect(result.current.stores).toHaveLength(1);
      expect(result.current.stores[0].id).toBe('sto1');
      expect(result.current.isLoading).toBe(false);
      expect(result.current.error).toBe('');
    });

    it('deve definir mensagem de erro ao receber AppError', async () => {
      mockListStoresExecute.mockRejectedValue(new AppError('Erro nas lojas'));

      const { result } = renderHook(() => usePlaces());

      await act(async () => {
        await result.current.listStores();
      });

      expect(result.current.error).toBe('Erro nas lojas');
      expect(result.current.isLoading).toBe(false);
      expect(result.current.stores).toHaveLength(0);
    });

    it('deve definir mensagem generica ao receber erro comum', async () => {
      mockListStoresExecute.mockRejectedValue(new Error('erro'));

      const { result } = renderHook(() => usePlaces());

      await act(async () => {
        await result.current.listStores();
      });

      expect(result.current.error).toBe('Erro ao buscar lojas.');
      expect(result.current.isLoading).toBe(false);
    });
  });
});
