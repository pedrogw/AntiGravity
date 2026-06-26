import { describe, it, expect, vi, beforeEach } from 'vitest';
import { ListStoresUseCase } from './ListStoresUseCase';
import { PlaceRepositoryProtocol } from '../../domain/repositories/PlaceRepositoryProtocol';
import { Store } from '../../domain/entities/Place';
import { Coordinates } from '../../domain/value_objects/Coordinates';

describe('ListStoresUseCase', () => {
  let mockRepo: PlaceRepositoryProtocol;
  let useCase: ListStoresUseCase;

  beforeEach(() => {
    mockRepo = {
      createFactory: vi.fn(),
      createStore: vi.fn(),
      listFactories: vi.fn(),
      listStores: vi.fn(),
      getStoreById: vi.fn(),
    };
    useCase = new ListStoresUseCase(mockRepo);
  });

  it('deve listar lojas chamando o repositorio', async () => {
    const mockStore = new Store(
      { name: 'Loja 1', location: new Coordinates({ lat: -23.5, lng: -46.6 }), ownerId: 'owner1' },
      'sto1',
    );
    vi.mocked(mockRepo.listStores).mockResolvedValue([mockStore]);

    const result = await useCase.execute();

    expect(mockRepo.listStores).toHaveBeenCalledOnce();
    expect(result).toHaveLength(1);
    expect(result[0].id).toBe('sto1');
    expect(result[0].name).toBe('Loja 1');
    expect(result[0].ownerId).toBe('owner1');
  });

  it('deve retornar lista vazia se nao houver lojas', async () => {
    vi.mocked(mockRepo.listStores).mockResolvedValue([]);

    const result = await useCase.execute();

    expect(result).toEqual([]);
  });
});
