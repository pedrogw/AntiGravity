import { UseCase } from './UseCase';
import { User } from '../../domain/entities/User';
import { AuthRepositoryProtocol } from '../../domain/repositories/AuthRepositoryProtocol';
import { TokenStorageProtocol } from '../../domain/repositories/TokenStorageProtocol';

export interface LoginUseCaseInput {
  email: string;
  password: string;
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

    const { user, token, refresh_token } = await this.authRepository.login(input.email, input.password);

    this.tokenStorage.saveToken(token);
    if (refresh_token) {
      this.tokenStorage.saveRefreshToken(refresh_token);
    }

    return user;
  }
}
