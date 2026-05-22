import { UseCase } from './UseCase';
import { Delivery } from '../../domain/entities/Delivery';
import { DeliveryRepositoryProtocol } from '../../domain/repositories/DeliveryRepositoryProtocol';

export interface CreateDeliveryInput {
  factoryId: string;
  storeId: string;
  driverId: string;
}

export class CreateDeliveryUseCase implements UseCase<CreateDeliveryInput, Delivery> {
  constructor(private deliveryRepository: DeliveryRepositoryProtocol) {}

  async execute(input: CreateDeliveryInput): Promise<Delivery> {
    if (!input.factoryId || !input.storeId || !input.driverId) {
      throw new Error('factoryId, storeId e driverId são obrigatórios.');
    }

    return await this.deliveryRepository.createDelivery(
      input.factoryId,
      input.storeId,
      input.driverId
    );
  }
}
