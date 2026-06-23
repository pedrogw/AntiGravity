import { PlaceRepositoryProtocol } from '../../domain/repositories/PlaceRepositoryProtocol';
import { Factory, Store } from '../../domain/entities/Place';
import { Coordinates } from '../../domain/value_objects/Coordinates';

export class ApiPlaceRepository implements PlaceRepositoryProtocol {
  async createFactory(name: string, location: Coordinates): Promise<Factory> {
    return new Factory({ name, location });
  }

  async createStore(name: string, location: Coordinates, ownerId: string): Promise<Store> {
    return new Store({ name, location, ownerId });
  }
}
