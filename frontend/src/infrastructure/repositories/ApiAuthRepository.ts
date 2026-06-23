import { AuthRepositoryProtocol } from '../../domain/repositories/AuthRepositoryProtocol';
import { User, UserProps } from '../../domain/entities/User';
import { InvalidCredentialsError } from '../../domain/errors/InvalidCredentialsError';
import { NetworkError } from '../../domain/errors/NetworkError';
import { apiClient } from '../api/api_client';
import { AxiosError } from 'axios';

export class ApiAuthRepository implements AuthRepositoryProtocol {
  async login(email: string, password: string): Promise<{ user: User; token: string; refresh_token: string }> {
    try {
      const response = await apiClient.post('/auth/login', { email, password });
      
      const { user: userData, token, refresh_token } = response.data;
      
      const userProps: UserProps = {
        email: userData.email,
        role: userData.role,
        createdAt: userData.created_at ? new Date(userData.created_at) : undefined,
      };

      const user = new User(userProps, userData.id);
      
      return { user, token: token || response.data.access_token, refresh_token: refresh_token || response.data.refresh_token };
    } catch (error) {
      if (error instanceof AxiosError) {
        if (error.response?.status === 401 || error.response?.status === 400) {
          throw new InvalidCredentialsError();
        }
      }
      throw new NetworkError();
    }
  }

  async refreshToken(refresh_token: string): Promise<{ access_token: string; refresh_token: string }> {
    try {
      const response = await apiClient.post('/auth/refresh', { refresh_token });
      return response.data;
    } catch (error) {
      if (error instanceof AxiosError) {
        if (error.response?.status === 401) {
          throw new InvalidCredentialsError('Sessão expirada. Faça login novamente.');
        }
      }
      throw new NetworkError();
    }
  }

  async logout(): Promise<void> {
    return Promise.resolve();
  }
}
