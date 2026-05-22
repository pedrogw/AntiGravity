import { AppError } from './AppError';

export class ValidationError extends AppError {
  constructor(message: string = 'Erro de validação nos dados fornecidos') {
    super(message, 'ValidationError');
  }
}
