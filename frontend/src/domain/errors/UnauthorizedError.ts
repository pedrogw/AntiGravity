import { AppError } from './AppError';

export class UnauthorizedError extends AppError {
  constructor(message: string = 'Acesso não autorizado ou credenciais inválidas') {
    super(message, 'UnauthorizedError');
  }
}
