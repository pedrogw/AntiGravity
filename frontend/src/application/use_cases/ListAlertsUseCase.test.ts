import { describe, it, expect, vi, beforeEach } from 'vitest';
import { ListAlertsUseCase } from './ListAlertsUseCase';
import { AlertRepositoryProtocol } from '../../domain/repositories/AlertRepositoryProtocol';
import { Alert } from '../../domain/entities/Alert';

describe('ListAlertsUseCase', () => {
  let mockRepo: AlertRepositoryProtocol;
  let useCase: ListAlertsUseCase;

  const fakeAlert = new Alert(
    { deliveryId: 'del1', message: 'Alerta crítico', isCritical: true, createdAt: new Date() },
    'alert1',
  );

  beforeEach(() => {
    mockRepo = { listAll: vi.fn() };
    useCase = new ListAlertsUseCase(mockRepo);
  });

  it('deve listar alertas com sucesso', async () => {
    vi.mocked(mockRepo.listAll).mockResolvedValue([fakeAlert]);

    const result = await useCase.execute();

    expect(mockRepo.listAll).toHaveBeenCalledOnce();
    expect(result).toHaveLength(1);
    expect(result[0].id).toBe('alert1');
    expect(result[0].isCritical).toBe(true);
  });

  it('deve passar delivery_id, limit e offset quando fornecidos', async () => {
    vi.mocked(mockRepo.listAll).mockResolvedValue([]);

    await useCase.execute({ deliveryId: 'del1', limit: 10, offset: 20 });

    expect(mockRepo.listAll).toHaveBeenCalledWith('del1', 10, 20);
  });

  it('deve retornar lista vazia quando não há alertas', async () => {
    vi.mocked(mockRepo.listAll).mockResolvedValue([]);

    const result = await useCase.execute();

    expect(result).toEqual([]);
  });
});
