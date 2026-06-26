import { UseCase } from './UseCase';
import { Alert } from '../../domain/entities/Alert';
import { AlertRepositoryProtocol } from '../../domain/repositories/AlertRepositoryProtocol';

export interface DismissAlertInput {
  alertId: string;
}

export class DismissAlertUseCase implements UseCase<DismissAlertInput, Alert> {
  constructor(private alertRepository: AlertRepositoryProtocol) {}

  async execute(input: DismissAlertInput): Promise<Alert> {
    return await this.alertRepository.dismiss(input.alertId);
  }
}