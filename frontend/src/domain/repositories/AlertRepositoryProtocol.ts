import { Alert } from '../entities/Alert';

export interface AlertRepositoryProtocol {
  listAll(deliveryId?: string, limit?: number, offset?: number): Promise<Alert[]>;
  dismiss(id: string): Promise<Alert>;
}
