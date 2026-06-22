import { renderHook, act } from '@testing-library/react';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { useDeliveries } from './useDeliveries';
import { makeListDeliveriesUseCase, makeCreateDeliveryUseCase, makeUpdateDeliveryUseCase } from '../infrastructure/di/factories';
import { ListDeliveriesUseCase } from '../application/use_cases/ListDeliveriesUseCase';
import { CreateDeliveryUseCase } from '../application/use_cases/CreateDeliveryUseCase';
import { UpdateDeliveryUseCase } from '../application/use_cases/UpdateDeliveryUseCase';
import { Delivery } from '../domain/entities/Delivery';
import { AppError } from '../domain/errors/AppError';

vi.mock('../infrastructure/di/factories', () => ({
  makeListDeliveriesUseCase: vi.fn(),
  makeCreateDeliveryUseCase: vi.fn(),
  makeUpdateDeliveryUseCase: vi.fn(),
}));

describe('useDeliveries hook', () => {
  let mockListExecute: ReturnType<typeof vi.fn>;
  let mockCreateExecute: ReturnType<typeof vi.fn>;
  let mockUpdateExecute: ReturnType<typeof vi.fn>;

  const fakeDelivery = new Delivery({ factoryId: 'f1', storeId: 's1', driverId: 'd1' }, 'del1');

  beforeEach(() => {
    vi.clearAllMocks();
    mockListExecute = vi.fn();
    mockCreateExecute = vi.fn();
    mockUpdateExecute = vi.fn();
    vi.mocked(makeListDeliveriesUseCase).mockReturnValue({ execute: mockListExecute } as unknown as ListDeliveriesUseCase);
    vi.mocked(makeCreateDeliveryUseCase).mockReturnValue({ execute: mockCreateExecute } as unknown as CreateDeliveryUseCase);
    vi.mocked(makeUpdateDeliveryUseCase).mockReturnValue({ execute: mockUpdateExecute } as unknown as UpdateDeliveryUseCase);
  });

  describe('fetchDeliveries', () => {
    it('deve buscar entregas com sucesso e popular o estado', async () => {
      mockListExecute.mockResolvedValue([fakeDelivery]);

      const { result } = renderHook(() => useDeliveries());

      await act(async () => {
        await result.current.fetchDeliveries();
      });

      expect(mockListExecute).toHaveBeenCalledWith({ role: undefined });
      expect(result.current.deliveries).toHaveLength(1);
      expect(result.current.deliveries[0].id).toBe('del1');
      expect(result.current.isLoading).toBe(false);
      expect(result.current.error).toBe('');
    });

    it('deve passar a role para o use case', async () => {
      mockListExecute.mockResolvedValue([]);

      const { result } = renderHook(() => useDeliveries());

      await act(async () => {
        await result.current.fetchDeliveries('motorista');
      });

      expect(mockListExecute).toHaveBeenCalledWith({ role: 'motorista' });
    });

    it('deve definir mensagem de erro ao receber AppError', async () => {
      mockListExecute.mockRejectedValue(new AppError('Erro de teste'));

      const { result } = renderHook(() => useDeliveries());

      await act(async () => {
        await result.current.fetchDeliveries();
      });

      expect(result.current.error).toBe('Erro de teste');
      expect(result.current.isLoading).toBe(false);
      expect(result.current.deliveries).toHaveLength(0);
    });

    it('deve definir mensagem genérica ao receber erro não-AppError', async () => {
      mockListExecute.mockRejectedValue(new Error('qualquer erro'));

      const { result } = renderHook(() => useDeliveries());

      await act(async () => {
        await result.current.fetchDeliveries();
      });

      expect(result.current.error).toBe('Erro ao buscar entregas.');
      expect(result.current.isLoading).toBe(false);
    });
  });

  describe('createDelivery', () => {
    it('deve criar entrega e adicionar à lista', async () => {
      mockCreateExecute.mockResolvedValue(fakeDelivery);

      const { result } = renderHook(() => useDeliveries());

      let created: Delivery | undefined;
      await act(async () => {
        created = await result.current.createDelivery('f1', 's1', 'd1');
      });

      expect(mockCreateExecute).toHaveBeenCalledWith({ factoryId: 'f1', storeId: 's1', driverId: 'd1' });
      expect(result.current.deliveries).toHaveLength(1);
      expect(result.current.deliveries[0].id).toBe('del1');
      expect(created?.id).toBe('del1');
      expect(result.current.isLoading).toBe(false);
    });

    it('deve definir erro e relançar ao receber AppError', async () => {
      mockCreateExecute.mockRejectedValue(new AppError('Falha na criação'));

      const { result } = renderHook(() => useDeliveries());

      await act(async () => {
        await expect(result.current.createDelivery('f1', 's1', 'd1')).rejects.toThrow('Falha na criação');
      });

      expect(result.current.error).toBe('Falha na criação');
      expect(result.current.isLoading).toBe(false);
    });

    it('deve definir erro genérico e relançar ao receber erro comum', async () => {
      mockCreateExecute.mockRejectedValue(new Error('erro'));

      const { result } = renderHook(() => useDeliveries());

      await act(async () => {
        await expect(result.current.createDelivery('f1', 's1', 'd1')).rejects.toThrow('erro');
      });

      expect(result.current.error).toBe('Erro ao criar entrega.');
      expect(result.current.isLoading).toBe(false);
    });
  });

  describe('updateDeliveryStatus', () => {
    it('deve atualizar status e modificar o item na lista', async () => {
      const updatedDelivery = new Delivery({ factoryId: 'f1', storeId: 's1', driverId: 'd1', status: 'em_transito' }, 'del1');
      mockListExecute.mockResolvedValue([fakeDelivery]);
      mockUpdateExecute.mockResolvedValue(updatedDelivery);

      const { result } = renderHook(() => useDeliveries());

      await act(async () => {
        await result.current.fetchDeliveries();
      });
      expect(result.current.deliveries[0].status).toBe('pendente');

      await act(async () => {
        const updated = await result.current.updateDeliveryStatus('del1', 'em_transito');
        expect(updated.status).toBe('em_transito');
      });

      expect(mockUpdateExecute).toHaveBeenCalledWith({ deliveryId: 'del1', data: { status: 'em_transito' } });
      expect(result.current.deliveries[0].status).toBe('em_transito');
    });

    it('deve definir erro e relançar ao receber AppError no update', async () => {
      mockUpdateExecute.mockRejectedValue(new AppError('Falha no update'));

      const { result } = renderHook(() => useDeliveries());

      await act(async () => {
        await expect(result.current.updateDeliveryStatus('del1', 'em_transito')).rejects.toThrow('Falha no update');
      });

      expect(result.current.error).toBe('Falha no update');
    });

    it('deve definir erro genérico e relançar ao receber erro comum no update', async () => {
      mockUpdateExecute.mockRejectedValue(new Error('erro'));

      const { result } = renderHook(() => useDeliveries());

      await act(async () => {
        await expect(result.current.updateDeliveryStatus('del1', 'em_transito')).rejects.toThrow('erro');
      });

      expect(result.current.error).toBe('Erro ao atualizar entrega.');
    });
  });
});
