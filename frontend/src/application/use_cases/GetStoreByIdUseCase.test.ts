import { describe, it, expect, vi } from 'vitest';
import { GetStoreByIdUseCase } from './GetStoreByIdUseCase';
import { Store } from '../../domain/entities/Place';
import { Coordinates } from '../../domain/value_objects/Coordinates';
import { PlaceRepositoryProtocol } from '../../domain/repositories/PlaceRepositoryProtocol';

describe('GetStoreByIdUseCase', () => {
  it('deve retornar store quando getStoreById resolve', async () => {
    const fakeStore = new Store(
      { name: 'Loja Teste', location: new Coordinates({ lat: -23.5, lng: -46.6 }), ownerId: 'owner-1' },
      'sto-123',
    );
    const mockRepo = { getStoreById: vi.fn().mockResolvedValue(fakeStore) } as unknown as PlaceRepositoryProtocol;
    const useCase = new GetStoreByIdUseCase(mockRepo);

    const result = await useCase.execute('sto-123');

    expect(mockRepo.getStoreById).toHaveBeenCalledWith('sto-123');
    expect(result).toBe(fakeStore);
  });

  it('deve propagar erro quando getStoreById rejeita', async () => {
    const mockRepo = { getStoreById: vi.fn().mockRejectedValue(new Error('Not found')) } as unknown as PlaceRepositoryProtocol;
    const useCase = new GetStoreByIdUseCase(mockRepo);

    await expect(useCase.execute('sto-123')).rejects.toThrow('Not found');
  });
});
