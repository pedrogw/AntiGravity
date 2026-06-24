import { useState, useCallback } from 'react';
import { makeListDriversUseCase } from '../infrastructure/di/factories';
import { User } from '../domain/entities/User';
import { AppError } from '../domain/errors/AppError';

export function useUsers() {
  const [drivers, setDrivers] = useState<User[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

  const fetchDrivers = useCallback(async () => {
    setIsLoading(true);
    setError('');
    try {
      const useCase = makeListDriversUseCase();
      const result = await useCase.execute();
      setDrivers(result);
    } catch (err) {
      if (err instanceof AppError) {
        setError(err.message);
      } else {
        setError('Erro ao buscar motoristas.');
      }
    } finally {
      setIsLoading(false);
    }
  }, []);

  return { drivers, isLoading, error, fetchDrivers };
}
