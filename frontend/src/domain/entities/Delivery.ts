import { Entity } from './Entity';
import { DeliveryStatus } from '../DeliveryStatus';

export interface DeliveryProps {
  factoryId: string;
  storeId: string;
  driverId: string;
  status?: DeliveryStatus;
  etaOriginal?: Date;
  etaCurrent?: Date;
  departedAt?: Date;
  currentLat?: number;
  currentLng?: number;
}

export class Delivery extends Entity<DeliveryProps> {
  get factoryId() { return this.props.factoryId; }
  get storeId() { return this.props.storeId; }
  get driverId() { return this.props.driverId; }
  get status(): DeliveryStatus { return this.props.status || 'pendente'; }
  get etaOriginal() { return this.props.etaOriginal; }
  get etaCurrent() { return this.props.etaCurrent; }
  get departedAt() { return this.props.departedAt; }
  get currentLat() { return this.props.currentLat; }
  get currentLng() { return this.props.currentLng; }
}
