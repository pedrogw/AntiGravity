import { UseCase } from './UseCase';
import { Alert } from '../../domain/entities/Alert';
import { AlertRepositoryProtocol } from '../../domain/repositories/AlertRepositoryProtocol';

export interface ListAlertsInput {
  deliveryId?: string;
  limit?: number;
  offset?: number;
}

export class ListAlertsUseCase implements UseCase<ListAlertsInput, Alert[]> {
  constructor(private alertRepository: AlertRepositoryProtocol) {}

  async execute(input: ListAlertsInput = {}): Promise<Alert[]> {
    return await this.alertRepository.listAll(input.deliveryId, input.limit, input.offset);
  }
}
