import { UseCase } from './UseCase';
import { Store } from '../../domain/entities/Place';
import { PlaceRepositoryProtocol } from '../../domain/repositories/PlaceRepositoryProtocol';
import { Coordinates } from '../../domain/value_objects/Coordinates';

export interface CreateStoreInput {
  name: string;
  location: { lat: number; lng: number };
  ownerId: string;
}

export class CreateStoreUseCase implements UseCase<CreateStoreInput, Store> {
  constructor(private placeRepository: PlaceRepositoryProtocol) {}

  async execute(input: CreateStoreInput): Promise<Store> {
    if (!input.name || !input.location || !input.ownerId) {
      throw new Error('name, location e ownerId são obrigatórios.');
    }

    const location = new Coordinates(input.location);
    return await this.placeRepository.createStore(input.name, location, input.ownerId);
  }
}
