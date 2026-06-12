import { Delivery } from '../entities/Delivery';

export interface UpdateDeliveryData {
  status?: string;
  lat?: number;
  lng?: number;
}

export interface DeliveryRepositoryProtocol {
  createDelivery(factoryId: string, storeId: string, driverId: string): Promise<Delivery>;
  listDeliveries(role?: string, limit?: number, offset?: number): Promise<Delivery[]>;
  updateDelivery(id: string, data: UpdateDeliveryData): Promise<Delivery>;
}
