import { useState, useCallback } from 'react';
import { useRouter } from 'next/navigation';
import { makeLoginUseCase } from '../infrastructure/di/factories';
import { getRouteByRole } from '../lib/routes';
import { AppError } from '../domain/errors/AppError';

export function useAuth() {
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  const router = useRouter();

  const login = useCallback(async (email: string, password: string) => {
    setIsLoading(true);
    setError('');

    try {
      const loginUseCase = makeLoginUseCase();
      const user = await loginUseCase.execute({ email, password });
      
      const destination = getRouteByRole(user.role);
      router.push(destination);

    } catch (err) {
      if (err instanceof AppError) {
        setError(err.message);
      } else {
        setError('Ocorreu um erro inesperado.');
      }
    } finally {
      setIsLoading(false);
    }
  }, [router]);

  return { login, isLoading, error };
}
