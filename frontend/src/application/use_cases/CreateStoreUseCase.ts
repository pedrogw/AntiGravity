import { UseCase } from './UseCase';
import { Store } from '../../domain/entities/Place';
import { PlaceRepositoryProtocol } from '../../domain/repositories/PlaceRepositoryProtocol';
import { CoordinatesProps } from '../../domain/value_objects/Coordinates';

export interface CreateStoreInput {
  name: string;
  location: CoordinatesProps;
  ownerId: string;
}

export class CreateStoreUseCase implements UseCase<CreateStoreInput, Store> {
  constructor(private placeRepository: PlaceRepositoryProtocol) {}

  async execute(input: CreateStoreInput): Promise<Store> {
    if (!input.name || !input.location || !input.ownerId) {
      throw new Error('name, location e ownerId são obrigatórios.');
    }

    return await this.placeRepository.createStore(input.name, input.location, input.ownerId);
  }
}
