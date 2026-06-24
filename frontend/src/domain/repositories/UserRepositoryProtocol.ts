import { User } from '../entities/User';

export interface UserRepositoryProtocol {
  listDrivers(): Promise<User[]>;
}
