import { DeliveryRepositoryProtocol, UpdateDeliveryData } from '../../domain/repositories/DeliveryRepositoryProtocol';
import { Delivery, DeliveryProps } from '../../domain/entities/Delivery';
import { apiClient } from '../api/api_client';

function toDelivery(raw: any): Delivery {
  const props: DeliveryProps = {
    factoryId: raw.factory_id || raw.factoryId,
    storeId: raw.store_id || raw.storeId,
    driverId: raw.driver_id || raw.driverId,
    status: raw.status,
    etaOriginal: raw.eta_original || raw.etaOriginal ? new Date(raw.eta_original || raw.etaOriginal) : undefined,
    etaCurrent: raw.eta_current || raw.etaCurrent ? new Date(raw.eta_current || raw.etaCurrent) : undefined,
    departedAt: raw.departed_at || raw.departedAt ? new Date(raw.departed_at || raw.departedAt) : undefined,
    currentLat: raw.current_lat ?? raw.currentLat,
    currentLng: raw.current_lng ?? raw.currentLng,
  };
  return new Delivery(props, raw.id);
}

export class ApiDeliveryRepository implements DeliveryRepositoryProtocol {
  async createDelivery(factoryId: string, storeId: string, driverId: string): Promise<Delivery> {
    const { data } = await apiClient.post('/deliveries/', {
      factory_id: factoryId,
      store_id: storeId,
      driver_id: driverId,
    });
    return toDelivery(data);
  }

  async listDeliveries(role?: string, limit = 50, offset = 0): Promise<Delivery[]> {
    const { data } = await apiClient.get('/deliveries/', {
      params: { limit, offset },
    });
    return (data || []).map(toDelivery);
  }

  async updateDelivery(id: string, update: UpdateDeliveryData): Promise<Delivery> {
    const { data } = await apiClient.patch(`/deliveries/${id}`, {
      status: update.status,
      lat: update.lat,
      lng: update.lng,
    });
    return toDelivery(data);
  }
}
