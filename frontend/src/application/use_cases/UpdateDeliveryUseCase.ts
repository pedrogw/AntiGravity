import { UseCase } from './UseCase';
import { Delivery } from '../../domain/entities/Delivery';
import { DeliveryRepositoryProtocol, UpdateDeliveryData } from '../../domain/repositories/DeliveryRepositoryProtocol';

export interface UpdateDeliveryInput {
  deliveryId: string;
  data: UpdateDeliveryData;
}

export class UpdateDeliveryUseCase implements UseCase<UpdateDeliveryInput, Delivery> {
  constructor(private deliveryRepository: DeliveryRepositoryProtocol) {}

  async execute(input: UpdateDeliveryInput): Promise<Delivery> {
    if (!input.deliveryId) {
      throw new Error('deliveryId é obrigatório.');
    }
    return await this.deliveryRepository.updateDelivery(input.deliveryId, input.data);
  }
}
