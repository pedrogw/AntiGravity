import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { apiClient } from '../infrastructure/api/api_client';
import { getRouteByRole } from '../use_cases/getRouteByRole';

export function useAuth() {
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  const router = useRouter();

  const login = async (email: string, password: string) => {
    setIsLoading(true);
    setError('');

    try {
      const response = await apiClient.post('/auth/login', { email, password });
      
      const { access_token, role } = response.data;
      
      if (typeof window !== 'undefined') {
        localStorage.setItem('token', access_token);
      }

      const destination = getRouteByRole(role);
      router.push(destination);

    } catch (err) {
      setError('Credenciais inválidas');
    } finally {
      setIsLoading(false);
    }
  };

  return { login, isLoading, error };
}
