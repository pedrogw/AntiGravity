import { UseCase } from './UseCase';
import { Delivery } from '../../domain/entities/Delivery';
import { DeliveryRepositoryProtocol } from '../../domain/repositories/DeliveryRepositoryProtocol';

export interface ListDeliveriesInput {
  role?: string;
}

export class ListDeliveriesUseCase implements UseCase<ListDeliveriesInput, Delivery[]> {
  constructor(private deliveryRepository: DeliveryRepositoryProtocol) {}

  async execute(input: ListDeliveriesInput = {}): Promise<Delivery[]> {
    return await this.deliveryRepository.listDeliveries(input.role);
  }
}
