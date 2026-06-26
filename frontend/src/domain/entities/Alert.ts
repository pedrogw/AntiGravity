import { Entity } from './Entity';

export interface AlertProps {
  deliveryId: string;
  message: string;
  isCritical: boolean;
  createdAt: Date;
  dismissedAt?: Date | null;
}

export class Alert extends Entity<AlertProps> {
  get deliveryId() { return this.props.deliveryId; }
  get message() { return this.props.message; }
  get isCritical() { return this.props.isCritical; }
  get createdAt() { return this.props.createdAt; }
  get dismissedAt() { return this.props.dismissedAt; }
  get isDismissed() { return !!this.props.dismissedAt; }
}
