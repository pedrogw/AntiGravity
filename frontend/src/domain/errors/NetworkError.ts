import { AppError } from './AppError';

export class NetworkError extends AppError {
  constructor(message: string = 'Erro de conexão com o servidor') {
    super(message, 'NetworkError');
  }
}
