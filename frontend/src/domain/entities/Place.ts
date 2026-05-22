import { Entity } from './Entity';
import { Coordinates } from '../value_objects/Coordinates';

export interface FactoryProps {
  name: string;
  location: Coordinates;
}

export class Factory extends Entity<FactoryProps> {
  get name(): string { return this.props.name; }
  get location(): Coordinates { return this.props.location; }
}

export interface StoreProps {
  name: string;
  location: Coordinates;
  ownerId: string;
}

export class Store extends Entity<StoreProps> {
  get name(): string { return this.props.name; }
  get location(): Coordinates { return this.props.location; }
  get ownerId(): string { return this.props.ownerId; }
}
