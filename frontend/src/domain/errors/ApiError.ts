import { AppError } from './AppError';

export class ApiError extends AppError {
  public readonly statusCode: number;

  constructor(statusCode: number, message: string = 'Erro na requisição') {
    super(message, 'ApiError');
    this.statusCode = statusCode;
  }
}
