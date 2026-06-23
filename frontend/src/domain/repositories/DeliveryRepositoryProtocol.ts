import { Delivery } from '../entities/Delivery';
import { DeliveryStatus } from '../DeliveryStatus';

export interface UpdateDeliveryData {
  status?: DeliveryStatus;
  lat?: number;
  lng?: number;
}

export interface DeliveryRepositoryProtocol {
  createDelivery(factoryId: string, storeId: string, driverId: string): Promise<Delivery>;
  listDeliveries(role?: string, limit?: number, offset?: number): Promise<Delivery[]>;
  updateDelivery(id: string, data: UpdateDeliveryData): Promise<Delivery>;
}
