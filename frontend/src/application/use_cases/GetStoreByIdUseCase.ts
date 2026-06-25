import { UseCase } from './UseCase';
import { Store } from '../../domain/entities/Place';
import { PlaceRepositoryProtocol } from '../../domain/repositories/PlaceRepositoryProtocol';

export class GetStoreByIdUseCase implements UseCase<string, Store> {
  constructor(private placeRepository: PlaceRepositoryProtocol) {}

  async execute(id: string): Promise<Store> {
    return await this.placeRepository.getStoreById(id);
  }
}
