import { useState, useCallback, useRef, useEffect } from 'react';
import { makeListAlertsUseCase, makeDismissAlertUseCase } from '../infrastructure/di/factories';
import { Alert } from '../domain/entities/Alert';
import { AppError } from '../domain/errors/AppError';

export function useAlerts(pollingInterval = 15000) {
  const [alerts, setAlerts] = useState<Alert[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  const intervalRef = useRef<ReturnType<typeof setInterval> | null>(null);

  const fetchAlerts = useCallback(async (deliveryId?: string) => {
    setIsLoading(true);
    setError('');
    try {
      const useCase = makeListAlertsUseCase();
      const result = await useCase.execute({ deliveryId, limit: 100 });
      setAlerts(result);
    } catch (err) {
      if (err instanceof AppError) {
        setError(err.message);
      } else {
        setError('Erro ao buscar alertas.');
      }
    } finally {
      setIsLoading(false);
    }
  }, []);

  const dismissAlert = useCallback(async (alertId: string) => {
    try {
      const useCase = makeDismissAlertUseCase();
      await useCase.execute({ alertId });
      setAlerts((prev) => prev.filter((a) => a.id !== alertId));
    } catch (err) {
      if (err instanceof AppError) {
        setError(err.message);
      } else {
        setError('Erro ao dispensar alerta.');
      }
    }
  }, []);

  useEffect(() => {
    const timer = setTimeout(() => fetchAlerts(), 0);
    intervalRef.current = setInterval(() => fetchAlerts(), pollingInterval);
    return () => {
      clearTimeout(timer);
      if (intervalRef.current) clearInterval(intervalRef.current);
    };
  }, [fetchAlerts, pollingInterval]);

  const criticalAlerts = alerts.filter((a) => a.isCritical);

  return { alerts, criticalAlerts, isLoading, error, fetchAlerts, dismissAlert };
}
