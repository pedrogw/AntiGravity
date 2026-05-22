import { useState, useCallback } from 'react';
import { makeListDeliveriesUseCase, makeCreateDeliveryUseCase } from '../infrastructure/di/factories';
import { Delivery } from '../domain/entities/Delivery';
import { AppError } from '../domain/errors/AppError';

export function useDeliveries() {
  const [deliveries, setDeliveries] = useState<Delivery[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

  const fetchDeliveries = useCallback(async (role?: string) => {
    setIsLoading(true);
    setError('');
    try {
      const useCase = makeListDeliveriesUseCase();
      const result = await useCase.execute({ role });
      setDeliveries(result);
    } catch (err) {
      if (err instanceof AppError) {
        setError(err.message);
      } else {
        setError('Erro ao buscar entregas.');
      }
    } finally {
      setIsLoading(false);
    }
  }, []);

  const createDelivery = useCallback(async (factoryId: string, storeId: string, driverId: string) => {
    setIsLoading(true);
    setError('');
    try {
      const useCase = makeCreateDeliveryUseCase();
      const newDelivery = await useCase.execute({ factoryId, storeId, driverId });
      setDeliveries((prev) => [...prev, newDelivery]);
      return newDelivery;
    } catch (err) {
      if (err instanceof AppError) {
        setError(err.message);
      } else {
        setError('Erro ao criar entrega.');
      }
      throw err;
    } finally {
      setIsLoading(false);
    }
  }, []);

  return { deliveries, isLoading, error, fetchDeliveries, createDelivery };
}
