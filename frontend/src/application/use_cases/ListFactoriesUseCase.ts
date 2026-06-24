import { UseCase } from './UseCase';
import { Factory } from '../../domain/entities/Place';
import { PlaceRepositoryProtocol } from '../../domain/repositories/PlaceRepositoryProtocol';

export class ListFactoriesUseCase implements UseCase<void, Factory[]> {
  constructor(private placeRepository: PlaceRepositoryProtocol) {}

  async execute(): Promise<Factory[]> {
    return await this.placeRepository.listFactories();
  }
}
