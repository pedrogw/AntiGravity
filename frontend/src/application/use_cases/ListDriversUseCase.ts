import { UseCase } from './UseCase';
import { User } from '../../domain/entities/User';
import { UserRepositoryProtocol } from '../../domain/repositories/UserRepositoryProtocol';

export class ListDriversUseCase implements UseCase<void, User[]> {
  constructor(private userRepository: UserRepositoryProtocol) {}

  async execute(): Promise<User[]> {
    return await this.userRepository.listDrivers();
  }
}
