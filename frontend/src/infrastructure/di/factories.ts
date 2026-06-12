import { ApiAuthRepository } from '../repositories/ApiAuthRepository';
import { ApiPlaceRepository } from '../repositories/ApiPlaceRepository';
import { ApiDeliveryRepository } from '../repositories/ApiDeliveryRepository';
import { TokenStorageAdapter } from '../storage/TokenStorageAdapter';

const deliveryRepository = new ApiDeliveryRepository();
const tokenStorageAdapter = new TokenStorageAdapter();
const apiAuthRepository = new ApiAuthRepository();

export const DI = {
  tokenStorage: tokenStorageAdapter,
  authRepository: apiAuthRepository,
  placeRepository: new ApiPlaceRepository(),
  deliveryRepository,
};

import { LoginUseCase } from '../../application/use_cases/LoginUseCase';
import { LogoutUseCase } from '../../application/use_cases/LogoutUseCase';
import { CreateDeliveryUseCase } from '../../application/use_cases/CreateDeliveryUseCase';
import { ListDeliveriesUseCase } from '../../application/use_cases/ListDeliveriesUseCase';
import { UpdateDeliveryUseCase } from '../../application/use_cases/UpdateDeliveryUseCase';
import { CreateFactoryUseCase } from '../../application/use_cases/CreateFactoryUseCase';
import { CreateStoreUseCase } from '../../application/use_cases/CreateStoreUseCase';

export const makeLoginUseCase = () => new LoginUseCase(DI.authRepository, DI.tokenStorage);
export const makeLogoutUseCase = () => new LogoutUseCase(DI.authRepository, DI.tokenStorage);
export const makeCreateDeliveryUseCase = () => new CreateDeliveryUseCase(DI.deliveryRepository);
export const makeListDeliveriesUseCase = () => new ListDeliveriesUseCase(DI.deliveryRepository);
export const makeUpdateDeliveryUseCase = () => new UpdateDeliveryUseCase(DI.deliveryRepository);
export const makeCreateFactoryUseCase = () => new CreateFactoryUseCase(DI.placeRepository);
export const makeCreateStoreUseCase = () => new CreateStoreUseCase(DI.placeRepository);
