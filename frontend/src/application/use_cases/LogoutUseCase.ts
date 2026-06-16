import { UseCase } from './UseCase';
import { AuthRepositoryProtocol } from '../../domain/repositories/AuthRepositoryProtocol';
import { TokenStorageProtocol } from '../../infrastructure/storage/TokenStorageAdapter';

export class LogoutUseCase implements UseCase<void, void> {
  constructor(
    private authRepository: AuthRepositoryProtocol,
    private tokenStorage: TokenStorageProtocol
  ) {}

  async execute(): Promise<void> {
    // 1. Invalida no backend (se houver implementação)
    await this.authRepository.logout();
    
    // 2. Remove tokens locais
    this.tokenStorage.clearTokens();
  }
}
