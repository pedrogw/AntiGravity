import { DeliveryRepositoryProtocol } from '../../domain/repositories/DeliveryRepositoryProtocol';
import { Delivery } from '../../domain/entities/Delivery';

export class ApiDeliveryRepository implements DeliveryRepositoryProtocol {
  async createDelivery(factoryId: string, storeId: string, driverId: string): Promise<Delivery> {
    // Mock implementation for now
    return new Delivery({ factoryId, storeId, driverId });
  }

  async listDeliveries(role?: string): Promise<Delivery[]> {
    // Mock implementation for now
    return [];
  }
}
