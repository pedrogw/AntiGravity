import { useState, useCallback } from 'react';
import {
  makeCreateFactoryUseCase,
  makeCreateStoreUseCase,
  makeListFactoriesUseCase,
  makeListStoresUseCase,
  makeGetStoreByIdUseCase,
} from '../infrastructure/di/factories';

import { AppError } from '../domain/errors/AppError';
import { CoordinatesProps } from '../domain/value_objects/Coordinates';
import { Factory, Store } from '../domain/entities/Place';

export function usePlaces() {
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  const [factories, setFactories] = useState<Factory[]>([]);
  const [stores, setStores] = useState<Store[]>([]);

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

  const listFactories = useCallback(async () => {
    setIsLoading(true);
    setError('');
    try {
      const useCase = makeListFactoriesUseCase();
      const result = await useCase.execute();
      setFactories(result);
    } catch (err) {
      if (err instanceof AppError) {
        setError(err.message);
      } else {
        setError('Erro ao buscar fábricas.');
      }
    } finally {
      setIsLoading(false);
    }
  }, []);

  const listStores = useCallback(async () => {
    setIsLoading(true);
    setError('');
    try {
      const useCase = makeListStoresUseCase();
      const result = await useCase.execute();
      setStores(result);
    } catch (err) {
      if (err instanceof AppError) {
        setError(err.message);
      } else {
        setError('Erro ao buscar lojas.');
      }
    } finally {
      setIsLoading(false);
    }
  }, []);

  const fetchStoreById = useCallback(async (id: string) => {
    setIsLoading(true);
    setError('');
    try {
      const useCase = makeGetStoreByIdUseCase();
      return await useCase.execute(id);
    } catch (err) {
      if (err instanceof AppError) {
        setError(err.message);
      } else {
        setError('Erro ao buscar loja.');
      }
      throw err;
    } finally {
      setIsLoading(false);
    }
  }, []);

  return { isLoading, error, createFactory, createStore, factories, stores, listFactories, listStores, fetchStoreById };
}
