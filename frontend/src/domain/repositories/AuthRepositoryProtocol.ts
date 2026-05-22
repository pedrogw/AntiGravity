import { User } from '../entities/User';

export interface AuthRepositoryProtocol {
  login(email: string, password: string): Promise<{ user: User; token: string }>;
  logout(): Promise<void>;
  // Opcionalmente podemos ter 'register' se necessário, mas focamos no fluxo básico
}
