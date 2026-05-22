import { UseCase } from './UseCase';
import { Factory } from '../../domain/entities/Place';
import { PlaceRepositoryProtocol } from '../../domain/repositories/PlaceRepositoryProtocol';
import { CoordinatesProps } from '../../domain/value_objects/Coordinates';

export interface CreateFactoryInput {
  name: string;
  location: CoordinatesProps;
}

export class CreateFactoryUseCase implements UseCase<CreateFactoryInput, Factory> {
  constructor(private placeRepository: PlaceRepositoryProtocol) {}

  async execute(input: CreateFactoryInput): Promise<Factory> {
    if (!input.name || !input.location) {
      throw new Error('name e location são obrigatórios.');
    }

    return await this.placeRepository.createFactory(input.name, input.location);
  }
}
