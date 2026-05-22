import { AuthRepositoryProtocol } from '../../domain/repositories/AuthRepositoryProtocol';
import { User, UserProps } from '../../domain/entities/User';
import { InvalidCredentialsError } from '../../domain/errors/InvalidCredentialsError';
import { NetworkError } from '../../domain/errors/NetworkError';
import { apiClient } from '../api/api_client';
import { AxiosError } from 'axios';

export class ApiAuthRepository implements AuthRepositoryProtocol {
  async login(email: string, password: string): Promise<{ user: User; token: string }> {
    try {
      const response = await apiClient.post('/api/v1/auth/login', { email, password });
      
      const { user: userData, token } = response.data;
      
      const userProps: UserProps = {
        email: userData.email,
        role: userData.role,
        createdAt: userData.created_at ? new Date(userData.created_at) : undefined,
      };

      const user = new User(userProps, userData.id);
      
      return { user, token };
    } catch (error) {
      if (error instanceof AxiosError) {
        if (error.response?.status === 401 || error.response?.status === 400) {
          throw new InvalidCredentialsError();
        }
      }
      throw new NetworkError();
    }
  }

  async logout(): Promise<void> {
    // Pode chamar endpoint do backend para invalidar sessão, se houver
    return Promise.resolve();
  }
}
