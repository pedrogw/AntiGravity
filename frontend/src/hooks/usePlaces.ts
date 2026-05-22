import { useState, useCallback } from 'react';
import { makeCreateFactoryUseCase, makeCreateStoreUseCase } from '../infrastructure/di/factories';
import { Factory, Store } from '../domain/entities/Place';
import { AppError } from '../domain/errors/AppError';
import { CoordinatesProps } from '../domain/value_objects/Coordinates';

export function usePlaces() {
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

  const createFactory = useCallback(async (name: string, location: CoordinatesProps) => {
    setIsLoading(true);
    setError('');
    try {
      const useCase = makeCreateFactoryUseCase();
      return await useCase.execute({ name, location });
    } catch (err) {
      if (err instanceof AppError) {
        setError(err.message);
      } else {
        setError('Erro ao criar fábrica.');
      }
      throw err;
    } finally {
      setIsLoading(false);
    }
  }, []);

  const createStore = useCallback(async (name: string, location: CoordinatesProps, ownerId: string) => {
    setIsLoading(true);
    setError('');
    try {
      const useCase = makeCreateStoreUseCase();
      return await useCase.execute({ name, location, ownerId });
    } catch (err) {
      if (err instanceof AppError) {
        setError(err.message);
      } else {
        setError('Erro ao criar loja.');
      }
      throw err;
    } finally {
      setIsLoading(false);
    }
  }, []);

  return { isLoading, error, createFactory, createStore };
}
