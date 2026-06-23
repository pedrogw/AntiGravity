import { useState, useCallback } from 'react';
import { makeListDeliveriesUseCase, makeCreateDeliveryUseCase, makeUpdateDeliveryUseCase } from '../infrastructure/di/factories';
import { Delivery } from '../domain/entities/Delivery';
import { DeliveryStatus } from '../domain/DeliveryStatus';
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

  const updateDeliveryStatus = useCallback(async (deliveryId: string, status: DeliveryStatus) => {
    setError('');
    try {
      const useCase = makeUpdateDeliveryUseCase();
      const updated = await useCase.execute({ deliveryId, data: { status } });
      setDeliveries((prev) => prev.map((d) => (d.id === deliveryId ? updated : d)));
      return updated;
    } catch (err) {
      if (err instanceof AppError) {
        setError(err.message);
      } else {
        setError('Erro ao atualizar entrega.');
      }
      throw err;
    }
  }, []);

  return { deliveries, isLoading, error, fetchDeliveries, createDelivery, updateDeliveryStatus };
}
