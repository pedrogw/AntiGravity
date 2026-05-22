import { AppError } from './AppError';

export class InvalidCredentialsError extends AppError {
  constructor(message: string = 'E-mail ou senha incorretos.') {
    super(message, 'InvalidCredentialsError');
  }
}
