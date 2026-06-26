import { describe, it, expect, vi, beforeEach } from 'vitest';
import { ListFactoriesUseCase } from './ListFactoriesUseCase';
import { PlaceRepositoryProtocol } from '../../domain/repositories/PlaceRepositoryProtocol';
import { Factory } from '../../domain/entities/Place';
import { Coordinates } from '../../domain/value_objects/Coordinates';

describe('ListFactoriesUseCase', () => {
  let mockRepo: PlaceRepositoryProtocol;
  let useCase: ListFactoriesUseCase;

  beforeEach(() => {
    mockRepo = {
      createFactory: vi.fn(),
      createStore: vi.fn(),
      listFactories: vi.fn(),
      listStores: vi.fn(),
      getStoreById: vi.fn(),
    };
    useCase = new ListFactoriesUseCase(mockRepo);
  });

  it('deve listar fabricas chamando o repositorio', async () => {
    const mockFactory = new Factory(
      { name: 'Fabrica 1', location: new Coordinates({ lat: -23.5, lng: -46.6 }) },
      'fac1',
    );
    vi.mocked(mockRepo.listFactories).mockResolvedValue([mockFactory]);

    const result = await useCase.execute();

    expect(mockRepo.listFactories).toHaveBeenCalledOnce();
    expect(result).toHaveLength(1);
    expect(result[0].id).toBe('fac1');
    expect(result[0].name).toBe('Fabrica 1');
  });

  it('deve retornar lista vazia se nao houver fabricas', async () => {
    vi.mocked(mockRepo.listFactories).mockResolvedValue([]);

    const result = await useCase.execute();

    expect(result).toEqual([]);
  });
});
