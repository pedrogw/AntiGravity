import { AlertRepositoryProtocol } from '../../domain/repositories/AlertRepositoryProtocol';
import { Alert } from '../../domain/entities/Alert';
import { apiClient } from '../api/api_client';

interface AlertApiResponse {
  id: string;
  delivery_id: string;
  message: string;
  is_critical: boolean;
  created_at: string;
}

function toAlert(raw: AlertApiResponse): Alert {
  return new Alert({
    deliveryId: raw.delivery_id,
    message: raw.message,
    isCritical: raw.is_critical,
    createdAt: new Date(raw.created_at),
  }, raw.id);
}

export class ApiAlertRepository implements AlertRepositoryProtocol {
  async listAll(deliveryId?: string, limit = 50, offset = 0): Promise<Alert[]> {
    const params: Record<string, string | number> = { limit, offset };
    if (deliveryId) params.delivery_id = deliveryId;
    const { data } = await apiClient.get('/alerts', { params });
    return (data || []).map(toAlert);
  }
}
