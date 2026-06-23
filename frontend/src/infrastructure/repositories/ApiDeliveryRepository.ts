import { DeliveryRepositoryProtocol, UpdateDeliveryData } from '../../domain/repositories/DeliveryRepositoryProtocol';
import { Delivery, DeliveryProps } from '../../domain/entities/Delivery';
import { DeliveryStatus } from '../../domain/DeliveryStatus';
import { apiClient } from '../api/api_client';

interface DeliveryApiResponse {
  id?: string;
  factory_id?: string;
  factoryId?: string;
  store_id?: string;
  storeId?: string;
  driver_id?: string;
  driverId?: string;
  status?: string;
  eta_original?: string;
  etaOriginal?: string;
  eta_current?: string;
  etaCurrent?: string;
  departed_at?: string;
  departedAt?: string;
  current_lat?: number;
  currentLat?: number;
  current_lng?: number;
  currentLng?: number;
}

function pick(raw: DeliveryApiResponse, snake: keyof DeliveryApiResponse, camel: keyof DeliveryApiResponse): string {
  return (raw[snake] || raw[camel] || '') as string;
}

function parseDate(raw: DeliveryApiResponse, snake: keyof DeliveryApiResponse, camel: keyof DeliveryApiResponse): Date | undefined {
  const val: string | undefined = (raw[snake] || raw[camel]) as string | undefined;
  return val ? new Date(val) : undefined;
}

function parseNum(raw: DeliveryApiResponse, snake: keyof DeliveryApiResponse, camel: keyof DeliveryApiResponse): number | undefined {
  return ((raw[snake] ?? raw[camel]) as number | undefined) ?? undefined;
}

function toDelivery(raw: DeliveryApiResponse): Delivery {
  const props: DeliveryProps = {
    factoryId: pick(raw, 'factory_id', 'factoryId'),
    storeId: pick(raw, 'store_id', 'storeId'),
    driverId: pick(raw, 'driver_id', 'driverId'),
    status: (raw.status ?? 'pendente') as DeliveryStatus,
    etaOriginal: parseDate(raw, 'eta_original', 'etaOriginal'),
    etaCurrent: parseDate(raw, 'eta_current', 'etaCurrent'),
    departedAt: parseDate(raw, 'departed_at', 'departedAt'),
    currentLat: parseNum(raw, 'current_lat', 'currentLat'),
    currentLng: parseNum(raw, 'current_lng', 'currentLng'),
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
