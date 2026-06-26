import { ApiAuthRepository } from '../repositories/ApiAuthRepository';
import { ApiPlaceRepository } from '../repositories/ApiPlaceRepository';
import { ApiDeliveryRepository } from '../repositories/ApiDeliveryRepository';
import { ApiUserRepository } from '../repositories/ApiUserRepository';
import { ApiAlertRepository } from '../repositories/ApiAlertRepository';
import { TokenStorageAdapter } from '../storage/TokenStorageAdapter';

const deliveryRepository = new ApiDeliveryRepository();
const tokenStorageAdapter = new TokenStorageAdapter();
const apiAuthRepository = new ApiAuthRepository();

export const DI = {
  tokenStorage: tokenStorageAdapter,
  authRepository: apiAuthRepository,
  placeRepository: new ApiPlaceRepository(),
  deliveryRepository,
  userRepository: new ApiUserRepository(),
  alertRepository: new ApiAlertRepository(),
};

import { LoginUseCase } from '../../application/use_cases/LoginUseCase';
import { LogoutUseCase } from '../../application/use_cases/LogoutUseCase';
import { CreateDeliveryUseCase } from '../../application/use_cases/CreateDeliveryUseCase';
import { ListDeliveriesUseCase } from '../../application/use_cases/ListDeliveriesUseCase';
import { UpdateDeliveryUseCase } from '../../application/use_cases/UpdateDeliveryUseCase';
import { CreateFactoryUseCase } from '../../application/use_cases/CreateFactoryUseCase';
import { CreateStoreUseCase } from '../../application/use_cases/CreateStoreUseCase';
import { ListDriversUseCase } from '../../application/use_cases/ListDriversUseCase';
import { ListFactoriesUseCase } from '../../application/use_cases/ListFactoriesUseCase';
import { ListStoresUseCase } from '../../application/use_cases/ListStoresUseCase';
import { ListAlertsUseCase } from '../../application/use_cases/ListAlertsUseCase';
import { DismissAlertUseCase } from '../../application/use_cases/DismissAlertUseCase';
import { GetStoreByIdUseCase } from '../../application/use_cases/GetStoreByIdUseCase';

export const makeLoginUseCase = () => new LoginUseCase(DI.authRepository, DI.tokenStorage);
export const makeLogoutUseCase = () => new LogoutUseCase(DI.authRepository, DI.tokenStorage);
export const makeCreateDeliveryUseCase = () => new CreateDeliveryUseCase(DI.deliveryRepository);
export const makeListDeliveriesUseCase = () => new ListDeliveriesUseCase(DI.deliveryRepository);
export const makeUpdateDeliveryUseCase = () => new UpdateDeliveryUseCase(DI.deliveryRepository);
export const makeCreateFactoryUseCase = () => new CreateFactoryUseCase(DI.placeRepository);
export const makeCreateStoreUseCase = () => new CreateStoreUseCase(DI.placeRepository);
export const makeListDriversUseCase = () => new ListDriversUseCase(DI.userRepository);
export const makeListFactoriesUseCase = () => new ListFactoriesUseCase(DI.placeRepository);
export const makeListStoresUseCase = () => new ListStoresUseCase(DI.placeRepository);
export const makeListAlertsUseCase = () => new ListAlertsUseCase(DI.alertRepository);
export const makeDismissAlertUseCase = () => new DismissAlertUseCase(DI.alertRepository);
export const makeGetStoreByIdUseCase = () => new GetStoreByIdUseCase(DI.placeRepository);
