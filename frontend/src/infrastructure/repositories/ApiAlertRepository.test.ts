import { describe, it, expect, vi, beforeEach } from 'vitest';
import { ApiAlertRepository } from './ApiAlertRepository';
import { apiClient } from '../api/api_client';

vi.mock('../api/api_client', () => ({
  apiClient: {
    get: vi.fn(),
  },
}));

describe('ApiAlertRepository', () => {
  let repo: ApiAlertRepository;

  beforeEach(() => {
    vi.clearAllMocks();
    repo = new ApiAlertRepository();
  });

  it('deve chamar GET /alerts sem parametros', async () => {
    vi.mocked(apiClient.get).mockResolvedValue({ data: [] });

    await repo.listAll();

    expect(apiClient.get).toHaveBeenCalledWith('/alerts', {
      params: { limit: 50, offset: 0 },
    });
  });

  it('deve passar delivery_id, limit e offset como query params', async () => {
    vi.mocked(apiClient.get).mockResolvedValue({ data: [] });

    await repo.listAll('del1', 10, 20);

    expect(apiClient.get).toHaveBeenCalledWith('/alerts', {
      params: { delivery_id: 'del1', limit: 10, offset: 20 },
    });
  });

  it('deve mapear resposta da API para entidade Alert', async () => {
    vi.mocked(apiClient.get).mockResolvedValue({
      data: [
        {
          id: 'alert1',
          delivery_id: 'del1',
          message: 'Alerta de teste',
          is_critical: true,
          created_at: '2026-06-25T10:00:00Z',
        },
      ],
    });

    const result = await repo.listAll();

    expect(result).toHaveLength(1);
    expect(result[0].id).toBe('alert1');
    expect(result[0].deliveryId).toBe('del1');
    expect(result[0].message).toBe('Alerta de teste');
    expect(result[0].isCritical).toBe(true);
    expect(result[0].createdAt).toBeInstanceOf(Date);
  });

  it('deve retornar lista vazia quando API retorna array vazio', async () => {
    vi.mocked(apiClient.get).mockResolvedValue({ data: [] });

    const result = await repo.listAll();

    expect(result).toEqual([]);
  });
});
