import { Delivery } from '../entities/Delivery';

export interface DeliveryRepositoryProtocol {
  createDelivery(factoryId: string, storeId: string, driverId: string): Promise<Delivery>;
  listDeliveries(role?: string): Promise<Delivery[]>;
}
