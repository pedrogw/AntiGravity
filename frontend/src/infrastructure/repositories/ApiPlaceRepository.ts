import { PlaceRepositoryProtocol } from '../../domain/repositories/PlaceRepositoryProtocol';
import { Factory, Store } from '../../domain/entities/Place';
import { CoordinatesProps, Coordinates } from '../../domain/value_objects/Coordinates';

export class ApiPlaceRepository implements PlaceRepositoryProtocol {
  async createFactory(name: string, location: CoordinatesProps): Promise<Factory> {
    // Mock implementation for now
    return new Factory({ name, location: new Coordinates(location) });
  }

  async createStore(name: string, location: CoordinatesProps, ownerId: string): Promise<Store> {
    // Mock implementation for now
    return new Store({ name, location: new Coordinates(location), ownerId });
  }
}
