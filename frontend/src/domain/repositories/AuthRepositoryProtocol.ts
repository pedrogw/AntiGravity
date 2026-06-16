import { User } from '../entities/User';

export interface AuthRepositoryProtocol {
  login(email: string, password: string): Promise<{ user: User; token: string; refresh_token: string }>;
  refreshToken(refresh_token: string): Promise<{ access_token: string; refresh_token: string }>;
  logout(): Promise<void>;
}
