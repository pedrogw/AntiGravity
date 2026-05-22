import { UseCase } from './UseCase';
import { User } from '../../domain/entities/User';
import { AuthRepositoryProtocol } from '../../domain/repositories/AuthRepositoryProtocol';
import { TokenStorageProtocol } from '../../infrastructure/storage/TokenStorageAdapter';

export interface LoginUseCaseInput {
  email: string;
  password?: string; // opcional para permitir fluxo de SSO no futuro, mas obrigatório aqui
}

export class LoginUseCase implements UseCase<LoginUseCaseInput, User> {
  constructor(
    private authRepository: AuthRepositoryProtocol,
    private tokenStorage: TokenStorageProtocol
  ) {}

  async execute(input: LoginUseCaseInput): Promise<User> {
    if (!input.email || !input.password) {
      throw new Error('E-mail e senha são obrigatórios.');
    }

    const { user, token } = await this.authRepository.login(input.email, input.password);
    
    this.tokenStorage.saveToken(token);
    
    return user;
  }
}
