import { renderHook, act } from '@testing-library/react';
import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { useAlerts } from './useAlerts';
import { makeListAlertsUseCase } from '../infrastructure/di/factories';
import { ListAlertsUseCase } from '../application/use_cases/ListAlertsUseCase';
import { Alert } from '../domain/entities/Alert';
import { AppError } from '../domain/errors/AppError';

vi.mock('../infrastructure/di/factories', () => ({
  makeListAlertsUseCase: vi.fn(),
}));

describe('useAlerts', () => {
  let mockExecute: ReturnType<typeof vi.fn>;

  const fakeAlert = new Alert(
    { deliveryId: 'del1', message: 'Alerta crítico', isCritical: true, createdAt: new Date() },
    'alert1',
  );

  const fakeNonCritical = new Alert(
    { deliveryId: 'del1', message: 'Alerta info', isCritical: false, createdAt: new Date() },
    'alert2',
  );

  beforeEach(() => {
    vi.clearAllMocks();
    vi.useFakeTimers();
    mockExecute = vi.fn();
    vi.mocked(makeListAlertsUseCase).mockReturnValue({ execute: mockExecute } as unknown as ListAlertsUseCase);
  });

  afterEach(() => {
    vi.useRealTimers();
  });

  it('deve buscar alertas no mount e popular estado', async () => {
    mockExecute.mockResolvedValue([fakeAlert]);

    const { result } = renderHook(() => useAlerts(60000));

    await act(async () => {
      await vi.advanceTimersByTimeAsync(0);
    });

    expect(mockExecute).toHaveBeenCalledOnce();
    expect(result.current.alerts).toHaveLength(1);
    expect(result.current.criticalAlerts).toHaveLength(1);
    expect(result.current.isLoading).toBe(false);
    expect(result.current.error).toBe('');
  });

  it('deve definir mensagem de erro ao receber AppError', async () => {
    mockExecute.mockRejectedValue(new AppError('Erro nos alertas'));

    const { result } = renderHook(() => useAlerts(60000));

    await act(async () => {
      await vi.advanceTimersByTimeAsync(0);
    });

    expect(result.current.error).toBe('Erro nos alertas');
    expect(result.current.isLoading).toBe(false);
    expect(result.current.alerts).toHaveLength(0);
  });

  it('deve definir mensagem generica ao receber erro comum', async () => {
    mockExecute.mockRejectedValue(new Error('erro'));

    const { result } = renderHook(() => useAlerts(60000));

    await act(async () => {
      await vi.advanceTimersByTimeAsync(0);
    });

    expect(result.current.error).toBe('Erro ao buscar alertas.');
    expect(result.current.isLoading).toBe(false);
  });

  it('deve separar alertas críticos dos não críticos', async () => {
    mockExecute.mockResolvedValue([fakeAlert, fakeNonCritical]);

    const { result } = renderHook(() => useAlerts(60000));

    await act(async () => {
      await vi.advanceTimersByTimeAsync(0);
    });

    expect(result.current.alerts).toHaveLength(2);
    expect(result.current.criticalAlerts).toHaveLength(1);
    expect(result.current.criticalAlerts[0].id).toBe('alert1');
  });

  it('deve atualizar erro em polling subsequente', async () => {
    mockExecute
      .mockResolvedValueOnce([fakeAlert])
      .mockRejectedValueOnce(new AppError('Falha no polling'));

    const { result } = renderHook(() => useAlerts(10000));

    await act(async () => {
      await vi.advanceTimersByTimeAsync(0);
    });
    expect(result.current.error).toBe('');

    await act(async () => {
      await vi.advanceTimersByTimeAsync(10000);
    });
    expect(result.current.error).toBe('Falha no polling');
    expect(result.current.isLoading).toBe(false);
  });

  it('deve fazer polling no intervalo configurado', async () => {
    mockExecute.mockResolvedValue([fakeAlert]);

    renderHook(() => useAlerts(10000));

    await act(async () => {
      await vi.advanceTimersByTimeAsync(0);
    });
    expect(mockExecute).toHaveBeenCalledTimes(1);

    await act(async () => {
      await vi.advanceTimersByTimeAsync(10000);
    });
    expect(mockExecute).toHaveBeenCalledTimes(2);

    await act(async () => {
      await vi.advanceTimersByTimeAsync(10000);
    });
    expect(mockExecute).toHaveBeenCalledTimes(3);
  });
});
