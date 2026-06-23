import { UseCase } from './UseCase';
import { Factory } from '../../domain/entities/Place';
import { PlaceRepositoryProtocol } from '../../domain/repositories/PlaceRepositoryProtocol';
import { Coordinates } from '../../domain/value_objects/Coordinates';

export interface CreateFactoryInput {
  name: string;
  location: { lat: number; lng: number };
}

export class CreateFactoryUseCase implements UseCase<CreateFactoryInput, Factory> {
  constructor(private placeRepository: PlaceRepositoryProtocol) {}

  async execute(input: CreateFactoryInput): Promise<Factory> {
    if (!input.name || !input.location) {
      throw new Error('name e location são obrigatórios.');
    }

    const location = new Coordinates(input.location);
    return await this.placeRepository.createFactory(input.name, location);
  }
}
