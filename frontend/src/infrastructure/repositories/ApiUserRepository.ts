import { UserRepositoryProtocol } from '../../domain/repositories/UserRepositoryProtocol';
import { User, UserRole } from '../../domain/entities/User';
import { ApiError } from '../../domain/errors/ApiError';
import { NetworkError } from '../../domain/errors/NetworkError';
import { apiClient } from '../api/api_client';
import { AxiosError } from 'axios';

interface UserResponse {
  id: string;
  email: string;
  role: UserRole;
  created_at: string;
}

export class ApiUserRepository implements UserRepositoryProtocol {
  async listDrivers(): Promise<User[]> {
    try {
      const { data } = await apiClient.get<UserResponse[]>('/users/drivers');
      return data.map((item) => new User(
        { email: item.email, role: item.role, createdAt: new Date(item.created_at) },
        item.id,
      ));
    } catch (error) {
      if (error instanceof AxiosError) {
        if (error.response) {
          throw new ApiError(error.response.status, error.message);
        }
        throw new NetworkError();
      }
      throw error;
    }
  }
}
