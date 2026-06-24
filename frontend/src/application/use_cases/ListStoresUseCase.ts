import { UseCase } from './UseCase';
import { Store } from '../../domain/entities/Place';
import { PlaceRepositoryProtocol } from '../../domain/repositories/PlaceRepositoryProtocol';

export class ListStoresUseCase implements UseCase<void, Store[]> {
  constructor(private placeRepository: PlaceRepositoryProtocol) {}

  async execute(): Promise<Store[]> {
    return await this.placeRepository.listStores();
  }
}
