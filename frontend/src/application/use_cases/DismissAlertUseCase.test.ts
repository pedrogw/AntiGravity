import { describe, it, expect, vi } from 'vitest';
import { DismissAlertUseCase } from './DismissAlertUseCase';
import { AlertRepositoryProtocol } from '../../domain/repositories/AlertRepositoryProtocol';
import { Alert } from '../../domain/entities/Alert';

describe('DismissAlertUseCase', () => {
  it('deve chamar dismiss no repositório e retornar alerta', async () => {
    const mockRepo: AlertRepositoryProtocol = { listAll: vi.fn(), dismiss: vi.fn() };
    const useCase = new DismissAlertUseCase(mockRepo);
    const fakeAlert = new Alert(
      { deliveryId: 'del1', message: 'teste', isCritical: false, createdAt: new Date() },
      'alert1',
    );
    vi.mocked(mockRepo.dismiss).mockResolvedValue(fakeAlert);

    const result = await useCase.execute({ alertId: 'alert1' });

    expect(mockRepo.dismiss).toHaveBeenCalledOnce();
    expect(mockRepo.dismiss).toHaveBeenCalledWith('alert1');
    expect(result.id).toBe('alert1');
  });
});