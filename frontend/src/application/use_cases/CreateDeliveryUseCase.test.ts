import { describe, it, expect, vi, beforeEach } from 'vitest';
import { CreateDeliveryUseCase } from './CreateDeliveryUseCase';
import { DeliveryRepositoryProtocol } from '../../domain/repositories/DeliveryRepositoryProtocol';
import { Delivery } from '../../domain/entities/Delivery';

describe('CreateDeliveryUseCase', () => {
  let mockRepo: DeliveryRepositoryProtocol;
  let useCase: CreateDeliveryUseCase;

  beforeEach(() => {
    mockRepo = {
      createDelivery: vi.fn(),
      listDeliveries: vi.fn(),
      updateDelivery: vi.fn(),
    };
    useCase = new CreateDeliveryUseCase(mockRepo);
  });

  it('deve criar uma entrega chamando o repositorio', async () => {
    const mockDelivery = new Delivery({ factoryId: 'f1', storeId: 's1', driverId: 'd1' }, 'del1');
    vi.mocked(mockRepo.createDelivery).mockResolvedValue(mockDelivery);

    const result = await useCase.execute({ factoryId: 'f1', storeId: 's1', driverId: 'd1' });

    expect(mockRepo.createDelivery).toHaveBeenCalledWith('f1', 's1', 'd1');
    expect(result.id).toBe('del1');
  });

  it('deve falhar se inputs não forem providos', async () => {
    await expect(useCase.execute({ factoryId: '', storeId: 's1', driverId: 'd1' }))
      .rejects
      .toThrow('factoryId, storeId e driverId são obrigatórios.');
  });
});
