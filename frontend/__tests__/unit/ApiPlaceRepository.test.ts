import { describe, it, expect, vi, beforeEach } from 'vitest';
import { ApiPlaceRepository } from '../../src/infrastructure/repositories/ApiPlaceRepository';
import { Coordinates } from '../../src/domain/value_objects/Coordinates';
import { ApiError } from '../../src/domain/errors/ApiError';
import { NetworkError } from '../../src/domain/errors/NetworkError';
import { AxiosError } from 'axios';

const { apiClient } = vi.hoisted(() => ({
  apiClient: { post: vi.fn(), get: vi.fn() },
}));

vi.mock('../../src/infrastructure/api/api_client', () => ({
  apiClient,
}));

describe('ApiPlaceRepository', () => {
  let repo: ApiPlaceRepository;
  const fakeLocation = new Coordinates({ lat: -23.5, lng: -46.6 });

  beforeEach(() => {
    vi.clearAllMocks();
    repo = new ApiPlaceRepository();
  });

  describe('createFactory', () => {
    it('deve chamar POST /places/factories com name, lat, lng e retornar Factory', async () => {
      apiClient.post.mockResolvedValue({
        data: { id: 'fac-123', name: 'Fabrica Teste', lat: -23.5, lng: -46.6 },
      });

      const factory = await repo.createFactory('Fabrica Teste', fakeLocation);

      expect(apiClient.post).toHaveBeenCalledWith('/places/factories', {
        name: 'Fabrica Teste',
        lat: -23.5,
        lng: -46.6,
      });
      expect(factory.id).toBe('fac-123');
      expect(factory.name).toBe('Fabrica Teste');
      expect(factory.location.lat).toBe(-23.5);
      expect(factory.location.lng).toBe(-46.6);
    });

    it('deve lançar NetworkError quando a requisição falha', async () => {
      apiClient.post.mockRejectedValue(
        new AxiosError('Network error', 'ERR_NETWORK'),
      );

      await expect(
        repo.createFactory('Fabrica Teste', fakeLocation),
      ).rejects.toThrow(NetworkError);
    });

    it('deve propagar erro não-Axios sem alteração', async () => {
      apiClient.post.mockRejectedValue(new Error('Erro genérico'));

      await expect(
        repo.createFactory('Fabrica Teste', fakeLocation),
      ).rejects.toThrow('Erro genérico');
    });

    it('deve lançar ApiError quando recebe HTTP 400', async () => {
      const axiosError = new AxiosError('Bad Request');
      Object.assign(axiosError, {
        response: { status: 400, data: { detail: 'Dado inválido' } },
      });
      apiClient.post.mockRejectedValue(axiosError);

      await expect(
        repo.createFactory('Fabrica Teste', fakeLocation),
      ).rejects.toThrow(ApiError);
    });
  });

  describe('createStore', () => {
    it('deve chamar POST /places/stores com name, lat, lng, owner_id e retornar Store', async () => {
      apiClient.post.mockResolvedValue({
        data: { id: 'sto-456', name: 'Loja Centro', lat: -23.55, lng: -46.63, owner_id: 'owner-1' },
      });

      const store = await repo.createStore('Loja Centro', fakeLocation, 'owner-1');

      expect(apiClient.post).toHaveBeenCalledWith('/places/stores', {
        name: 'Loja Centro',
        lat: -23.5,
        lng: -46.6,
        owner_id: 'owner-1',
      });
      expect(store.id).toBe('sto-456');
      expect(store.name).toBe('Loja Centro');
      expect(store.location.lat).toBe(-23.55);
      expect(store.location.lng).toBe(-46.63);
      expect(store.ownerId).toBe('owner-1');
    });

    it('deve lançar NetworkError quando a requisição falha', async () => {
      apiClient.post.mockRejectedValue(
        new AxiosError('Network error', 'ERR_NETWORK'),
      );

      await expect(
        repo.createStore('Loja Centro', fakeLocation, 'owner-1'),
      ).rejects.toThrow(NetworkError);
    });
  });

  describe('getStoreById', () => {
    it('deve chamar GET /places/stores/{id} e retornar Store', async () => {
      apiClient.get.mockResolvedValue({
        data: { id: 'sto-789', name: 'Loja Teste', lat: -23.55, lng: -46.63, owner_id: 'owner-1' },
      });

      const store = await repo.getStoreById('sto-789');

      expect(apiClient.get).toHaveBeenCalledWith('/places/stores/sto-789');
      expect(store.id).toBe('sto-789');
      expect(store.name).toBe('Loja Teste');
      expect(store.location.lat).toBe(-23.55);
      expect(store.location.lng).toBe(-46.63);
      expect(store.ownerId).toBe('owner-1');
    });

    it('deve lançar NetworkError quando a requisição falha', async () => {
      apiClient.get.mockRejectedValue(
        new AxiosError('Network error', 'ERR_NETWORK'),
      );

      await expect(
        repo.getStoreById('sto-789'),
      ).rejects.toThrow(NetworkError);
    });

    it('deve propagar erro não-Axios sem alteração', async () => {
      apiClient.get.mockRejectedValue(new Error('Erro genérico'));

      await expect(
        repo.getStoreById('sto-789'),
      ).rejects.toThrow('Erro genérico');
    });

    it('deve lançar ApiError quando recebe HTTP 404', async () => {
      const axiosError = new AxiosError('Not Found');
      Object.assign(axiosError, {
        response: { status: 404, data: { detail: 'Loja não encontrada' } },
      });
      apiClient.get.mockRejectedValue(axiosError);

      await expect(
        repo.getStoreById('sto-789'),
      ).rejects.toThrow(ApiError);
    });
  });
});
