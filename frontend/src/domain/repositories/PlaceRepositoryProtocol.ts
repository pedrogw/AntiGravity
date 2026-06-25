import { Factory, Store } from '../entities/Place';
import { Coordinates } from '../value_objects/Coordinates';

export interface PlaceRepositoryProtocol {
  createFactory(name: string, location: Coordinates): Promise<Factory>;
  createStore(name: string, location: Coordinates, ownerId: string): Promise<Store>;
  listFactories(): Promise<Factory[]>;
  listStores(): Promise<Store[]>;
  getStoreById(id: string): Promise<Store>;
}
